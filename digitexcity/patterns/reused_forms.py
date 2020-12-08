from django import forms

"""
This module contains useful transfer forms which may be used by treasury and connected apps as well
"""


class BaseControlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserValidation(forms.Form):
    """
    This form is called by treasury for validation codes input

    Google code is just a placeholder for now, you may enter any 6-digit number, it won't be validated
    """
    email_code = forms.CharField(label='Email Code', max_length=6)
    google_code = forms.CharField(label='Google Code', max_length=6)


class AppDepositTemplate(forms.Form):
    """
    This form is called by connected apps to initiate withdraw or deposit action with treasury
    """

    CURRENCY_CODES = (
        ('USD', 'US Dollar'),
    )
    TRANSFER_ACTIONS = (
        ('TTA', 'Treasury -> App Balance'),
        ('ATT', 'App Balance -> Treasury')
    )

    amount = forms.IntegerField(label="Amount")
    currency_code = forms.ChoiceField(label=False, choices=CURRENCY_CODES)
    transfer_action = forms.ChoiceField(label="From - To", choices=TRANSFER_ACTIONS)
