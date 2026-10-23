from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .form import CommentForm
from .models import Post
from .visibility import visible_posts


def blog_home(request, cat_name=None, auther_username=None, tag_name=None):
    query = (
        visible_posts(request.user)
        .select_related("auther")
        .prefetch_related("category", "tag")
        .order_by("-published_date", "-pk")
    )
    if cat_name:
        query = query.filter(category__name=cat_name)
    if auther_username:
        query = query.filter(auther__username=auther_username)
    if tag_name:
        query = query.filter(tag__name=tag_name)
    search = request.GET.get("search", "").strip()
    if search:
        query = query.filter(Q(title__icontains=search) | Q(content__icontains=search))
    return render(
        request,
        "blog/blog-home.html",
        {"posts": Paginator(query.distinct(), 10).get_page(request.GET.get("page"))},
    )


def blog_single(request, name):
    post = get_object_or_404(visible_posts(request.user), pk=name)
    # Public posts are public; login_re is enforced by the shared visibility policy.
    Post.objects.filter(pk=post.pk).update(counted_views=F("counted_views") + 1)
    post.refresh_from_db(fields=["counted_views"])
    accessible = visible_posts(request.user)
    return render(
        request,
        "blog/blog-single.html",
        {
            "posts": post,
            "prev_post": accessible.filter(pk__lt=post.pk).order_by("-pk").first(),
            "next_post": accessible.filter(pk__gt=post.pk).order_by("pk").first(),
            "form": CommentForm(),
        },
    )


def test(request):
    return render(request, "blog/test.html")


def blog_category(request, cat_name):
    return blog_home(request, cat_name=cat_name)


def blog_search(request):
    return blog_home(request)


@login_required
@require_POST
def Leave_a_Comments(request):
    try:
        post_id = int(request.POST.get("post_id", ""))
    except (TypeError, ValueError):
        raise Http404("Invalid post.")
    post = get_object_or_404(visible_posts(request.user), pk=post_id)
    data = request.POST.copy()
    data["name"] = request.user.get_full_name() or request.user.username
    data["email"] = request.user.email
    form = CommentForm(data)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, "Your comment has been submitted successfully!")
        return redirect("blog:blog_single", name=post.pk)
    return render(
        request, "blog/blog-single.html", {"posts": post, "form": form}, status=400
    )
