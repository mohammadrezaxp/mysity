from django import template
from blog.models import Post , Category

register = template.Library()

@register.simple_tag(name='po')
def hello():
    posts = Post.objects.filter(status=1).first()
    return posts

@register.filter
def simp(value):
    return value[:10]

@register.inclusion_tag('blog/papularpost.html')
def pap():
    posts = Post.objects.filter(status=1).order_by('published_date')
    return {'posts':posts}

@register.inclusion_tag('blog/post_katagore.html')
def kat():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for cat in categories:
        cat_dict[cat.name] = posts.filter(category=cat).count()

    return {'categories': cat_dict}