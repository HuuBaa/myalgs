from django.shortcuts import render, reverse
from . import forms
from django.http import HttpResponseRedirect
from .models import User
import hashlib
from decorators import loginrequired
from myalgs.settings import SECRET_KEY


def setcookie(response, user_id, user_email, user_pass_hash, secret_key):
    s = '%s-%s-%s' % (user_email, user_pass_hash, secret_key)
    s = hashlib.sha1(s.encode()).hexdigest()
    L = ['UID:' + str(user_id), s]
    cookie = '-'.join(L)
    response.set_cookie('algs', cookie, 60)
    return response

# Create your views here.


def login(request):
    if request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            next=form.data['next']
            user_email = form.cleaned_data['user_email'].encode('utf-8')
            user_password = form.cleaned_data['user_password'].encode('utf-8')
            user_pass_hash = hashlib.sha1(
                user_email + user_password).hexdigest()
            u = User.objects.filter(user_email=user_email)[0]
            if user_pass_hash == u.user_pass_hash:
                response = HttpResponseRedirect(next)
                response = setcookie(
                    response,
                    u.id,
                    u.user_email,
                    u.user_pass_hash,
                    SECRET_KEY)
                return response
            else:
                return HttpResponseRedirect(reverse('index:index'))
    else:
        form = forms.LoginForm()
    next=request.GET.get('next','/')
    return render(request, 'auth/login.html', {'form': form,'next':next})


def register(request):

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name'].encode('utf-8')
            user_email = form.cleaned_data['user_email'].encode('utf-8')
            user_password = form.cleaned_data['user_password'].encode('utf-8')
            user_pass_hash = hashlib.sha1(
                user_email + user_password).hexdigest()
            u = User.objects.create(
                user_name=user_name,
                user_email=user_email,
                user_pass_hash=user_pass_hash)
            u.save()
            return HttpResponseRedirect(reverse('authin:login'))
    else:
        form = forms.RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@loginrequired
def logout(requset, **kw):
    response = HttpResponseRedirect(reverse('index:index'))
    response.delete_cookie('algs')
    return response
