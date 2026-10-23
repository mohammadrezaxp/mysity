from django.db.models import Q
from django.utils import timezone

from .models import Post


def published_posts():
    return Post.objects.filter(status=True, published_date__lte=timezone.now())


def visible_posts(user):
    if user.is_authenticated and user.is_staff:
        return Post.objects.all()
    published = Q(status=True, published_date__lte=timezone.now())
    if user.is_authenticated:
        return Post.objects.filter(published | Q(auther=user))
    return Post.objects.filter(published, login_re=False)


def public_posts():
    return published_posts().filter(login_re=False)
