# Generated by Django 3.2.3 on 2021-09-08 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0016_auto_20210908_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dutycalendar',
            name='festival',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='personnel.holidaysandfestivals', verbose_name='节日'),
        ),
    ]
