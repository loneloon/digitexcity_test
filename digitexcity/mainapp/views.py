from django.shortcuts import render
from patterns.reused_funcs import gather_balances


# also nothing to write home about

def index(request):

    content = {
        'page_title': 'Home'
    }
    gather_balances()
    return render(request, 'mainapp/index.html', content)

