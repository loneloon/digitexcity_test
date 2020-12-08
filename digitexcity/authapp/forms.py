from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import BaseUser
import hashlib
import random


class BaseUserSignIn(AuthenticationForm):
    class Meta:
        model = BaseUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for param_name, param in self.fields.items():
            param.widget.attrs['class'] = 'form-control'


class BaseUserRegistration(UserCreationForm):
    class Meta:
        model = BaseUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for param_name, param in self.fields.items():
            param.widget.attrs['class'] = 'form-control'
            param.help_text = ''

    def save(self, *args, **kwargs):
        """Custom save method to implement email activation key
        """

        user = super(BaseUserRegistration, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user
