from django.shortcuts import render, reverse
from . import forms
from django.http import HttpResponseRedirect,HttpResponse
from .models import User
import hashlib
from tools import loginrequired,cookie2user,send_email_new,setcookie
from myalgs.settings import SECRET_KEY
from django.contrib import  messages


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
            confirm_token = u.generate_confirm_token()
            confirm_url = 'http://127.0.0.1'+reverse('authin:confirm', args=[confirm_token])
            send_email_new('确认', confirm_url, '742790905@qq.com', u.user_email)
            return HttpResponseRedirect(reverse('authin:login'))
    else:
        form = forms.RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@loginrequired
def logout(requset, **kw):
    response = HttpResponseRedirect(reverse('index:index'))
    response.delete_cookie('algs')
    return response

@loginrequired
def unconfirmed(request,**kw):
    return render(request,'auth/unconfirmed.html')

@loginrequired
def confirm(request,token,**kw):
    user=kw.get('user')
    confirm_status=user.email_confirm(token)
    if confirm_status == False:
        return HttpResponse('无效的token')
        # return HttpResponseRedirect(reverse('index:index'))
    return HttpResponse(confirm_status)


@loginrequired
def resendemail(request,**kw):
    user=kw.get('user')
    confirm_token = user.generate_confirm_token()
    confirm_url = 'http://127.0.0.1' + reverse('authin:confirm', args=[confirm_token])
    send_email_new('确认', confirm_url, '742790905@qq.com', user.user_email)
    messages.info(request,'已经重新发送')
    return HttpResponseRedirect(reverse('index:index'))