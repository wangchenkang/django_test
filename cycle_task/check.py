import os
import errno
import sys
import shutil
import psutil
import urllib.request

if __name__ == '__main__':
    # p = psutil.Process(int(sys.argv[1]))
    # if p.status() == psutil.STATUS_ZOMBIE:
    #     print('done....')
    db_path = '{}/new/hunting_tracker/cycle_task/'.format('/tmp')
    try:
        os.makedirs(db_path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            shutil.rmtree(db_path)
            os.makedirs(db_path)

    url = 'http://192.168.9.103:60011/script/download/{}/?name={}'.format(10, 'untitled.txt')
    urllib.request.urlretrieve(url, '{}{}'.format(db_path, 'untitled.txt'))

    print('done....')

