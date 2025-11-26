from django.contrib.sitemaps.views import sitemap
from django.urls import path , include
from blog.sitemaps import BlogSitemap
from mysity.views import  contact , home , about , news
from django.conf import settings
from django.conf.urls.static import static
from mysity.sitemaps import StaticViewSitemap
sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
}
urlpatterns = [
    path('home/', home, name='index'),
    path('contact/',contact, name = 'contact'),
    path('about/',about,name='about'),
    path('news/',news,name='news'),
    path('__debug__/',include('debug_toolbar.urls')),
    path('robots.txt', include('robots.urls')),
    path('summernote/',include('django_summernote.urls')),
    path('captcha/',include('captcha.urls')),
    path('user_mange/',include('user_mangmant.urls')) ,
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)