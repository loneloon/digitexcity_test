from mainapp.models import AppRegister
from patterns.reused_funcs import get_apps
from django.core.management.base import BaseCommand


# This command will register all connected apps to the database (by default uses _app substring to detect the app)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        for app in get_apps():
            if not AppRegister.objects.filter(name=app):
                print('Adding ' + app + ' to the register...')
                try:
                    AppRegister.objects.create(name=app)
                    print('Success!')
                except Exception as e:
                    print('Error!', e)
            else:
                print(app + ' is already in the register!\nSkipping...')
