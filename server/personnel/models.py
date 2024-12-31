from django.db import models
from common.BaseModel import BaseModel


class DutyClassify(BaseModel):
    """
        值班分类模型
    """
    label = models.CharField(verbose_name=u"类型名称", blank=False, null=False, max_length=16)
    allowance = models.FloatField(verbose_name=u"基础津贴", blank=False, null=False, default=0, max_length=16)
    subsidizedMeals = models.FloatField(verbose_name=u"餐饮补贴", blank=False, null=False, default=0, max_length=16)
    holidayOnly = models.BooleanField(verbose_name=u"仅假日班", default=False, help_text=u"只有假日才值的班。")
    doubleShift = models.BooleanField(verbose_name=u"假日双班", default=False, help_text=u"假日记作两个班次。")
    color = models.CharField(verbose_name=u"渲染颜色", blank=True, null=True, default='#000000', max_length=32)
    sequence = models.IntegerField(verbose_name=u"显示顺序", default=0, help_text=u"默认正序排列")

    class Meta:
        unique_together = ['label', 'deleteTime']


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
    classify = models.ForeignKey(DutyClassify, verbose_name=u"值班类型", on_delete=models.DO_NOTHING, related_name='festival_classify')
    allowanceMultiple = models.FloatField(verbose_name=u"基本津贴倍数", default=1, max_length=2)
    totalAllowance = models.FloatField(verbose_name=u"总津贴", default=0, max_length=4)
    subsidizedMealsMultiple = models.FloatField(verbose_name=u"餐饮补贴倍数", default=1, max_length=2)
    totalSubsidizedMeals = models.FloatField(verbose_name=u"总餐补", default=0, max_length=4)
    festival = models.ForeignKey(HolidaysAndFestivals, verbose_name=u"节假日", on_delete=models.CASCADE, related_name='festival_plan')

    class Meta:
        unique_together = ['festival', 'classify', 'deleteTime']


class DutyPersonnel(BaseModel):
    """
        值班人员模型
    """
    name = models.CharField(verbose_name=u"人员姓名", blank=False, null=False, max_length=64)
    tel = models.CharField(verbose_name=u"联系电话", blank=False, null=False, default='', max_length=16, unique=True)
    classify = models.ManyToManyField(DutyClassify, verbose_name=u"值班类型")
    sequence = models.IntegerField(verbose_name=u"值班顺序", default=0, help_text=u"默认正序排列")

    @property
    def classify_details(self):
        return self.classify


class DutyCalendar(BaseModel):
    """
        值班日历模型
    """
    date = models.DateField(verbose_name=u"日期", blank=False, null=False, db_index=True)
    holiday = models.BooleanField(verbose_name=u"是否假日", default=False)
    festival = models.ForeignKey(HolidaysAndFestivals, verbose_name=u"节假日", blank=True, null=True, on_delete=models.DO_NOTHING, related_name='calendar_festival')

    class Meta:
        unique_together = ['date', 'deleteTime']


class DutyCalendarPlan(BaseModel):
    """
        值班日历排班计划模型
    """
    date = models.ForeignKey(DutyCalendar, verbose_name=u"值班日期", on_delete=models.CASCADE, related_name='calendar_plan')
    classify = models.ForeignKey(DutyClassify, verbose_name=u"值班类型", on_delete=models.DO_NOTHING, related_name='calendar_classify')
    personnel = models.ForeignKey(DutyPersonnel, verbose_name=u"值班人员", on_delete=models.DO_NOTHING, related_name='calendar_personnel')
    totalAllowance = models.FloatField(verbose_name=u"总津贴", default=0, max_length=4)
    totalSubsidizedMeals = models.FloatField(verbose_name=u"总餐补", default=0, max_length=4)

    class Meta:
        unique_together = ['date', 'classify', 'deleteTime']
