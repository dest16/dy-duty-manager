REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ],

    # 控制REST API访问的权限【一旦开启，REST API必须在登录后才能使用】
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAdminUser',  # 必须是管理员
        'rest_framework.permissions.IsAuthenticated',  # 必须是有效用户
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 自上而下顺序认证
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # 与JWTTokenUserAuthentication择其一
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',  # 单点登录专用
        'rest_framework.authentication.SessionAuthentication',  # REST API 及 Django-admin
        'rest_framework.authentication.BasicAuthentication',
    ),

    # 分页
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PAGINATION_CLASS': 'utils.Pagination.CustomLimitOffsetPagination',
    'PAGE_SIZE': 10,

    # 自定义REST API异常处理方法
    'EXCEPTION_HANDLER': 'utils.ExceptionHandler.custom_exception_handler'
}
