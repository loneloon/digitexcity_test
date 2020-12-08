from django.urls import path, re_path, include

import dapi.views as dapi

app_name = 'dapi'

urlpatterns = [
    path('wallet/external-transfer', dapi.external_transfer, name='external_transfer'),
    path('wallet/external-transaction-status', dapi.external_transaction_status, name='external_transaction_status'),
]