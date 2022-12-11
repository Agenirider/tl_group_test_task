import json
import random
import time
import traceback
from datetime import timedelta
from typing import List

import names
import redis

from employees.models import Employees
from tl_group_test import settings

REDIS_KEY_NAME: str = 'html_employees_structure'


def name_generator() -> List[str]:
    gender: str = random.choice(['male', "female"])
    random_name: str = names.get_full_name(gender=gender)
    return random_name.split()


def unpack_data() -> str:
    html_code: list = []

    def unpack_structure(emp_object):

        subs: list = emp_object.get_subordinate
        if subs and not emp_object.manager:
            html_code.append(f'<ul class="treeline">'
                             f'<li>TOP MANAGER {emp_object}'
                             f'<div class="drop" onclick="return showTree(this)">+</div>'
                             f'<ul style="display: auto">')
            for x in subs:
                unpack_structure(x)

        elif subs and emp_object.manager:
            html_code.append(f'<li >{emp_object} MANAGER OF {emp_object.department}'
                             f'<div class="drop" onclick="return showTree(this)">+</div>'
                             f'<ul style="display: auto">')
            for x in subs:
                unpack_structure(x)

        elif not subs and emp_object.manager:
            html_code.append(f'<li>{emp_object} {emp_object.department}</li>')

    big_boss: Employees = Employees.objects.get(rank=0)
    unpack_structure(big_boss)

    return ''.join(html_code)


""" Init cache access """
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT,
                                   db=0,
                                   socket_connect_timeout=1)

REDIS_IS_CONNECT: bool = False
max_connect_attempts = 1 if settings.DEBUG else 3

while True:
    try:
        REDIS_IS_CONNECT = redis_instance.ping()
        print('>>>>>> REDIS CONNECTED <<<<<<')
        break

    except (ConnectionError, TimeoutError,
            redis.exceptions.ConnectionError,
            redis.exceptions.TimeoutError):

        REDIS_IS_CONNECT = False

    if REDIS_IS_CONNECT:
        print('REDIS CONNECTED')
        pass

    else:
        time.sleep(2)
        print('FAIL CONNECTION to REDIS')
        max_connect_attempts -= 1

        if max_connect_attempts == 0:
            REDIS_IS_CONNECT = False
            break


def get_data_from_redis() -> str:
    cached_data: str = ''

    global REDIS_IS_CONNECT
    if REDIS_IS_CONNECT:
        try:
            cached_data: bytes = redis_instance.get(REDIS_KEY_NAME)
            print(f'[INFO] Получены кешированные данные {len(cached_data) if cached_data else ""}')

            try:
                cached_data: str = json.loads(cached_data)
            except TypeError:
                pass
        except redis.exceptions.TimeoutError:
            REDIS_IS_CONNECT = False
            pass

    if not cached_data:
        try:
            cached_data: str = unpack_data()
            redis_instance.setex(REDIS_KEY_NAME,
                                 timedelta(minutes=60),
                                 json.dumps(cached_data))
            print(f'[INFO] Данные {len(cached_data)} сохранены в кеш')
        except Exception:
            traceback.print_exc()

    return cached_data
