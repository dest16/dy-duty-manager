# Generated by Django 3.2.3 on 2021-09-07 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0013_alter_holidaysandfestivals_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holidaysandfestivals',
            name='plan',
            field=models.TextField(verbose_name='倍数计划'),
        ),
    ]
