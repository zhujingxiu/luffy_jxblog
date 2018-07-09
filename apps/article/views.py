from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import View
from django.http import JsonResponse
from django.template.loader import render_to_string
from users.models import UserInfo
from blog.views import Auth
from .models import Article, Category, Tag, Article2Category, Comment
from .forms import ArticleForm, CategoryForm


# Create your views here.
class CategoryAllView(View):
    def get(self, request):
        if request.is_ajax():
            data = Category.objects.filter(blog__user_id=request.user.id)
            data = list(data.values('id', 'title'))

            return JsonResponse(data, safe=False)
        else:
            return render(request, 'home/category.html')


class CategoryCheckView(Auth):
    def get(self, request):
        '''
        分类名称检查
        :param request:
        :return:
        '''

        title = request.GET.get('title', '')
        query = Category.objects.filter(title=title, blog__user=request.user.id)

        return HttpResponse('false' if query.count() else 'true')


class CategoryNewView(Auth, View):
    '''
    添加分类
    '''

    def get(self, request):
        title = '添加分类'
        form = CategoryForm()
        return JsonResponse(
            {'title': title, 'content': render_to_string('home/category.html', {'form': form}, request=request)})

    def post(self, request):
        data = dict(request.POST)
        data.update({'user_id': request.user.id})
        form = CategoryForm(data)
        if form.is_valid():
            print(form.cleaned_data)
            Category.objects.create(title=request.POST.get('title'), blog_id=request.user.id)
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 0, 'msg': form.errors})


class ArticleNewView(Auth, View):
    '''
    添加文章
    '''

    def get(self, request):
        return render(request, 'home/article.html', {'title': '添加文章','form': ArticleForm()})

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article.objects.create(user=request.user, title=form.cleaned_data.get('title'),
                                             content=form.cleaned_data.get('content'),
                                             is_top=form.cleaned_data.get('is_top'),
                                             is_discuss=form.cleaned_data.get('is_discuss'))
            print(form.cleaned_data)
            for _category in form.cleaned_data.get('category'):
                Article2Category.objects.create(article=article, category=_category)
            for i in form.cleaned_data.get('tag','').split('|'):
                print(i)
            return redirect(reverse('home', kwargs={'username': request.user.username}))
        else:
            print(form.errors)
            return render(request, 'home/article.html', {'form': form})


class ArticleDetailView(View):
    '''
    文章详情
    '''

    def get(self, request, username, article_id):
        user = UserInfo.objects.filter(username=username).first()
        blog = user.blog

        article = Article.objects.filter(pk=article_id).first()
        comments = Comment.objects.filter(article_id=article_id)
        return render(request, 'home/detail.html', {'article': article, 'comments': comments})


class ArticleDeleteView(View):
    '''
    删除文章
    '''

    def get(self, request, username, article_id):
        return render(request, 'home/article.html')
