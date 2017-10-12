#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
class LoginForm(forms.Form):
    user_email = forms.CharField(label="邮箱",max_length=100)
    user_password = forms.CharField(label="密码",widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    user_name=forms.CharField(label="用户名", max_length=50)
    user_email = forms.EmailField(label="邮箱", max_length=100,error_messages={'required':u'请填入邮箱'})
    user_password = forms.CharField(label="密码", widget=forms.PasswordInput())
    user_password2 = forms.CharField(label="重复密码", widget=forms.PasswordInput())

    def clean_user_password2(self):
        cleaned_data = super(RegisterForm, self).clean()
        user_password=cleaned_data['user_password']
        user_password2= cleaned_data['user_password2']
        if user_password2 != user_password:
            raise forms.ValidationError('两次密码不一致')
