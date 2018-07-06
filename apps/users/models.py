from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ("unknown", u"保密"),
        ("male", u"男"),
        ("female", u"女")
    )
    gender = models.CharField("性别", max_length=8, choices=GENDER_CHOICES, default="unknown")
    birthday = models.DateField("出生年月", null=True, blank=True)
    mobile = models.CharField('联系电话', max_length=16, null=True, unique=True)
    email = models.EmailField("邮箱", max_length=128, null=True, blank=True)
    avatar = models.FileField(upload_to='avatar/', default="avatar/default.png", verbose_name='头像')
    add_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = '用户信息'
        db_table = 'luf_users'

    def __str__(self):
        return self.username