from time import timezone
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post
from django.utils import timezone
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from .form import CommentForm
from django.contrib import messages
def blog_home (request, cat_name = None,auther_username = None, tag_name = None) :
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by('-published_date')
    if cat_name :
        posts = posts.filter(category__name= cat_name)
    if auther_username :
        posts = posts.filter(auther__username=auther_username)
    if tag_name:
        posts = posts.filter(tags__name=tag_name)
    posts = Paginator(posts,2)
    try:
        page_numb = request.GET.get('page')
        posts = posts.get_page(page_numb)
    except PageNotAnInteger :
        posts = posts.get_page(1)
    except EmptyPage :
        posts = posts.get_page(1)
    context ={'posts':posts}
    return render(request,'blog/blog-home.html',context)
def blog_single (request, name) :
   # post = Post.objects.filter(status=1)
    posts = get_object_or_404(Post,pk = name,status=1)
    posts.counted_views = posts.counted_views +1
    posts.save()
    prev_post = Post.objects.filter(id__lt=posts.id, status=1).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=posts.id, status=1).order_by('id').first()
    context ={'posts':posts,
              'next_post':next_post,
              'prev_post':prev_post

              }
    return render(request,'blog/blog-single.html',context)
def test(request):
    return render(request, 'blog/test.html')

def blog_category(request, cat_name) :
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name= cat_name)
    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)

def blog_search(request) :
    posts = Post.objects.filter(status=1)
    search = request.GET.get('search')
    if search :
        posts = posts.filter(content__icontains=search)
    context ={'posts':posts}
    return render(request,'blog/blog-home.html',context)

def Leave_a_Comments(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            post_id = request.POST.get('post_id')
            comment.post = get_object_or_404(Post, id=post_id)
            comment.save()
            messages.success(request, 'Your comment has been submitted successfully!')
            return redirect('blog:blog_single', name=comment.post.id)
    else:
        form = CommentForm()

    context = {'form': form}
    return render(request, 'blog/blog_comment.html', context)