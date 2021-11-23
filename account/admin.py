from django.contrib import admin

# this finds the User model currently used by this app
from django.contrib.auth import get_user_model

# Register your models here.
User = get_user_model()
admin.site.register(User)
