from django.db import transaction
from rest_framework import serializers
from rest_framework_bulk import BulkSerializerMixin


class BaseSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    deleteTime = serializers.CharField(required=False, read_only=True)  # read_only=True会导致unique_together出现500错误
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    modifyTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    # 重写save方法，开启django的数据库事务管理，避免批量操作时事务不一致
    def save(self, **kwargs):
        with transaction.atomic():
            return super().save(**kwargs)
