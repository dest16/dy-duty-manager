# Generated by Django 3.2.3 on 2021-10-18 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0031_auto_20211018_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dutycalendar',
            name='deleteTime',
            field=models.DateTimeField(default=None, null=True, verbose_name='删除时间'),
        ),
        migrations.AlterField(
            model_name='dutyclassify',
            name='deleteTime',
            field=models.DateTimeField(default=None, null=True, verbose_name='删除时间'),
        ),
        migrations.AlterField(
            model_name='dutypersonnel',
            name='deleteTime',
            field=models.DateTimeField(default=None, null=True, verbose_name='删除时间'),
        ),
        migrations.AlterField(
            model_name='holidaysandfestivals',
            name='deleteTime',
            field=models.DateTimeField(default=None, null=True, verbose_name='删除时间'),
        ),
        migrations.AlterField(
            model_name='holidaysandfestivalsplan',
            name='deleteTime',
            field=models.DateTimeField(default=None, null=True, verbose_name='删除时间'),
        ),
    ]
