from django.db import models

# Create your models here.
# 设计博客文章标题和内容的数据模型

class Article(models.Model):
    # 文章ID
    article_id = models.AutoField(primary_key=True) # 设置为主键
    # 文章标题
    title = models.CharField(max_length=32, default='Title')
    # 文章摘要
    brief_content = models.CharField(max_length=256, null=True)
    # 文章内容
    content = models.TextField(null=True)
    # 文章发布日期
    publish_date = models.DateTimeField(auto_now=True) # 设置为自动更新

    def __str__(self): # __str__方法用于返回模型的字符串表示
        return self.title

class Test(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    def __str__(self):
        return self.name
