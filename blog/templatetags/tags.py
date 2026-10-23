from django import template

from blog.models import Category
from blog.visibility import public_posts

register = template.Library()


@register.simple_tag(name="po")
def hello():
    posts = public_posts().first()
    return posts


@register.filter
def simp(value):
    return value[:10]


@register.inclusion_tag("blog/papularpost.html")
def pap():
    posts = public_posts().order_by("published_date")
    return {"posts": posts}


@register.inclusion_tag("blog/post_katagore.html")
def kat():
    posts = public_posts()
    categories = Category.objects.all()
    cat_dict = {}
    for cat in categories:
        cat_dict[cat.name] = posts.filter(category=cat).count()

    return {"categories": cat_dict}
