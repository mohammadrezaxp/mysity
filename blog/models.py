from django.db import models
from django.utils import timezone
from  django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
class Category(models.Model) :
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name
class Post(models.Model):
    auther = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', default='blog/photo_2025-06-10_23-20-04.jpg')
    counted_views = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    status = models.BooleanField()
    tag = TaggableManager()
    login_re =models.BooleanField(default=False)
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta :
        ordering =['created_date']
        verbose_name= ['select objact']
        verbose_name_plural = 'post'
    def __str__(self):
        return self.title

    def count_comment(self):
        return self.comment.count()

    def get_absolute_url(self):
        return reverse('blog:blog_single', kwargs={'name': self.id})
class Comments(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment')
    name = models.CharField(max_length=225)
    subject = models.CharField(max_length=100)
    message =models.TextField()
    email = models.EmailField()
    creat_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} ({self.email}) - {self.subject} | {self.message[:30]}..."

