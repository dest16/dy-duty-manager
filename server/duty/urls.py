"""duty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_bulk.routes import BulkRouter

# *** swagger START ***
import user_agents
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg import openapi, views

swagger_info = openapi.Info(
    title="Duty Management API",
    default_version='v1.0.0',
    description="""
        This is a demo project for the [drf-yasg](https://github.com/axnsan12/drf-yasg) Django Rest Framework library.
        The `swagger-ui` view can be found [here](/cached/swagger).
        The `ReDoc` view can be found [here](/cached/redoc).
        The swagger YAML document can be found [here](/cached/swagger.yaml).
        
        You can log in using the pre-existing `admin` user with password `passwordadmin`.
    """,  # noqa
    # terms_of_service="https://www.google.com/policies/terms/",
    # contact=openapi.Contact(email="contact@snippets.local"),
    # license=openapi.License(name="BSD License"),
)

SchemaView = views.get_schema_view(
    # validators=['ssv', 'flex'],  # ssv会导致批量BulkRouter库引入时，swagger报错
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
    info=''
)


def root_redirect(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = user_agents.parse(user_agent_string)

    if user_agent.is_mobile:
        schema_view = 'cschema-redoc'
    else:
        schema_view = 'cschema-swagger-ui'

    return redirect(schema_view, permanent=True)

# *** swagger END ***


# 引入app的urls
from personnel.urls import router as personnel_router
# from test111.urls import router as test111_router
router = BulkRouter()
router.registry.extend(personnel_router.registry)
# router.registry.extend(test111_router.registry)

# *** Token ***
from rest_framework_simplejwt.views import TokenRefreshView
from utils.Token import CustomTokenObtainPairView

# *** CSRF token && User info ***
from .views import get_csrf_token, get_user_info, get_whole_month_plan


urlpatterns = [
    path('admin/', admin.site.urls),
    # REST API Auth
    re_path(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # *** swagger START ***
    re_path(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^redoc-old/$', SchemaView.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),
    re_path(r'^cached/swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=None), name='cschema-json'),
    re_path(r'^cached/swagger/$', SchemaView.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    re_path(r'^cached/redoc/$', SchemaView.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),
    re_path(r'^$', root_redirect),
    # *** swagger END ***
    re_path(r'^api/', include(router.urls)),
    # *** Token ***
    re_path(r'^api/token/obtain/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # *** CSRF token && User info ***
    re_path(r'^api/csrf-token/', get_csrf_token, name='get_csrf_token'),
    re_path(r'^api/user/info/', get_user_info, name='get_user_info'),
    # *** 无登录获取整月排班计划 ***
    re_path(r'^api/get_whole_month_plan/', get_whole_month_plan, name='get_whole_month_plan')
]
