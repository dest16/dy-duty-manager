from django.contrib import admin
from .models import DutyClassify, DutyPersonnel


class DutyClassifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'allowance', 'subsidizedMeals', 'holidayOnly', 'doubleShift', 'color', 'sequence', 'createTime', 'modifyTime', 'isActive')


admin.site.register(DutyClassify, DutyClassifyAdmin)
admin.site.register(DutyPersonnel)
