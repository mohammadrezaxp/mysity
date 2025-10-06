
from django.urls import path
from mysity.views import about , contact
urlpatterns = [
    path('ansur/',about),
    path('jison/',contact)
]
