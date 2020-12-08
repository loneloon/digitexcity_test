from patterns.reused_funcs import redirect_302


def external_transfer(request):
    """
    Redirects to treasury transfer protocol with a GET query tail
    :param request:
    :return:
    """
    if request.method == 'GET':
        return redirect_302(re_path='treasury:transfer', query_dict=request.GET)


def external_transaction_status(request):
    """
    Redirects from application to treasury GET request with transaction details
    :param request:
    :return:
    """
    if request.method == 'GET':
        return redirect_302(re_path='treasury:transaction_details', query_dict=request.GET)
