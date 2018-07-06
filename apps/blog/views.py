from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from users.models import UserInfo

# Create your views here.


class Auth(View):
    def dispatch(self, request, *args, **kwargs):

        user_obj = UserInfo.objects.filter(username=request.user.username).first()
        if not user_obj:
            return redirect(reverse("login"))
        return super(Auth, self).dispatch(request, *args, **kwargs)