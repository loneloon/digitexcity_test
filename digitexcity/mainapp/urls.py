from django.urls import path, re_path, include

import mainapp.views as mainapp

app_name = 'mainapp'

# short and sweet, just a lonely index url

urlpatterns = [
    path('', mainapp.index, name='index')
]