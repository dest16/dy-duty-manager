# Generated by Django 3.2.3 on 2021-09-16 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0021_alter_dutypersonnel_tel'),
    ]

    operations = [
        migrations.AddField(
            model_name='holidaysandfestivals',
            name='allowanceMultiple',
            field=models.FloatField(default=1, max_length=2, verbose_name='基本津贴倍数'),
        ),
        migrations.AddField(
            model_name='holidaysandfestivals',
            name='classify',
            field=models.ForeignKey(default='4de9a362-fc18-11eb-8231-f4b52024bb83', on_delete=django.db.models.deletion.DO_NOTHING, to='personnel.dutyclassify', verbose_name='值班类型'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='holidaysandfestivals',
            name='subsidizedMealsMultiple',
            field=models.FloatField(default=1, max_length=2, verbose_name='餐饮补贴倍数'),
        ),
        migrations.AddField(
            model_name='holidaysandfestivals',
            name='totalAllowance',
            field=models.FloatField(default=0, max_length=4, verbose_name='总津贴'),
        ),
        migrations.AddField(
            model_name='holidaysandfestivals',
            name='totalSubsidizedMeals',
            field=models.FloatField(default=0, max_length=4, verbose_name='总餐补'),
        ),
        migrations.AlterField(
            model_name='dutypersonnel',
            name='classify',
            field=models.ManyToManyField(to='personnel.DutyClassify', verbose_name='值班类型'),
        ),
        migrations.AlterField(
            model_name='holidaysandfestivals',
            name='date',
            field=models.DateField(verbose_name='日期'),
        ),
        migrations.AlterUniqueTogether(
            name='holidaysandfestivals',
            unique_together={('date', 'classify', 'isActive')},
        ),
        migrations.RemoveField(
            model_name='holidaysandfestivals',
            name='plan',
        ),
    ]
