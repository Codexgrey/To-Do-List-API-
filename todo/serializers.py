from rest_framework import serializers
from .models import Person, Todo


class PersonSerializer(serializers.ModelSerializer):
    all_todo = serializers.ReadOnlyField()
    class Meta:
        model = Person
        fields = [  #'__all__'#
            "id",   
            "name",
            "gender",
            "dob",
            "today",
            "all_todo"                     
        ]        


class TodoSerializer(serializers.ModelSerializer):
    person_name = serializers.ReadOnlyField()
    class Meta:
        model = Todo                       
        fields = [
            "id",
            "title",
            "person",
            "person_name",
            "body", 
            "when",                      
            "today",
            "date"
        ]