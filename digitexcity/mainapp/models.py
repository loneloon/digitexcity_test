from django.db import models
from django.conf import settings
from patterns.reused_funcs import gather_balances
import sys


class AppRegister(models.Model):
    """
    This class implements an app register model based on _app tag in included apps
    to reference app_names, app_ids.

    it also has a useful method which returns an app-balance model for each app included in settings file
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=20, unique=True)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated', auto_now=True)

    @staticmethod
    def get_items():
        return AppRegister.objects.all()

    @classmethod
    def get_model_for_app(cls, app_name):
        return getattr(sys.modules[app_name + '.models'], app_name.capitalize()[:-4] + 'Balance')