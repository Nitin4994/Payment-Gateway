# Generated by Django 2.2.7 on 2021-01-22 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fName', models.CharField(max_length=50, verbose_name='first_name')),
                ('lName', models.CharField(max_length=50, verbose_name='last_name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=500, verbose_name='password')),
                ('address', models.CharField(max_length=350, verbose_name='address')),
                ('dob', models.DateField(verbose_name='date_of_birth')),
                ('company', models.CharField(max_length=50, verbose_name='company')),
            ],
            options={
                'db_table': 'Manager',
            },
        ),
    ]
