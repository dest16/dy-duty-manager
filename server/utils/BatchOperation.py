from rest_framework import viewsets, response, exceptions, status
from django.shortcuts import get_object_or_404
from rest_framework_bulk import mixins


class BatchOperationAPIViewSet(mixins.BulkCreateModelMixin,
                               mixins.BulkUpdateModelMixin,
                               mixins.BulkDestroyModelMixin,
                               viewsets.ModelViewSet):

    allowed_batch_methods = ['get', 'post', 'put', 'patch', 'delete']

    # 先判断当前请求方法是否允许
    def __allowed_request_methods(self, request):
        # 字符串全部转为小写
        allowed_batch_methods = [i.lower() for i in self.allowed_batch_methods]
        request_method = str(request.stream.method).lower()
        if request_method in allowed_batch_methods:
            return True
        else:
            raise exceptions.ValidationError('非法请求！不允许 %s 方法。' % request_method)

    # 由于rest_framework_bulk的update方法出现错误，暂无法使用，遂自行实现批量update
    def bulk_update(self, request, *args, **kwargs):
        """
            当前重写批量更新方法，存在以下不足：
            （1）【事务一致性】以for循环形式逐一save，若出现错误，则当前错误以及之后的更新对象将不会被更新，之前的都已更新
            （2）......
        """
        if self.__allowed_request_methods(request) is True:
            # 获取批量更新时，以哪个字段作为key进行数据匹配【其实这个key也可以从前端动态传入，从request中获取】
            id_attr = getattr(self.serializer_class.Meta, 'update_lookup_field', 'id')
            partial = kwargs.pop('partial', False)
            instances = []  # 这个变量是用于保存修改过后的对象，返回给前端
            for item in request.data:  # 遍历列表中的每个对象
                instance = get_object_or_404(self.queryset, ** {'{}'.format(id_attr): str(item[id_attr])})
                # 构造序列化对象，注意partial=True表示允许局部更新
                # 调用父类 ModelViewSet 的get_serializer方法
                serializer = super().get_serializer(instance, data=item, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                instances.append(serializer.data)  # 将数据添加到列表中

            return response.Response(instances)

    # filters配合批量删除使用时有个问题，当过滤参数（例如id）传空时，就会删除所有数据，这是不可取的，遂自行实现批量delete
    def bulk_destroy(self, request, *args, **kwargs):
        if self.__allowed_request_methods(request) is True:
            qs = self.get_queryset()
            filtered = self.filter_queryset(qs)
            # 批量删除要求传入的data必须为数组且必须有元素，否则不允许删除
            if isinstance(request.data, list) and len(request.data) > 0:
                filtered = filtered.filter(id__in=request.data)  # 目前写死，删除时必须使用“id”为key
            else:
                filtered = qs

            if not self.allow_bulk_destroy(qs, filtered):
                return response.Response(status=status.HTTP_400_BAD_REQUEST)

            self.perform_bulk_destroy(filtered)

            return response.Response(status=status.HTTP_204_NO_CONTENT)
