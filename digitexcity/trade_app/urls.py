from django.urls import path, re_path, include
from patterns.reused_models import AppViews

app_name = 'trade_app'

"""
All app urls are unified and based on pattern view class methods
"""

urlpatterns = [
    path('', AppViews.display, name='display'),
    path('transfer/', AppViews.initiate_transfer, name='transfer'),
    path('transfer/complete/', AppViews.transfer_complete, name='transfer_complete')
]