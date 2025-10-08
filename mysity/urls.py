
from django.urls import path
from mysity.views import about , contact
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('ansur/',about),
    path('jison/',contact)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)