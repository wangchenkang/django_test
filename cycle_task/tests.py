import random

import requests
import time
import argparse
from django.test import TestCase


def test():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=int, help='cycle task id')
    args = parser.parse_args()

    print('sub start: {}'.format(args.id))

    time.sleep(25)  # 假装在这里有业务逻辑

    requests.get('http://192.168.9.103:60011/terminology/platform/1/')

    url = "http://192.168.9.103:60011/cycle_task/send_result/"

    payload = {
        "id": args.id,
        "data": {
            "error_code": 0,
            "data": random.randint(0, 100)
        }
    }

    headers = {
        'content-type': "application/json",
    }

    requests.post(url, json=payload, headers=headers)

    print('sub end')


if __name__ == '__main__':
    test()
