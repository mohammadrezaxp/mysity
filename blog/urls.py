from django.urls import path
from blog.views import   blog_home , blog_single , test , blog_category ,blog_search , Leave_a_Comments
from django.conf import settings
from django.conf.urls.static import static
from blog.feeds import LatestEntriesFeed
app_name = 'blog'
urlpatterns = [

    path('', blog_home, name='blog_home'),
    path('<int:name>/', blog_single, name='blog_single'),
    path('category/<str:cat_name>/', blog_category, name='blog_category'),
    path('tag/<str:tag_name>/', blog_home, name='blog_tag'),
    path('auther/<str:auther_username>/', blog_home, name='blog_author'),
    path('search/',blog_search, name='blog_search') ,
    path("rss/feed/", LatestEntriesFeed()),
    path('comments',Leave_a_Comments,name='blog_comment'),
    path('test/', test, name='test')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)