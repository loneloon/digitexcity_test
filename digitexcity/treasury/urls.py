from django.urls import path, re_path, include

import treasury.views as treasury

app_name = 'treasury'

urlpatterns = [
    path('', treasury.display, name='display'),
    path('transfer/', treasury.transfer_funds, name='transfer'),
    path('transaction-details/', treasury.transaction_details, name='transaction_details'),
]
