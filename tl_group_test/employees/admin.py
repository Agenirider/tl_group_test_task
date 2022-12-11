from django.contrib import admin
from django.contrib.auth.models import Group

from employees.models import (Departments,
                              Employees,
                              #Relations
                              )


@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'departament_name',
                    )
    search_fields = ['departament_name']


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'family',
                    'job_title',
                    'hire_date',
                    'dismissal_date',
                    'department_id',
                    'salary',
                    'is_active',
                    'manager',
                    'rank'
                    )
    search_fields = ['name',
                     'family',
                     'department_id__departament_name',
                     'manager__name']


# @admin.register(Relations)
# class RelationsAdmin(admin.ModelAdmin):
#     list_display = ('id',
#                     'employee_id',
#                     'high_level_manager'
#                     )
#     search_fields = ['employee_id',
#                      'high_level_manager']


admin.site.unregister(Group)