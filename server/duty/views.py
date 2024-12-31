import datetime
from django.middleware.csrf import get_token
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework import status
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from personnel.models import DutyCalendarPlan
from common.send_wechat import send_inform


# 获取CSRFToken
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({"csrfToken": token}, status=status.HTTP_200_OK)


# 根据token获取用户信息
def get_user_info(request):
    try:
        jwt_object = JWTAuthentication()
        token = request.headers.get("Authorization")
        # 去掉AUTH_HEADER_TYPES前缀：Bearer （注意这里有个空格）
        token = token[7:]
        validated_token = jwt_object.get_validated_token(token)
        user = jwt_object.get_user(validated_token)
        user_info = {
            "name": "%s%s" % (user.last_name, user.first_name)
        }

        return JsonResponse(user_info, status=status.HTTP_200_OK)
    except AuthenticationFailed:
        return JsonResponse({"msg": u"身份验证失败，请重新登录。", "code": 100401}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return JsonResponse({"msg": u"服务器发生未知错误，请联系网站管理员。", "code": 100500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 获取指定月份整月的排班表（无需登录）
def get_whole_month_plan(request):
    ym = request.GET["ym"]
    queryset = DutyCalendarPlan.objects.filter(isActive=True, date__date__startswith=ym)
    class_data_list = []  # 存放值班类型数据，数组中元素为值班类型UUID转的字符串
    class_data_tuple = []  # 存放值班类型数据，数组中元素为元组 (类型id，类型名称，顺序)
    plan_data_dict = {}  # 存放排班计划数据，字典中元素为字典 { 日期：{ 值班类型：人名 } }
    for i in queryset:
        class_id = str(i.classify.id)
        if class_id not in class_data_list:
            class_data_list.append(class_id)
            class_data_tuple.append((class_id, i.classify.label, i.classify.sequence))

        plan_data_dict.setdefault(i.date.date.strftime("%Y-%m-%d"), {})[class_id] = i.personnel.name

    plan_data_list = []  # 存放排班计划数据，数组中元素为字典 { date: xxx, ... }
    for date in sorted(plan_data_dict):
        plan_data_list.append({"date": date, **plan_data_dict[date]})

    return JsonResponse({
        "plan": plan_data_list,
        "class": sorted(class_data_tuple, key=lambda x: x[2])
    }, status=status.HTTP_200_OK)


# 定时发送值班提醒
def send_duty_plan():
    """
    2022-11-07 推送规则修改如下：
    （1）无论什么时候发，同一个内容必须发 1+1 次，即第一次直接发，第二次检查是否发生了更新，若有更新则再发一次
    （2）每天19点30分，发送次日值班计划；
    （3）每天10点30分检查今日值班计划是否发生了更新，若发生了更新，则再发一遍
    """

    weekday_dict = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    plan_url = "http://dm.sanxiacloud.com/MonthPlan?ym="
    now = datetime.datetime.now()
    hour = now.hour
    today = now.strftime("%Y-%m-%d")
    weekday = weekday_dict[now.weekday()]

    # 检查是否发生了更新
    if hour in [10]:
        yesterday = (now.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
        lastSendTime = datetime.datetime.fromisoformat("%s 19:30:00" % yesterday)
        queryset = DutyCalendarPlan.objects.filter(isActive=True, date__date=today)
        message = ""
        update = False
        for i in queryset:
            modifyTime = datetime.datetime.fromisoformat(datetime.datetime.strftime(i.modifyTime, "%Y-%m-%d %H:%M:%S"))
            # 如果有任何一条记录修改时间大于上一次推送时间，表示值班计划可能发生了变化，要重新推送
            if modifyTime > lastSendTime:
                update = True

            p = i.personnel
            message = message + "\n◆ %s：%s（%s）" % (i.classify.label, p.name, p.tel)

        if update is True:
            # 获取今日是否有“节假日”的排班，以此来获取节假日名称
            holiday_list = queryset.filter(classify__holidayOnly=True)
            if len(holiday_list) > 0:
                try:
                    festival_name = holiday_list[0].date.festival.name or weekday
                except:
                    festival_name = weekday
            else:
                festival_name = weekday

            subject = "【值班通知（新）】 %s %s" % (today, festival_name)
            send_inform(subject, message, plan_url + now.strftime("%Y-%m"))

    # 直接发次日的值班计划
    if hour in [19]:
        next_day = now.today() + datetime.timedelta(days=1)
        tomorrow = next_day.strftime("%Y-%m-%d")
        weekday = weekday_dict[(now.today() + datetime.timedelta(days=1)).weekday()]
        queryset = DutyCalendarPlan.objects.filter(isActive=True, date__date=tomorrow)
        message = ""
        for i in queryset:
            p = i.personnel
            message = message + "\n◆ %s：%s（%s）" % (i.classify.label, p.name, p.tel)

        # 获取次日是否有“节假日”的排班，以此来获取节假日名称
        holiday_list = queryset.filter(classify__holidayOnly=True)
        if len(holiday_list) > 0:
            try:
                festival_name = holiday_list[0].date.festival.name or weekday
            except:
                festival_name = weekday
        else:
            festival_name = weekday

        subject = "【值班通知】 %s %s" % (tomorrow, festival_name)

        send_inform(subject, message, plan_url + next_day.strftime("%Y-%m"))

    """
    if hour in [10, 15]:
        queryset = DutyCalendarPlan.objects.filter(isActive=True, date__date=today)
        lastSendTime = datetime.datetime.fromisoformat("%s 10:10:00" % today)
        subject = "【%s %s】" % (today, weekday)
        message = ""
        update = False
        for i in queryset:
            modifyTime = datetime.datetime.fromisoformat(datetime.datetime.strftime(i.modifyTime, "%Y-%m-%d %H:%M:%S"))
            # 如果有任何一条记录修改时间大于上一次推送时间，表示值班计划可能发生了变化，要重新推送
            if modifyTime > lastSendTime:
                update = True

            p = i.personnel
            message = message + "\n◆ %s：%s(%s)" % (i.classify.label, p.name, p.tel)

        if hour == 10 or (hour == 15 and update is True):
            send_inform(subject, message)

    if hour in [16, 21]:
        tomorrow = (now.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        weekday = weekday_dict[(now.today() + datetime.timedelta(days=1)).weekday()]
        queryset = DutyCalendarPlan.objects.filter(isActive=True, date__date=tomorrow)
        # 获取次日是否有“节假日”的排班，以此来判断次日是不是节假日
        holiday_list = queryset.filter(classify__holidayOnly=True)
        if len(holiday_list) > 0:
            lastSendTime = datetime.datetime.fromisoformat("%s 16:10:00" % today)
            try:
                festival_name = holiday_list[0].date.festival.name or weekday
            except:
                festival_name = weekday

            subject = "【%s%s】" % (tomorrow, " " + festival_name)
            message = ""
            update = False
            for i in queryset:
                modifyTime = datetime.datetime.fromisoformat(datetime.datetime.strftime(i.modifyTime, "%Y-%m-%d %H:%M:%S"))
                # 如果有任何一条记录修改时间大于上一次推送时间，表示值班计划可能发生了变化，要重新推送
                if modifyTime > lastSendTime:
                    update = True

                p = i.personnel
                message = message + "\n◆ %s：%s(%s)" % (i.classify.label, p.name, p.tel)

            if hour == 16 or (hour == 21 and update is True):
                send_inform(subject, message)
    """
