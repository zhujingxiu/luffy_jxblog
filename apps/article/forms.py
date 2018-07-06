#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _AUTHOR_  : zhujingxiu
# _DATE_    : 2018/7/5

from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget
from .models import Article, Category, Tag


class ArticleForm(forms.Form):
    '''
    博文表单
    '''
    title = forms.CharField(initial='', min_length=8, label='标题', strip=True, error_messages={'required': '不得为空', 'min_length': '不得少于8个字符'})
    content = forms.CharField(initial='', label='内容', strip=True, widget=SummernoteWidget())

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    is_top = forms.BooleanField()
    is_discuss = forms.BooleanField()


class CategoryForm(forms.Form):
    title = forms.CharField(initial='', min_length=2, label='标题', strip=True,
                            error_messages={'required': '不得为空', 'min_length': '不得少于2个字符'})

    def clean_title(self):
        user_id = self.data.get('user_id')
        number = Category.objects.filter(title=self.cleaned_data.get('title'), blog__user_id=user_id).count()
        if number:
            raise ValidationError('已存在该分类了')
        return self.cleaned_data.get('title')