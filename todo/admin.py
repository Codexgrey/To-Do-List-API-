from django.contrib import admin
from .models import Person, Todo

# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'when']
    list_filter = ['date']
    search_fields = ['title', 'when', 'date']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'today']
    search_fields = ['name', 'today', 'gender']