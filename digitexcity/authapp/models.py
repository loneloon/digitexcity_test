from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


class BaseUser(AbstractUser):

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expiration = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expiration:
            return False
        else:
            return True
