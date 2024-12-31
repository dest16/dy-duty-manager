from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
        由于rest_framework的LimitOffsetPagination无法通过传入limit实现是否分页的控制，若在客户端传入limit=9999999999，会非常丑
        因此重写REST自带分页器的paginate_queryset方法，实现当limit传入-1时，则查询全部数据（即不分页）
    """
    def paginate_queryset(self, queryset, request, view=None):
        try:
            req_limit = request.query_params[self.limit_query_param]
        except:
            req_limit = None

        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []

        if req_limit == "-1":
            self.offset = 0
            return list(queryset)
        else:
            return list(queryset[self.offset:self.offset + self.limit])
