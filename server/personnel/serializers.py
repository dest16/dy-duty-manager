from rest_framework import serializers
from .models import HolidaysAndFestivals, HolidaysAndFestivalsPlan, DutyClassify, DutyPersonnel, DutyCalendar, DutyCalendarPlan
from rest_framework_bulk import BulkListSerializer
from rest_framework.filters import SearchFilter
from common.BaseSerializer import BaseSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer


class HolidaysAndFestivalsPlanInlineSerializer(BaseSerializer):

    class Meta(object):
        model = HolidaysAndFestivalsPlan
        exclude = ['festival']


class HolidaysAndFestivalsSerializer(BaseSerializer, WritableNestedModelSerializer):
    # festival_plan 字段名必须要与 HolidaysAndFestivalsPlan 中FK festival 的 related_name 一模一样，否则API会报错 filed not exist
    festival_plan = HolidaysAndFestivalsPlanInlineSerializer(many=True, required=True)

    class Meta(object):
        model = HolidaysAndFestivals
        fields = "__all__"
        list_serializer_class = BulkListSerializer
        filter_backends = (SearchFilter,)
        update_lookup_field = 'id'


class HolidaysAndFestivalsPlanSerializer(BaseSerializer):

    class Meta(object):
        model = HolidaysAndFestivalsPlan
        fields = "__all__"
        list_serializer_class = BulkListSerializer
        filter_backends = (SearchFilter,)
        update_lookup_field = 'id'


class DutyClassifySerializer(BaseSerializer):
    allowance = serializers.FloatField(
        required=True,
        min_value=0,
        max_value=2000,
        error_messages={
            "invalid": u"基础津贴的值必须为非负数。",
            "min_value": u"基础津贴的值应在0 ~ 2000之间。",
            "max_value": u"基础津贴的值应在0 ~ 2000之间。"
        }
    )
    subsidizedMeals = serializers.FloatField(
        required=True,
        min_value=0,
        max_value=200,
        error_messages={
            "invalid": u"餐饮补贴的值必须为非负数。",
            "min_value": u"餐饮补贴的值应在0 ~ 200之间。",
            "max_value": u"餐饮补贴的值应在0 ~ 200之间。"
        }
    )

    class Meta(object):
        model = DutyClassify
        # exclude = ['isActive']  # 被排出的字段将不会在model层引用，因此也无法更新被排除的字段
        fields = "__all__"

        # 在Meta类下面的list_serializer_class选项用来修改当`many=True`时使用的类。
        # 默认情况下，DRF使用的是ListSerializer。
        # 但是ListSerializer没有实现自己的批量update方法。
        # 在DRF3中如果需要批量更新对象，则需定义此属性，并编写ListSerializer的子类
        # 所以bulk库提供了一个BulkListSerializer类
        # 它直接继承了ListSerializer，并重写了update方法。
        list_serializer_class = BulkListSerializer

        # 这条可以不写。但实际上，批量删除需要搭配过滤操作
        filter_backends = (SearchFilter,)

        # 批量更新时，默认使用id去匹配对象，可通过下列字段自定义匹配key
        update_lookup_field = 'id'


class DutyPersonnelSerializer(BaseSerializer):
    classify_details = DutyClassifySerializer(many=True, read_only=True)

    class Meta(object):
        model = DutyPersonnel
        fields = "__all__"
        list_serializer_class = BulkListSerializer
        filter_backends = (SearchFilter,)
        update_lookup_field = 'id'


class DutyCalendarPlanInlineSerializer(BaseSerializer):

    class Meta(object):
        model = DutyCalendarPlan
        exclude = ['date']


class DutyCalendarSerializer(BaseSerializer, WritableNestedModelSerializer):
    calendar_plan = DutyCalendarPlanInlineSerializer(many=True, required=True)

    class Meta(object):
        model = DutyCalendar
        fields = "__all__"
        list_serializer_class = BulkListSerializer
        filter_backends = (SearchFilter,)
        update_lookup_field = 'id'


class DutyCalendarPlanSerializer(BaseSerializer):

    class Meta(object):
        model = DutyCalendarPlan
        fields = "__all__"
        list_serializer_class = BulkListSerializer
        filter_backends = (SearchFilter,)
        update_lookup_field = 'id'
