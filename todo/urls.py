from django.urls import path
from . import views

urlpatterns = [
    path('persons/', views.persons), # students
    path('persons/<int:person_id>', views.person_detail),
    path('todolist/', views.todolist), # books
    path('todolist/<int:todo_id>', views.todo_detail),
    path('today/', views.list_today),
]
