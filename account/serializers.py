from rest_framework import serializers
from django.contrib.auth import get_user_model
# from .models import CustomUser

# Best Practice; so whenever you change User model name, 
#   - you don't have to do so everywhere just in settings at AUTH_USER_MODEL
# from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = User
        fields = [ #'__all__'
            "id",
            "username", 
            "first_name", 
            "last_name", 
            "email",  
            "password", 
            "is_active",
            "address", 
            "date_joined"
        ]

# since we aren't using ModelSerializer, we create our own fields
class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=500)
    new_password = serializers.CharField(max_length=500)
    re_password = serializers.CharField(max_length=500)
 
    def validate_newpassword(self, value):
        if value != self.initial_data['re_password']:
            raise serializers.ValidationError("Please enter matching passwords")
        else:
            return value




