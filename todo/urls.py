from django.urls import path
from . import views

urlpatterns = [
    path('todolist/', views.todolist), # books
    path('todolist/<int:todo_id>', views.todo_detail),
    path('todos/mark_complete/<int:todo_id>', views.mark_complete),
    path('todos/today/', views.list_today),
    path('todos/anyfuturedate/', views.list_future),
]
