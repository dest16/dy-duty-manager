from django_filters import rest_framework as filters
from .models import HolidaysAndFestivals, DutyCalendar


class HolidaysAndFestivalsFilter(filters.FilterSet):
    ym = filters.CharFilter(field_name='date', lookup_expr='startswith')  # 过滤数据表中date字段以参数ym（str）开头的记录

    class Meta:
        model = HolidaysAndFestivals
        fields = ('date',)


class DutyCalendarFilter(filters.FilterSet):
    ym = filters.CharFilter(field_name='date', lookup_expr='startswith')

    class Meta:
        model = DutyCalendar
        fields = ('date',)
