from . import views
from django.urls import path

app_name = 'basicapp'

urlpatterns = [
        path('index/',views.index, name='index'),
        path('register/',views.register, name='register'),
        path('logout/',views.user_logout,name='logout'),
        path('special/',views.special,name='special'),
        path('user_login/',views.user_login,name='user_login'),
]
