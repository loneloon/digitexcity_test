from django.db import models
from django.conf import settings
from mainapp.models import AppRegister
from patterns.reused_forms import AppDepositTemplate
from patterns.reused_funcs import generate_tracking_id, generate_signature, redirect_302
from django.shortcuts import render, HttpResponseRedirect, reverse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from urllib.parse import urlencode


class SimpleBankBase(models.Model):
    """
    This class is used as a Base both by treasury and apps
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField('master balance', max_digits=20, decimal_places=2, default=0)

    @classmethod
    def get_balance(cls, user):
        return cls.objects.filter(user=user).first().balance

    @classmethod
    def withdraw(cls, user, amount):
        instance = cls.objects.filter(user=user).first()
        instance.balance = float(instance.balance) - amount
        instance.save()

    @classmethod
    def deposit(cls, user, amount):
        instance = cls.objects.filter(user=user).first()
        instance.balance = float(instance.balance) + amount
        instance.save()

    class Meta:
        abstract = True


class BaseTransfer(models.Model):
    """
    This class used as a Base for main Transfer model, used by Treasury to record and update transactions
    """

    PENDING = 'PNDNG'
    AWAITING_CONFIRMATION = 'AW_CF'
    CANCELLED = 'CNCLD'
    APPROVED = 'APRVD'

    TRANSFER_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (AWAITING_CONFIRMATION, 'Awaiting confirmation'),
        (CANCELLED, 'Cancelled'),
        (APPROVED, 'Approved'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    app = models.ForeignKey(AppRegister, verbose_name='Transfer to (APP)', on_delete=models.CASCADE)
    amount = models.FloatField('transfer amount', null=False)
    status = models.CharField('status', max_length=5, choices=TRANSFER_STATUS_CHOICES, default=PENDING)
    sender = models.CharField('sender', max_length=16)
    receiver = models.CharField('receiver', max_length=16)
    currency_code = models.CharField(max_length=3, null=True)
    tracking_id = models.CharField(max_length=128, unique=True, null=False)
    callback_url = models.CharField(max_length=30, null=False)
    signature = models.CharField(max_length=64, null=False)
    email_code = models.CharField(max_length=64, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        abstract = True


class AppViews:

    """
    This class is used as a view collector for each connected application (game_app, social_app, trade_app)
    """

    def __init__(self):
        pass

    @staticmethod
    @login_required(login_url='auth:signin')
    def initiate_transfer(request):
        """
        With this method Application initiates transfer dialogue on GET and redirects to API upon getting queries
        on POST
        :param request:
        :return:
        """

        if request.method == "GET":

            title = 'Secure Transfer'
            transfer_request_form = AppDepositTemplate()

            content = {'title': title, 'transfer_request': transfer_request_form, 'app_repath': request.path}

            return render(request, 'patterns/transfer_request.html', content)

        else:
            app_name = list(el for el in request.path.split('/') if el != "")[0]
            app = AppRegister.objects.filter(name__contains=app_name).first()
            track_id = generate_tracking_id(app.name, request.user.username)
            sender = 'treasury' if request.POST['transfer_action'][0] == 'T' else 'app'
            receiver = 'treasury' if request.POST['transfer_action'][2] == 'T' else 'app'

            new_values = dict()

            new_values['app'] = app.id
            new_values['amount'] = request.POST['amount']
            new_values['currency_code'] = request.POST['currency_code']
            new_values['sender'] = sender
            new_values['receiver'] = receiver
            new_values['tracking_id'] = track_id
            new_values['callback_url'] = (reverse('dapi:external_transaction_status'))
            new_values['signature'] = generate_signature(new_values)

            return redirect_302(re_path='dapi:external_transfer', query_dict=new_values)

    @staticmethod
    @login_required(login_url='auth:signin')
    def transfer_complete(request):
        """
        This method changes application balances in case of successful transaction and redirects to API for
        transaction-details view from treasury using callback_url + /?transaction_id=
        :param request:
        :return:
        """

        if request.method == 'GET':
            app_name = AppRegister.objects.filter(id=int(request.GET['app'])).first().name
            app = AppRegister.get_model_for_app(app_name=app_name)
            try:
                if request.GET['status'] == 'APRVD':
                    if request.GET['receiver'] == 'app':
                        app.deposit(user=request.user,
                                        amount=float((request.GET['amount'])))
                    elif request.GET['receiver'] == 'treasury':
                        app.withdraw(user=request.user,
                                     amount=float((request.GET['amount'])))

                return HttpResponseRedirect(request.GET['callback_url'] + '?tracking_id=' + request.GET['tracking_id'])
            except:
                return Http404

    @staticmethod
    @login_required(login_url='auth:signin')
    def display(request):
        """
        Virtually a basic index request for apps, displays balance and provides a MakeTransfer link
        :param request:
        :return:
        """

        app_name = list(el for el in request.path.split('/') if el != "")[0]+'_app'
        app = AppRegister.get_model_for_app(app_name=app_name)
        userbalance = app.get_balance(user=request.user)

        title = app_name.capitalize()[:-4]+' App'

        content = {'title': title, 'balance': userbalance, 'transfer_link': reverse(app_name+':transfer')}

        return render(request, 'patterns/app_balance.html', content)
