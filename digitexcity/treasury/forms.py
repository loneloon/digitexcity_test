from patterns.reused_forms import BaseControlForm
from mainapp.models import AppRegister
from django import forms
from .models import Transfer

"""
If needed may be used to initiate transfers from Treasury side 
"""


class TransferSaveForm(BaseControlForm):
    class Meta:
        model = Transfer
        exclude = ('user', 'email_code')
