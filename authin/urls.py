#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^unconfirmed/$',views.unconfirmed,name='unconfirmed'),
    url(r'^confirm/(?P<token>.*)$',views.confirm,name='confirm'),
    url(r'^resendemail/$',views.resendemail,name='resendemail')
]
