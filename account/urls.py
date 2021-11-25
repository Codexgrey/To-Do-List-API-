from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.get_user),
    path('account/signup/', views.add_user),
    path('account/login/', views.user_login),
    path('account/profile', views.profile),
    path('account/<uuid:user_id>', views.user_detail),
    path('account/changepassword', views.reset_password)
]