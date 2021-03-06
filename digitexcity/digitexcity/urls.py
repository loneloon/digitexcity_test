"""digitexcity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('mainapp.urls', namespace='main')),
    path('dapi/', include('dapi.urls', namespace='dapi')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('treasury/', include('treasury.urls', namespace='treasury')),
    path('social/', include('social_app.urls', namespace='social_app')),
    path('games/', include('games_app.urls', namespace='games_app')),
    path('trade/', include('trade_app.urls', namespace='trade_app')),

    re_path(r'^auth/verify/google/oauth2/', include("social_django.urls", namespace="google_auth")),
]

connected_apps = {}
