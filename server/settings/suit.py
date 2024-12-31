DATETIME_FORMAT = 'Y-m-d H:i:s'  # suit在admin里设置时间的一个小bug。需要把时间格式指定一下

DATE_FORMAT = 'Y-m-d'

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': u'内部管理系统后台',  # 后台title
    'HEADER_DATE_FORMAT': '',  # 后台显示当前日期格式，不填则为默认
    'HEADER_TIME_FORMAT': 'l H:i:s',  # 后台显示当前时间格式

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True,  # Default True
    # 'MENU_OPEN_FIRST_CHILD': True,  # Default True
    # 'MENU_EXCLUDE': ('auth.group',),  # 菜单排除括号中的项

    # suit建议, APP目录名字最好都用小写字母，避免不必要的麻烦发生
    'MENU': (
        'sites',
        {'app': 'accounts', 'label': u'用户管理', 'icon': 'icon-chevron-right', 'models': ({'model': 'MyUser', 'label': '用户信息'}, {'model': 'MyGroup', 'label': '分组授权'}, 'TenantsData', 'UserAvatar', 'AlipayAuthUser', 'QQAuthUser', 'ProblemFeedback', 'SMSNotification')},
        # '-',
        {'app': 'agreement', 'label': u'内容管理', 'models': ('AgreementTemplate',)},
        # '-',
    ),

    # 分页
    'LIST_PER_PAGE': 20,  # 后台list_display默认每页至多展示信息条数
}
