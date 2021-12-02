from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist")
    body = models.TextField()
    when = models.CharField(max_length=20, null=True, blank=True)
    day = models.DateField(default=now)
    date = models.DateTimeField(auto_now_add=True)
    # student = models.OneToOneField(Student, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def __str__(self):
        return f'{self.body} for {self.user.username}'
    
    def delete(self):
        self.is_active = False
        self.save()
        return