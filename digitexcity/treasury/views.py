from django.shortcuts import render, reverse, HttpResponseRedirect, Http404
from .models import UserTreasury, Transfer
from .forms import TransferSaveForm
from patterns.reused_forms import UserValidation
from patterns.reused_funcs import send_email_validation_code, redirect_302
from authapp.models import BaseUser
from mainapp.models import AppRegister
from django.contrib.auth.decorators import login_required
import random
import json
import copy
import hashlib


@login_required(login_url='auth:signin')
def display(request):
    """
    Treasury index page to display balance
    :param request:
    :return:
    """

    title = 'Treasury'

    userbalance = UserTreasury.get_balance(user=request.user)

    content = {'title': title, 'balance': userbalance}

    return render(request, 'treasury/treasury.html', content)


@login_required(login_url='auth:signin')
def transfer_funds(request):
    """
    This view is accessed by API 302 redirects from application to manage transaction records
    and poke Treasury to perform balance action on its side
    :param request:
    :return:
    """

    title = 'Transfer'

    print(request.POST)
    print(request.GET)

    content = {'title': title}

    if request.method == 'POST':
        if request.POST['email_code']:
            pending_transfer = Transfer.objects.filter(tracking_id=request.POST['tracking_id']).first()

            if hashlib.sha256(request.POST['email_code'].encode('utf-8')).hexdigest() == pending_transfer.email_code:
                UserTreasury.withdraw(user=pending_transfer.user, amount=float(pending_transfer.amount))
                pending_transfer.status = 'APRVD'
            else:
                pending_transfer.status = 'CNCLD'

            pending_transfer.save()
            updated_query = copy.deepcopy(request.POST)
            updated_query['status'] = pending_transfer.status
            return redirect_302(re_path=pending_transfer.app.name + ':transfer_complete', query_dict=updated_query)
        else:
            return HttpResponseRedirect(reverse('main:index'))

    else:
        # api_tail - зашитый в форму словарь параметров от dapi
        if request.GET['receiver'] == 'app':
            status = 'AW_CF'
        elif request.GET['receiver'] == 'treasury':
            status = 'APRVD'

        pending_transfer = Transfer.objects.create(
            user=request.user,
            app=AppRegister.objects.filter(id=int(request.GET['app'])).first(),
            amount=float(request.GET['amount']),
            currency_code=request.GET['currency_code'],
            sender=request.GET['sender'],
            receiver=request.GET['receiver'],
            status=status,
            tracking_id=request.GET['tracking_id'],
            callback_url=request.GET['callback_url'],
            signature=request.GET['signature'],
            email_code=send_email_validation_code(request.user)
        )

        if pending_transfer.status == 'AW_CF':
            content['validation_form'] = UserValidation()
            content['api_tail'] = {k: v for k, v in request.GET.items()}
            return render(request, 'treasury/validation.html', content)

        elif pending_transfer.status == 'APRVD':
            updated_query = {k: v for k, v in request.GET.items()}
            updated_query['status'] = 'APRVD'
            UserTreasury.deposit(user=pending_transfer.user, amount=float(pending_transfer.amount))
            return redirect_302(re_path=pending_transfer.app.name+':transfer_complete', query_dict=updated_query)
        else:
            return Http404


@login_required(login_url='auth:signin')
def transaction_details(request):
    """
    This view provides a transaction info snippet by API redirect from application
    :param request:
    :return:
    """
    if request.method == 'GET':

        info = Transfer.objects.filter(tracking_id=request.GET['tracking_id']).first()

        content = {'title': 'Transfer Details'}
        content['track_id'] = info.tracking_id
        content['from_to'] = "From {0} - To {1}".format((info.app.name if info.sender == 'app' else 'treasury'), (info.app.name if info.receiver == 'app' else 'treasury'))
        content['status'] = info.status
        content['amount'] = str(info.amount) + ' ' + info.currency_code
        content['created'] = info.created_at
        content['updated'] = info.updated_at

        return render(request, 'treasury/trans_info.html', content)

    else:
        return Http404


