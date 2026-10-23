from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="index", permanent=False)),
    path("ref/", include("mysity.urls")),
    path("blog/", include("blog.urls")),
    path("api/", include("api.urls")),
    path("ref/user_manage/", include("user_mangmant.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
