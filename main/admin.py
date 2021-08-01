from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(ToDo)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("todo", "user")


@admin.register(NoteBook)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("notebook_name", "user")
