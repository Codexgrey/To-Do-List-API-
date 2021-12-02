from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.get_user),
    path('user/signup/', views.add_user),
    path('user/login/', views.user_login),
    path('user/profile', views.profile),
    path('user/<uuid:user_id>', views.user_detail),
    path('user/changepassword', views.reset_password)
]