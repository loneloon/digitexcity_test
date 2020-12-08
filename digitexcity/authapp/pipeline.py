from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from treasury.models import UserTreasury
from authapp.views import create_balance_stack


def add_balance_stack(backend, user, response, *args, **kwargs):
    """
    This function creates db entries for Treasury and included user app-balance accounts
    as a part of pipeline sequence for google signup registrations.

    create_balance_stack func. is also included in ordinary registration view for manual sign-ups.

    :param backend:
    :param user:
    :param response:
    :param args:
    :param kwargs:
    :return:
    """
    return create_balance_stack(user)
