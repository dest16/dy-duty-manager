from rest_framework import decorators, response
from .models import HolidaysAndFestivals, HolidaysAndFestivalsPlan, DutyClassify, DutyPersonnel, DutyCalendar, DutyCalendarPlan
from .serializers import HolidaysAndFestivalsSerializer, HolidaysAndFestivalsPlanSerializer, DutyClassifySerializer, DutyPersonnelSerializer, DutyCalendarSerializer, DutyCalendarPlanSerializer
from utils.BatchOperation import BatchOperationAPIViewSet
from utils.ExtraAction import ExtraActionAPIViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import HolidaysAndFestivalsFilter, DutyCalendarFilter
from utils.NestedUpdate import NestedUpdateByPKViewSet


class HolidaysAndFestivalsViewSet(ExtraActionAPIViewSet, BatchOperationAPIViewSet, NestedUpdateByPKViewSet):
    queryset = HolidaysAndFestivals.objects.filter(isActive=True).order_by('-date')
    serializer_class = HolidaysAndFestivalsSerializer
    allowed_batch_methods = ['patch', 'delete']
    queryset_values_fields = ['id', 'date', 'name', 'festival_plan']  # 限定ExtraActionAPIViewSet的dictionary返回结果集的字段
    # filter
    filter_backends = (DjangoFilterBackend,)
    filter_class = HolidaysAndFestivalsFilter
    # Field name converted to pk
    converted_pk_fields = ["id"]

    # 传入“XXXX-XX-XX”格式的日期，查询当前日期的所有假日数据
    @decorators.action(methods=['get'], detail=False, url_path='getHFDateDetail', url_name='getHFDateDetail')
    def get_hf_date_detail(self, request):
        try:
            date = request.query_params['date']
            queryset = self.queryset.filter(date=date).first()
            if queryset:
                serializer = self.serializer_class(queryset)
                obj = serializer.data
            else:
                obj = None
        except:
            obj = None

        return response.Response(obj)


class HolidaysAndFestivalsPlanViewSet(ExtraActionAPIViewSet, BatchOperationAPIViewSet):
    queryset = HolidaysAndFestivalsPlan.objects.filter(isActive=True).order_by('createTime')
    serializer_class = HolidaysAndFestivalsPlanSerializer
    allowed_batch_methods = ['patch', 'delete']


class DutyClassifyViewSet(ExtraActionAPIViewSet, BatchOperationAPIViewSet):
    queryset = DutyClassify.objects.filter(isActive=True).order_by('sequence', 'createTime')
    serializer_class = DutyClassifySerializer
    allowed_batch_methods = ['patch', 'delete']
    queryset_values_fields = ['id', 'label', 'color', 'allowance', 'subsidizedMeals', 'holidayOnly', 'doubleShift', 'sequence']


class DutyPersonnelViewSet(ExtraActionAPIViewSet, BatchOperationAPIViewSet):
    queryset = DutyPersonnel.objects.filter(isActive=True).order_by('sequence', 'createTime')
    serializer_class = DutyPersonnelSerializer
    allowed_batch_methods = ['patch', 'delete']
    queryset_values_fields = ['id', 'name', 'tel', 'classify']


class DutyCalendarViewSet(ExtraActionAPIViewSet, BatchOperationAPIViewSet, NestedUpdateByPKViewSet):
    queryset = DutyCalendar.objects.filter(isActive=True).order_by('-date')
    serializer_class = DutyCalendarSerializer
    allowed_batch_methods = ['patch', 'delete']
    queryset_values_fields = ['id', 'date', 'holiday', 'festival', 'calendar_plan']
    # filter
    filter_backends = (DjangoFilterBackend,)
    filter_class = DutyCalendarFilter
    # Field name converted to pk
    converted_pk_fields = ["id"]


class DutyCalendarPlanViewSet(ExtraActionAPIViewSet, BatchOperationAPIViewSet):
    queryset = DutyCalendarPlan.objects.filter(isActive=True).order_by('createTime')
    serializer_class = DutyCalendarPlanSerializer
    allowed_batch_methods = ['patch', 'delete']
