from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
class Task(models.Model):
        PRIORITY_CHOICES=[
             ('low','LOW'),
             ('medium','MEDIUM'),
             ('high','HIGH')
        ]

        title=models.CharField(max_length=100)
        description=models.TextField()
        priority=models.CharField(max_length=50,choices=PRIORITY_CHOICES)
        category=models.ForeignKey(Category,on_delete=models.CASCADE)
        due_date=models.DateTimeField(null=True,blank=True)
        completed=models.BooleanField(default=True)
        user=models.ForeignKey(User,on_delete=models.CASCADE)

        def __str__(self) -> str:
             return self.title