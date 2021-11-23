from django.db import models
from django.utils import timezone


# Create your models here.
def get_today():
    currtime = timezone.now()
    today = currtime.strftime("%d-%m-%Y")   
    return today  

class Person(models.Model):
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=15)
    dob = models.CharField(max_length=24)
    today = models.CharField(max_length=25, default=get_today())
    # date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def all_todo(self):
        return self.todolist.all().values()


class Todo(models.Model):
    title = models.CharField(max_length=300)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="todolist")
    body = models.TextField()
    when = models.CharField(max_length=20)
    today = models.CharField(max_length=25, default=get_today())
    date = models.DateTimeField(auto_now_add=True)
    # student = models.OneToOneField(Student, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    @property
    def person_name(self):
        return self.person.name