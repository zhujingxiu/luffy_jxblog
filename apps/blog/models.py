from django.db import models
from users.models import UserInfo
# Create your models here.


class Blog(models.Model):
    """
    博客信息 个人站点设置
    """
    title = models.CharField('个人博客标题', max_length=64)
    site_name = models.CharField('站点名称', max_length=64)
    theme = models.CharField('博客主题', max_length=32)
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = verbose_name = '用户博客'
        db_table = 'luf_blog'

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.title)




