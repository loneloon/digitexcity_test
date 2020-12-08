from django.urls import path, re_path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('signin/', authapp.signin, name='signin'),
    path('signout/', authapp.signout, name='signout'),
    path('register/', authapp.register, name='register'),
    path('profile_edit/', authapp.edit, name='edit'),  # profile edit view is plugged with main page redirect
    re_path(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
]
