from rest_framework_bulk.routes import BulkRouter
from .views import UserViewSet, AvatarViewSet, AccessKeyViewSet, SiteViewSet, ProfileViewSet, HolidaysAndFestivalsViewSet, HolidaysAndFestivalsPlanViewSet

app_name = 'test111'

router = BulkRouter()  # 支持批量操作
router.register(r'users', UserViewSet)
router.register(r'avatar', AvatarViewSet)
router.register(r'accessKey', AccessKeyViewSet)
router.register(r'site', SiteViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'userHolidaysAndFestivals', HolidaysAndFestivalsViewSet)
router.register(r'userHolidaysAndFestivalsPlan', HolidaysAndFestivalsPlanViewSet)

urlpatterns = router.urls
