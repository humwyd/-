# Generated by Django 3.0.7 on 2020-07-24 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backed', '0003_auto_20200722_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='avg_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=6, null=True),
        ),
    ]
