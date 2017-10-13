#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from tools import cookie2user
from django.utils import deprecation


class UnConfirmMiddleware(deprecation.MiddlewareMixin):
    def process_request(self, request):
        cookie = request.COOKIES.get('algs', '')
        user = cookie2user(cookie)
        exurls=['/auth/logout/','/auth/login','/auth/register','/auth/unconfirmed/']
        if request.path in exurls or request.path.startswith('/auth/confirm/'):
            return None
        if (user is not None and (user.user_confirmed == False)):
            return  HttpResponseRedirect(reverse('authin:unconfirmed'))

