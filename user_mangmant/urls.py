from django.urls import path
from  .views import  loge_page , logout_page , regster_page
app_name = 'User_manage'

urlpatterns =[

    path('login/',loge_page, name = 'login'),
    path('logout/',logout_page, name = 'logout'),
    path('regster/',regster_page , name = 'regster')



]