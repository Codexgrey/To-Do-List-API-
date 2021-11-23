from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.user_accounts),
    path('account/<int:user_id>', views.user_detail),
    path('account/changepassword', views.change_password)
]