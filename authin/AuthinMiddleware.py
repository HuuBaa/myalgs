#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.http import HttpResponse
from decorators import cookie2user
from django.utils import deprecation


class UnConfirmMiddleware(deprecation.MiddlewareMixin):
    def process_request(self, request):
        cookie = request.COOKIES.get('algs', '')
        user = cookie2user(cookie)
        if request.path == '/auth/logout/':
            return None
        if user is not None and (user.user_confirmed == False):
            return HttpResponse('未确认')
