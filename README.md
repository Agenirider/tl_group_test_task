# Develop
- перейдите в директорию с проектом
- добавьте виртуальное окружение Python
- установите дополнительные пакеты из requirements.txt
- создайте базу данных sqlite -  python manage.py migrate
- добавьте суперюзера - python manage.py ensure_admin
- заполните базу данных тестовыми данными - python fill_employees_data (замечание: процесс может занять пару минут и более)
- запустите проект python manage.py runserver


# Kind of prod
- установите Docker Desktop
- перейдите в директорию с проектом
- выполните команду docker-compose up --build
- При первом запуске база данных будет заполняться сотрудниками, 
это может занять некоторое время. 
Если не охота ждать - уменьшите значение переменной EMPLOYEE_MAX_QUANTITY в файле tl_group_test/employees/management/commands/fill_employees_data.py
 - проект доступен по адресу http://localhost:8000/