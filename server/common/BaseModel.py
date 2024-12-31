import uuid
import datetime
from django.db import models


class BaseModel(models.Model):
    """
        本项目所有模型（model）的基础类
        规定了id（UUID格式）、isActive（用于假删除）、createTime（创建时间）、modifyTime（修改时间）
        重写了delete方法，用于通过is_active实现假删除
        同时，为了让假删除与unique_together不出现冲突，每个model都加了deleteTime，默认为''，只有isActive改为
    """
    id = models.UUIDField(verbose_name="UUID", primary_key=True, default=uuid.uuid1)
    isActive = models.BooleanField(verbose_name="是否有效", default=True)
    # isActive假删除启用时，deleteTime将作为所有model的unique_together必带的字段（否则isActive无论true/false，创建、删除都会报错）
    # 而deleteTime默认值不能用 None（null），必须用 ""，因为数据库中 null != null 恒成立
    deleteTime = models.CharField(verbose_name=u"删除时间", default="", max_length=19)
    createTime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    modifyTime = models.DateTimeField(verbose_name="最新修改时间", auto_now=True)

    class Meta:
        abstract = True  # 抽象基类，告诉django，不用在数据库创建对应的表

    # 【弃用】由于“假删除”会导致on_delete失效，暂时未能找到非常好的方法兼容“假删除”与on_delete联动，故暂且弃用“假删除”
    # def delete(self, using=None, keep_parents=False):
    #     self.isActive = False
    #     self.deleteTime = datetime.datetime.now().strftime("%F %T")
    #     self.save()
