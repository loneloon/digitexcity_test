from django.shortcuts import reverse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import uuid
import datetime
from urllib.parse import urlencode
import hashlib
import random
import string
import sys


def redirect_302(re_path, query_dict):
    response = HttpResponse(status=302)
    response['Location'] = "{0}?{1}".format(reverse(re_path), urlencode(query_dict))
    return response


def generate_tracking_id(app, user):
    date = str(datetime.datetime.now())[:19]
    mash = app + user + date
    return uuid.uuid3(uuid.NAMESPACE_DNS, mash).hex


def generate_signature(query_dict):
    signature = ''

    for idx, (key, val) in enumerate(query_dict.items()):
        if idx == 0:
            signature += f"{key}=" + urlencode({key: val})
        else:
            signature += f"&{key}=" + urlencode({key: val})

    signature = hashlib.sha256(signature.encode('utf-8'))
    return signature.hexdigest()


def send_email_validation_code(user):

    code = str()
    while len(code) < 6:
        code += str(random.choice(string.digits))

    title = f'Transaction validation code'

    message = f'Dear {user.first_name},\n' \
              f'\n' \
              f'In order to confirm your pending transaction\n' \
              f'we kindly ask you to enter the following code into the corresponding form field:\n' \
              f'{code}'

    send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    return hashlib.sha256(code.encode('utf-8')).hexdigest()


def get_apps():  # search project for included apps
    return tuple(app for app in settings.INSTALLED_APPS if '_app' in app)


def gather_balances():
    apps = get_apps()

    result = {}
    for app in apps:
        try:
            recovered_balance = getattr(sys.modules[app + '.models'], app.capitalize()[:-4] + 'Balance')
        except:
            recovered_balance = False

        if recovered_balance:
            result[app] = recovered_balance

    return result


