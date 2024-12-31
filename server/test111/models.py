from django.db import models
from common.BaseModel import BaseModel
from personnel.models import DutyClassify


class Site(models.Model):
    url = models.CharField(max_length=100)


class User(models.Model):
    username = models.CharField(max_length=100)


class AccessKey(models.Model):
    key = models.CharField(max_length=100)


class Profile(models.Model):
    sites = models.ManyToManyField(Site)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    access_key = models.ForeignKey(AccessKey, null=True, on_delete=models.DO_NOTHING)


class Avatar(models.Model):
    image = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, related_name='avatars', on_delete=models.DO_NOTHING)


class HolidaysAndFestivals(BaseModel):
    """
        节假日模型
        为了实现自动排班，且公司能自定义“假日”，允许手动提前录入假日信息
    """
    date = models.DateField(verbose_name=u"日期", blank=False, null=False)
    name = models.CharField(verbose_name=u"假日名称", blank=False, null=False, max_length=64)

    class Meta:
        unique_together = ['date', 'deleteTime']


class HolidaysAndFestivalsPlan(BaseModel):
    """
        节假日值班津贴加倍计划模型
    """
    classify = models.ForeignKey(DutyClassify, verbose_name=u"值班类型", on_delete=models.DO_NOTHING, related_name='user_hf_plan_classify')
    allowanceMultiple = models.FloatField(verbose_name=u"基本津贴倍数", default=1, max_length=2)
    totalAllowance = models.FloatField(verbose_name=u"总津贴", default=0, max_length=4)
    subsidizedMealsMultiple = models.FloatField(verbose_name=u"餐饮补贴倍数", default=1, max_length=2)
    totalSubsidizedMeals = models.FloatField(verbose_name=u"总餐补", default=0, max_length=4)
    festival = models.ForeignKey(HolidaysAndFestivals, verbose_name=u"节假日", on_delete=models.DO_NOTHING, related_name='plan')

    class Meta:
        unique_together = ['festival', 'classify', 'deleteTime']
