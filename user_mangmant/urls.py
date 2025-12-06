from django.urls import path
from  .views import  loge_page , logout_page , sing_up_page
app_name = 'User_manage'

urlpatterns =[

    path('login/',loge_page, name = 'login'),
    path('logout/',logout_page, name = 'logout'),
    path('sing_up/',sing_up_page, name = 'sing_up')



]