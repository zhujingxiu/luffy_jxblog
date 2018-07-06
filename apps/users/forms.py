#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/7/2

from django import forms
from .models import UserInfo
from django.core.exceptions import ValidationError

from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    username = forms.CharField(initial='', min_length=8, label='账号', strip=True,
                               error_messages={'required': '不得为空', 'min_length': '不得少于8个字符'})
    password = forms.CharField(initial='', min_length=6, label='密码', strip=True,
                               error_messages={'required': '不得为空', 'min_length': '不得少于6个字符'})
    confirm = forms.CharField(initial='', min_length=6, label='确认密码', strip=True,
                              error_messages={'required': '不得为空', 'min_length': '不得少于6个字符'})
    email = forms.CharField(initial='', label='邮箱', strip=True,
                            error_messages={'required': '不得为空', 'min_length': '不得少于8个字符'})
    captcha = CaptchaField(initial='', label='验证码', error_messages={'required': '不得为空', "invalid": u"验证码错误"})

    def clean_user(self):
        username = self.cleaned_data.get('username')
        users = UserInfo.objects.filter(username=username).count()
        if users:
            raise ValidationError('该用户已存在')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = UserInfo.objects.filter(email=email).count()
        if users:
            raise ValidationError('该邮箱已存在')
        else:
            return email

    def clean_confirm(self):
        pwd = self.cleaned_data.get('password', '')
        confirm = self.cleaned_data.get('confirm', '')
        if pwd and pwd != confirm:
            raise ValidationError('两次密码输入不一致')
        return confirm

    # def clean_captcha(self):
    #     print('*'*80)
    #     print(self.cleaned_data)
    #     captcha = self.cleaned_data.get('captcha', '')
    #     print(captcha)
    #     valide = CaptchaStore.objects.filter(response=captcha[1], hashkey=captcha[0])
    #     if valide:
    #          return captcha[1]
    #     else:
    #          raise ValidationError('验证码错误')
