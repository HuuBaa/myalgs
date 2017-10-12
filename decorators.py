#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from authin.models import User
import hashlib
from myalgs.settings import SECRET_KEY


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
    def decofunc(request, **kw):
        cookie = request.COOKIES.get('algs', '')
        user = cookie2user(cookie)
        if user is not None:
            return func(request, user=user)
        else:
            return HttpResponseRedirect(reverse('authin:login'))
    return decofunc
