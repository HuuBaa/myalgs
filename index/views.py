from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from tools import loginrequired, cookie2user

# Create your views here.


def index(request):
    cookie = request.COOKIES.get('algs', '')
    user = cookie2user(cookie)
    return render(request, 'index/index.html', {'user': user})
