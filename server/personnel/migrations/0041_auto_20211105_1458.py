# Generated by Django 3.2.3 on 2021-11-05 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0040_dutyclassify_doubleshift'),
    ]

    operations = [
        migrations.AddField(
            model_name='dutyclassify',
            name='holidayOnly',
            field=models.BooleanField(default=False, help_text='只有假日才值的班。', verbose_name='仅假日班'),
        ),
        migrations.AlterField(
            model_name='dutyclassify',
            name='doubleShift',
            field=models.BooleanField(default=False, help_text='假日记作两个班次。', verbose_name='假日双班'),
        ),
    ]
