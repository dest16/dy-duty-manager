# from rest_framework import routers
from rest_framework_bulk.routes import BulkRouter
from .views import HolidaysAndFestivalsViewSet, HolidaysAndFestivalsPlanViewSet, DutyClassifyViewSet, DutyPersonnelViewSet, DutyCalendarViewSet, DutyCalendarPlanViewSet

app_name = 'personnel'

# router = routers.DefaultRouter()  # 不支持批量操作
router = BulkRouter()  # 支持批量操作
router.register(r'HolidaysAndFestivals', HolidaysAndFestivalsViewSet)
router.register(r'HolidaysAndFestivalsPlan', HolidaysAndFestivalsPlanViewSet)
router.register(r'DutyClassify', DutyClassifyViewSet)
router.register(r'DutyPersonnel', DutyPersonnelViewSet)
router.register(r'DutyCalendar', DutyCalendarViewSet)
router.register(r'DutyCalendarPlan', DutyCalendarPlanViewSet)

urlpatterns = router.urls
