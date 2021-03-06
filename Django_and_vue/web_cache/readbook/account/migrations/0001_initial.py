# Generated by Django 3.0.7 on 2020-07-14 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=30)),
                ('phone', models.CharField(max_length=20, verbose_name='Phone')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('uimg', models.CharField(max_length=256, null=True)),
                ('date_of_birth', models.CharField(max_length=40, verbose_name='birth_date')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='join_date')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last_login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
