from rest_framework.views import exception_handler
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    自定义REST API异常处理
    :param exc: 异常
    :param context: 文本
    :return: null
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    if isinstance(exc, IntegrityError):
        if "UNIQUE" in str(exc):
            try:
                try:
                    field_dict = context["view"].serializer_class().fields
                except:
                    field_dict = {}

                field_label_list = []
                for f in str(exc).split(":")[1].split(","):
                    if not f.strip().endswith("deleteTime"):
                        field = f.strip().split(".")[-1]
                        try:
                            # 将字段名转化为verbose_name返回，更加直观
                            field_label_list.append(field_dict[field].label)
                        except:
                            field_label_list.append(field)

                response = Response({'message': '『%s』等字段的值已存在，请勿重复添加！' % "、".join(field_label_list)}, status=status.HTTP_400_BAD_REQUEST)
            except:
                response = Response({'message': '重复数据无法添加，请检查！'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response({'message': '服务器出现未知错误'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        response = exception_handler(exc, context)
        # 更改部分异常文本描述
        if response:
            if isinstance(response.data, dict):
                for k, v in response.data.items():
                    try:
                        if v[0].code == 'unique':
                            # 值班类型中'key', 'deleteTime'联合唯一（实际上是key唯一，由于是假删除，必须联合'deleteTime'），当出现重复时，重写异常提示文本
                            if 'key' in v[0] and context['view'].basename.lower() == 'dutyclassify':
                                response.data[k] = u"类型键值『%s』已存在。" % context['request'].data['key']

                    except:
                        pass
            elif isinstance(response.data, list):
                pass
            else:
                pass

            # Now add the HTTP status code to the response.
            # if response is not None:
            #     response.data['status_code'] = response.status_code

    return response
