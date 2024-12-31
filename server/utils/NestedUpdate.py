from rest_framework import viewsets


class NestedUpdateByPKViewSet(viewsets.ModelViewSet):
    """
        使用drf_writable_nested进行嵌套操作（创建、更新）时，遇到了一个问题：
            （1）嵌套列表中的实例的主键使用“pk”可正常创建、更新，但若使用“id”等其他字段名，则只能创建，无法更新，报错id已存在；
            （2）查看drf_writable_nested相关源码及Github的issue，自定义主键早已支持，且报错出现在调用drf_writable_nested之前；
            （3）由此可见该类问题可能并非drf_writable_nested不支持自定义主键，但目前未能找到问题原因。

        由于花费了较多时间，未能解决问题，遂使用一个公用父类，重写update方法，将嵌套实例的主键字段名修改为“pk”，以支持嵌套更新。
        【注意】此嵌套指的是“反”嵌套，即若M2中某字段外键关联到M1，则操作M1时，同步更新M2的数据；并非网上提到的depth嵌套
    """

    # The list of field names to be converted to "pk". When the model to be updated is nested with multiple custom
    # primary keys, how many primary key field names are provided in the list, all will be replaced with "pk"
    # E.g: converted_pk_fields = ["id"] or converted_pk_fields = ["id", "user_id", "role_id", ...]
    converted_pk_fields = ["id"]

    # 替换主键
    def replace_pk(self, instance):
        for k, v in instance.items():  # 循环前端提交的json
            if isinstance(v, list):  # 判断字段是否是（嵌套的）数组类型
                for i, obj in enumerate(v):  # 循环（嵌套的）数组
                    if isinstance(obj, dict):  # 判断数组元素是否是对象（实例）
                        for f in self.converted_pk_fields:  # 循环要转换为pk的预定义字段名数组
                            if f in obj.keys():  # 如果某个字段名属于对象（实例），则认为它是第一个匹配到的主键【目前存在BUG】
                                obj["pk"] = obj.pop(f)  # 将找到的主键值赋给pk，并加到对象（实例）中，同时删除原主键
                                break

                        self.replace_pk(obj)  # 递归查找嵌套并替换pk

    def update(self, request, *args, **kwargs):
        self.replace_pk(request.data)

        return super().update(request, *args, **kwargs)
