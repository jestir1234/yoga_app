from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
import bcrypt
from .models.users import User

UserModel = get_user_model()


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        print('password.encode', password.encode('utf-8'))
        print('user.password.encode', user.password.encode('utf-8'))
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            return None
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
