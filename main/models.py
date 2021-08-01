from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class ToDo(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    todo = models.CharField(max_length=500)
    created = models.DateField(auto_now_add=True)


class NoteBook(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='+')
    notebook_name = models.CharField(max_length=500)
    notebook_content = models.TextField()
    created = models.DateField(auto_now_add=True)
