from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100,default=1)
    created_date = models.DateTimeField(default=1)


class Todo(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(default='')
