from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from duty.settings import PRIVATE_KEY
from utils.RSACrypt import rsa_decrypt


UserModel = get_user_model()


class CustomAuthBackend(ModelBackend):
    """
        自定义登录验证，实现手机号、邮箱等代替用户名
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 前端使用RSA加密了密码，先解密，再验证
        password = rsa_decrypt(password, PRIVATE_KEY)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            # 仅限username验证
            # user = UserModel._default_manager.get_by_natural_key(username)

            # 验证username或email，可自定义为任意model中的字段，但要注意唯一性，不能get超过1条记录
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
