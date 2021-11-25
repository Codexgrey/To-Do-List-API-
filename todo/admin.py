from django.contrib import admin
from .models import Todo

# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'when', 'day']
    list_filter = ['date']
    search_fields = ['title', 'when', 'day',]
