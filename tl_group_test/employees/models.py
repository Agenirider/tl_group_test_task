import datetime

from django.db import models


class Departments(models.Model):
    departament_name = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return f'{self.departament_name}'

    class Meta:
        verbose_name_plural = "Departments"


EMPLOYEE_STATUS = (('ordinary', 'ordinary'),
                   ('manager', 'manager'),
                   )


class Employees(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    family = models.CharField(max_length=30, blank=False, null=False)
    hire_date = models.DateField(default=datetime.date.today, blank=False, null=False)
    dismissal_date = models.DateField(blank=True, null=True)
    job_title = models.CharField(choices=EMPLOYEE_STATUS,
                                 default='ordinary',
                                 max_length=8,
                                 blank=False,
                                 null=False)

    department = models.ForeignKey(Departments,
                                   null=True,
                                   on_delete=models.CASCADE)

    salary = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True,
                                    null=False,
                                    blank=False)

    rank = models.IntegerField(default=5)
    manager = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name="employees",
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.family}'

    @property
    def get_subordinate(self):
        sub = list(Employees.objects.filter(manager=self.pk))
        if sub:
            return sub

    class Meta:
        verbose_name_plural = "Employees"
