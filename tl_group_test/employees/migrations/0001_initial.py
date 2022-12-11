# Generated by Django 3.2.8 on 2022-12-10 08:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departament_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('family', models.CharField(max_length=30)),
                ('hire_date', models.DateField(default=datetime.date.today)),
                ('dismissal_date', models.DateField(blank=True, null=True)),
                ('job_title', models.CharField(choices=[('ordinary', 'ordinary'), ('manager', 'manager')], default='ordinary', max_length=8)),
                ('salary', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('rank', models.IntegerField(default=5)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.departments')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='employees.employees')),
            ],
            options={
                'verbose_name_plural': 'Employees',
            },
        ),
    ]
