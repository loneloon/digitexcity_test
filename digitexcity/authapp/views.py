from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.conf import settings
from authapp.models import BaseUser
from authapp.forms import BaseUserSignIn, BaseUserRegistration
from django.urls import reverse
from django.core.mail import send_mail


# Balance partition models
from treasury.models import UserTreasury
from games_app.models import GamesBalance
from trade_app.models import TradeBalance
from social_app.models import SocialBalance


def signin(request):
    title = "Sign In"

    next_url = ''

    if request.method == 'GET' and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:index'))

    signin_form = BaseUserSignIn(data=request.POST)
    if request.method =='POST' and signin_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)

            if 'next' in request.POST.keys():
                next_url = request.POST['next']
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(reverse('main:index'))

    else:
        if 'next' in request.GET.keys():
            next_url = request.GET['next']

    content = {'title': title, 'signin_form': signin_form, 'next_url':next_url}
    return render(request, 'authapp/signin.html', content)


def signout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    title = 'Registration'

    if request.method == 'POST':
        reg_form = BaseUserRegistration(request.POST, request.FILES)

        if reg_form.is_valid():
            reg_form.save()
            user = BaseUser.objects.filter(username=request.POST['username']).first()
            create_balance_stack(user)

            if send_email_verification(user):
                print('Email verification sent.')
            else:
                print('Failed to send email verification.')

            return HttpResponseRedirect(reverse('auth:signin'))

    else:
        reg_form = BaseUserRegistration()

    content = {'title': title, 'reg_form': reg_form}

    return render(request, 'authapp/register.html', content)


def edit(request):
    return HttpResponseRedirect(reverse('main:index'))


def send_email_verification(user):
    verification_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Email verification message'

    message = f'In order to finalize the registration process at {settings.DOMAIN_NAME}\n' \
              f' we kindly ask you to verify your email by clicking the link below:\n' \
              f'{settings.DOMAIN_NAME}{verification_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = BaseUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error verifying email address: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error verifying email address: {e.args}')
        return HttpResponseRedirect(reverse('main:index'))


def create_balance_stack(user):
    partitions = [UserTreasury, GamesBalance, TradeBalance, SocialBalance]

    for model in partitions:
        if not model.objects.filter(user=user):
            model.objects.create(user=user)
