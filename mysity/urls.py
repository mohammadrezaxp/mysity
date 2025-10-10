
from django.urls import path
from mysity.views import  contact , home , about , blog_home , blog_single
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('home/', home, name='index'),
    path('contact/',contact, name = 'contact'),
    path('about/',about,name='about'),
    path('blog_single',blog_single,name='blog_single'),
    path('blog_home/',blog_home,name='blog_home')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)