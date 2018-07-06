"""luffy_jxblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from users import views as user_view
from article import views as article_view

from django.conf.urls.static import static
urlpatterns = [
    re_path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', user_view.IndexView.as_view(), name='index'),
    path('captcha/', include('captcha.urls')),
    path('summernote/', include('django_summernote.urls')),


    path('login/', user_view.LoginView.as_view(), name='login'),

    path('register/', user_view.RegisterView.as_view(), name='register'),
    path('check_user/', user_view.CheckUserView.as_view(), name='check_user'),

    path('newcaptcha/', user_view.NewCaptchaView.as_view(), name='newcaptcha'),
    path('verify/', user_view.VerifyCaptchaView.as_view(), name='verify'),

    # 用户

    re_path('i/delarticle/(?P<article_id>[0-9]+)/', article_view.ArticleDeleteView.as_view(), name='delarticle'),

    path('i/logout/', user_view.LogoutView.as_view(), name='logout'),
    path('i/newarticle/', article_view.ArticleNewView.as_view(), name='newarticle'),
    path('i/newcategory/', article_view.CategoryNewView.as_view(), name='newcategory'),
    path('i/chkcategory/', article_view.CategoryCheckView.as_view(), name='chkcategory'),
    path('i/allcategory/', article_view.CategoryAllView.as_view(), name='allcategory'),

    re_path('(?P<username>.{6,})/article/(?P<article_id>[0-9]+)/', article_view.ArticleDetailView.as_view(), name='article'),

    re_path('(?P<username>.{6,})/', user_view.HomeView.as_view(), name='home'),

]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)