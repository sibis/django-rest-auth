from .models import User
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self,username=None, password=None):
        """
        Authentication method
        """

        try:
            user = User.objects.get(email=username)
            if user.check_password(password) and user.is_active:
                return user
        except:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except:
            return None
