from django.db import models
from blog.models import Blog
from users.models import UserInfo
# Create your models here.


class Category(models.Model):
    """
    博主个人文章分类表
    """
    title = models.CharField('分类标题', max_length=32)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所属博客')

    class Meta:
        verbose_name_plural = verbose_name = '博主个人文章分类'
        db_table = 'luf_category'

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    博主个人文章标签
    """
    title = models.CharField('标签名称', max_length=32)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='所属博客')

    class Meta:
        verbose_name_plural = verbose_name = '博主个人文章标签'
        db_table = 'luf_tag'

    def __str__(self):
        return self.title


class Article(models.Model):
    '''
    博主文章
    '''
    title = models.CharField('文章标题', max_length=64)
    desc = models.CharField('文章描述', max_length=256)
    content = models.TextField()

    comments = models.IntegerField('评论数', default=0)
    likes = models.IntegerField('点赞数', default=0)
    dislikes = models.IntegerField('反对数', default=0)

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='作者')
    category = models.ManyToManyField(Category, through='Article2Category', through_fields=('article', 'category'), related_name='categories', verbose_name='文章分类')
    tag = models.ManyToManyField(Tag, through='Article2Tag', through_fields=('article', 'tag'), related_name='tags', verbose_name='文章标签')

    status = models.BooleanField('是否发布', default=False)
    is_top = models.BooleanField('置顶', default=False)
    is_discuss = models.BooleanField('可否评论', default=True)
    add_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = '博主文章'
        db_table = 'luf_article'

    def __str__(self):
        return self.title


class Article2Category(models.Model):
    '''
    文章标签映射表
    '''
    article = models.ForeignKey("Article", on_delete=models.CASCADE, verbose_name='文章')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name='分类')

    class Meta:
        verbose_name_plural = verbose_name = '文章分类映射表'
        db_table = 'luf_article_category'
        unique_together = [
            ('article', 'category'),
        ]

    def __str__(self):
        return "{0}[{1}]".format(self.article.title, self.category.title)

class Article2Tag(models.Model):
    '''
    文章标签映射表
    '''
    article = models.ForeignKey("Article", on_delete=models.CASCADE, verbose_name='文章')
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, verbose_name='标签')

    class Meta:
        verbose_name_plural = verbose_name = '文章标签映射表'
        db_table = 'luf_article_tag'
        unique_together = [
            ('article', 'tag'),
        ]

    def __str__(self):
        return "{0}[{1}]".format(self.article.title, self.tag.title)


class ArticleLike(models.Model):
    """
    文章的赞成或反对记录
    """

    user = models.ForeignKey(UserInfo, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    is_like = models.BooleanField('是否赞成', default=True)

    class Meta:
        verbose_name_plural = verbose_name = '博主个人文章标签'
        db_table = 'luf_article_like'
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):
    """
    文章评论表
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='评论文章')
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.CharField('评论内容', max_length=256)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = verbose_name = '博主个人文章标签'
        db_table = 'luf_comment'

    def __str__(self):
        return self.content