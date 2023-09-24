from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class BlockedUserAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # Проверка, заблокирован ли пользователь
        if user.is_blocked:
            return None  # Заблокированным пользователям не разрешается вход

        # Проверка пароля (или других методов аутентификации, если необходимо)
        if user.check_password(password):
            return user
        return None