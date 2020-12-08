import os
import datetime
from django.core.management.base import BaseCommand
import shutil


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        """
        This command deletes db file if it exists, wipes migrations from all connected apps

        :param args:
        :param kwargs:
        :return:
        """

        result_str = ''

        try:
            for file in os.scandir(os.getcwd()):
                if os.path.isdir(file.path):
                    if os.path.exists(file.path+'/migrations/'):
                        for contents in os.scandir(file.path+'/migrations/'):
                            if 'initial' in contents.name:
                                os.remove(contents.path)

                    if file.name == 'tmp':
                        shutil.rmtree(file.path)
                        print('[' + str(datetime.datetime.now()) + '] /tmp wiped.')

            result_str += 'Migrations wiped. '
        except:
            result_str += 'Error on migrations removal. '

        try:
            if os.path.exists('db.sqlite3'):
                os.remove('db.sqlite3')
                result_str += 'Db deleted.'
            else:
                result_str += 'No db found.'
        except:
            result_str += "Couldn't delete db."

        print('['+str(datetime.datetime.now())+'] ' + result_str)