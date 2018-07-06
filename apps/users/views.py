from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, Http404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from article.models import Article
from .models import UserInfo
from .forms import RegisterForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# Create your views here.


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class HomeView(View):

    def get(self, request, username):

        user = UserInfo.objects.get(username=username)
        articles_set = Article.objects.filter(user=user)
        paginator = Paginator(articles_set, 10)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return render(request, 'home/index.html', {'user': user, 'articles': articles})


class LogoutView(View):

    def get(self, request, username):
        print(request)
        logout(request)
        return redirect(reverse('index'))


class LoginView(View):
    '''
    登录认证
    '''

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home', kwargs={'username': username}))

        return render(request, 'login.html', {'msg': '用户名或密码有误'})


class RegisterView(View):
    def get(self, request):

        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'register.html', {'form': RegisterForm(), 'hashkey': hashkey, 'image_url': image_url})

    def post(self, request):

        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = UserInfo.objects.create_user(username=username, password=pwd, email=email)
            return redirect(reverse('login'))
        else:
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)
            return render(request, 'register.html',
                          {'form': form, 'hashkey': hashkey, 'image_url': image_url})


class CheckUserView(View):

    def get(self, request):
        '''
        用户名检查
        :param request:
        :return:
        '''

        username = request.GET.get('username', '')
        query = UserInfo.objects.filter(username=username)
        return HttpResponse('false' if query.count() else 'true')


class NewCaptchaView(View):
    '''
    刷新验证码
    '''

    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return JsonResponse({'hashkey': hashkey, 'image_url': image_url})


class VerifyCaptchaView(View):
    '''
    验证
    '''

    def get(self, request):
        valide = CaptchaStore.objects.filter(response=request.GET['captcha'], hashkey=request.GET['hashkey'])
        return JsonResponse({'status': 1 if valide else 0})
