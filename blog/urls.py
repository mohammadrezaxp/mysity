from django.urls import path

from . import views
from .feeds import LatestEntriesFeed

app_name = "blog"
urlpatterns = [
    path("", views.blog_home, name="blog_home"),
    path("<int:name>/", views.blog_single, name="blog_single"),
    path("category/<str:cat_name>/", views.blog_category, name="blog_category"),
    path("tag/<str:tag_name>/", views.blog_home, name="blog_tag"),
    path("auther/<str:auther_username>/", views.blog_home, name="blog_author"),
    path("search/", views.blog_search, name="blog_search"),
    path("rss/feed/", LatestEntriesFeed(), name="feed"),
    path("comments", views.Leave_a_Comments, name="blog_comment"),
    path("test/", views.test, name="test"),
]
