from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.home, name='home'),
    path('regist', views.regist, name='regist'),
    path('activate/<str:token>/', views.activate_user, name='activate_user'),
    path('user_login', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('mypage/<int:user_id>/', views.mypage, name='mypage'),  # 修正
    path('mypage_edit/', views.mypage_edit, name='mypage_edit'),
]
