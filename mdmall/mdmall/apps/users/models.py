from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser

from mdmall.utils.db import BaseModel





class User(AbstractUser, BaseModel):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:  # 配置数据库表名,及设置模型在admin站点显示的中文名
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
