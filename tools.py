#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from authin.models import User
import hashlib
from myalgs.settings import SECRET_KEY
from django.core.mail import send_mail



def setcookie(response, user_id, user_email, user_pass_hash, secret_key):
    s = '%s-%s-%s' % (user_email, user_pass_hash, secret_key)
    s = hashlib.sha1(s.encode()).hexdigest()
    L = ['UID:' + str(user_id), s]
    cookie = '-'.join(L)
    response.set_cookie('algs', cookie, 60)
    return response


def cookie2user(cookie):
    try:
        uid = cookie.split('-')[0].split(':')[1]
        u = User.objects.filter(id=int(uid))[0]
        s = '%s-%s-%s' % (u.user_email, u.user_pass_hash, SECRET_KEY)
        s = hashlib.sha1(s.encode()).hexdigest()
        if cookie.split('-')[1] == s:
            user = u
        else:
            user = None
    except Exception:
        user = None
    return user


# 使用了这个装饰器的view，可以从kw['user']获取到user

def loginrequired(func):
    def decofunc(request,*args,**kw):
        cookie = request.COOKIES.get('algs', '')
        user = cookie2user(cookie)
        if user is not None:
            return func(request, user=user,*args,**kw)
        else:
            return HttpResponseRedirect(reverse('authin:login'))
    return decofunc


def send_email_new(subject,body,from_email,*to_emails):
    try:
        send_mail(subject, body, from_email,
              to_emails, fail_silently=False)
    except:
        pass