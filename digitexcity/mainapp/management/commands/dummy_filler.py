from django.core.management.base import BaseCommand
from authapp.models import BaseUser as User

import json
import os

JSON_SOURCE = 'mainapp/json'

admins_username = 'digitadmin'


def read_json(file_name):
    with open(os.path.join(JSON_SOURCE, file_name + '.json'), 'r') as jf:
        return json.load(jf)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # redundant command, creates superuser

        if not User.objects.filter(username=admins_username):
            User.objects.create_superuser(admins_username, 'adm@digitexcity.local', 'secret666')
        else:
            print('Admin already exists.')