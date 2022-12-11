from typing import Iterator

import django
from django.core.management import BaseCommand

from employees.models import Departments, Employees
from employees.utils import name_generator

DEPARTMENTS_LIMIT: int = 25
HIERARCHY_MAX_LEVEL: int = 5
EMPLOYEE_MAX_QUANTITY: int = 50000


class Command(BaseCommand):
    def handle(self, *args, **options):

        try:
            # Добавляем топ менеджера
            name, family = name_generator()
            top_manager, is_created_top_manager = Employees.objects.get_or_create(pk=1,
                                                                                  name=name,
                                                                                  family=family,
                                                                                  salary=100000,
                                                                                  rank=0)

            if not is_created_top_manager:
                raise AttributeError

            # добавляем сотрудников по подразделениям(департаментам) - плоский лист
            # менеджер текущего уровня - первый сотрудник вышележащего уровня
            # делим общее количество сотрудников на максимальное количество департаментов
            # делаем итератор списка сотрудников - когда он заканчивается (при условии, что dep_id%5 без остатка)
            # переходим на нижележащий уровень и ставим менеджера уровня первого спеца из предыдущего уровня
            previous_level_dep: Departments = None
            current_rank: int = 1
            current_level_manager: Employees = None

            for dep_id in range(1, DEPARTMENTS_LIMIT + 1):
                print(f'Добавляем департамент #{dep_id}')
                department, is_created = Departments.objects.get_or_create(departament_name=f"department_{dep_id}")

                if not previous_level_dep:
                    current_level_manager = top_manager

                # определяем максимальное количество сотрудников на уровне
                dep_volume: int = round(EMPLOYEE_MAX_QUANTITY / DEPARTMENTS_LIMIT + 1)
                emp_iter: Iterator = iter(range(1, dep_volume))

                while True:
                    try:
                        next(emp_iter)
                        name, family = name_generator()
                        employee, _ = Employees.objects.get_or_create(name=name,
                                                                      family=family,
                                                                      department=department,
                                                                      manager=current_level_manager,
                                                                      rank=current_rank,
                                                                      salary=(100000 / current_rank) * 0.5)

                        print(f"Сотрудник {employee}, уровень - {current_rank}")

                    except StopIteration:
                        print('Департамент обработан')

                        if dep_id % 5 == 0:
                            current_rank += 1
                            # Берем спеца из предыдущего уровня, ставим его менеджером для текущего
                            previous_level_dep = department
                            current_level_manager = list(Employees.objects.filter(department=department))[-1]
                            current_level_manager.job_title = 'manager'
                            current_level_manager.salary = 100000 / current_rank
                            current_level_manager.save()

                        break
        except (AttributeError, django.db.utils.IntegrityError):
            print("Сотрудники уже добавлены")
