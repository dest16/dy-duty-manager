from rest_framework import viewsets, decorators, response


class ExtraActionAPIViewSet(viewsets.ModelViewSet):
    """
        每个API的公共扩展方法
    """

    queryset_values_fields = ['id']

    @decorators.action(methods=['get'], detail=False, url_path='count', url_name='count')
    def count(self, request):
        try:
            count = self.queryset.count()
        except:
            count = len(self.queryset)

        return response.Response(count)

    @decorators.action(methods=['get'], detail=False, url_path='dictionary', url_name='dictionary')
    def dictionary(self, request):
        """
            支持用户自定义URL参数【?fields=f1,f2,f3...】，用于查询用户想得到的信息，主要是为了去掉不关心的字段，提高查询效率\n
            但是为了数据信息的安全，自定义的fields必须是queryset_values_fields(系统预先设定的字段集)的子集元素\n
            例如：fields=id,name,date,password，而queryset_values_fields=['id', 'name', 'date', 'plan']\n
            那么API将返回 { 'id': xxx, 'name': xxx, 'date': xxx }
        """
        try:
            try:
                user_custom_fields = request.query_params["fields"].split(",")
                final_fields = set(user_custom_fields) & set(self.queryset_values_fields)  # 求交集
                if len(final_fields) <= 0:
                    final_fields = self.queryset_values_fields
            except:
                # 如果自定义字段不存在，则默认返回允许的所有字段
                final_fields = self.queryset_values_fields

            queryset = self.queryset.values(*final_fields)
        except:
            # 如果允许的字段出现异常，则返回所有字段
            queryset = self.queryset.values()

        return response.Response(queryset)
