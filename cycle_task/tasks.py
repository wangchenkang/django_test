import ast
import shutil
import subprocess
import urllib.request

from datetime import datetime, timedelta

import os

import errno
import psutil
from celery import shared_task

from cycle_task.models import CycleTask


@shared_task
def ttt():

    cycle_tasks = CycleTask.objects.filter(
        is_deleted=False, is_active=True
    ).prefetch_related('classification__script')

    for ct in cycle_tasks:

        if ct.pid == -100000:
            if ct.next_time and datetime.now() > ct.next_time:
                # 有对应脚本
                if ct.classification.script_id and \
                        ct.classification.script.is_deleted == 0:

                    db_path = '/tmp{}'.format(ct.classification.script.path)
                    try:
                        os.makedirs(db_path)
                    except OSError as e:
                        if e.errno == errno.EEXIST:
                            shutil.rmtree(db_path)
                            os.makedirs(db_path)

                    for f in ct.classification.script.name.split(','):
                        # :todo 之后写settings
                        url = 'http://192.168.9.103:60011' \
                              '/script/download/{}/?name={}'.format(
                                ct.classification.script_id, f
                              )
                        urllib.request.urlretrieve(
                            url, '{}{}'.format(db_path, f))

                    cmd = ct.classification.script.run_command.split(' ')
                    cmd.extend(['--id', str(ct.id)])

                    p = subprocess.Popen(
                        cmd,
                        cwd=os.path.dirname(db_path)
                    )

                    ct.pid = p.pid
                    ct.next_time = datetime.now() + timedelta(hours=ct.cycle)
                    ct.count += 1
                    ct.status = '正常'
                else:
                    ct.status = '失败'
                ct.save()
        else:
            if psutil.pid_exists(ct.pid):
                p = psutil.Process(ct.pid)
                if p.status() == psutil.STATUS_ZOMBIE:
                    result = ast.literal_eval(ct.result)
                    if result.get('error_code', -1) == 0:
                        ct.status = '停止'
                    else:
                        ct.status = '失败'

                    ct.pid = -100000
                    ct.save()
            else:
                # 这种情况不应该发生
                ct.status = '失败'
                ct.pid = -100000
                ct.save()

    return None


@shared_task
def clean():
    """
    什么都不做，就是为了刷掉defunct
    :return:
    """
    subprocess.Popen(['date'])
    return None
