# Generated by Django 3.2.3 on 2021-09-08 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0018_alter_dutycalendar_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dutycalendar',
            name='date',
            field=models.DateField(db_index=True, verbose_name='日期'),
        ),
    ]
