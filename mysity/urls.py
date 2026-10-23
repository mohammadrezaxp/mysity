from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blog.sitemaps import BlogSitemap
from mysity.sitemaps import StaticViewSitemap
from mysity.views import about, contact, home, news

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
}
urlpatterns = [
    path("home/", home, name="index"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path("news/", news, name="news"),
    path("robots.txt", include("robots.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("captcha/", include("captcha.urls")),
    path("user_mange/", include("user_mangmant.urls", namespace="LegacyUserManage")),
    # path('sing_up/',include('user_mangmant.urls', namespace='LegacyUserManage')),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
