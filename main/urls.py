from django.urls import path
from . import views

todo = views.ToDo()
notebook = views.NoteBook()
wikipedia = views.Wikipedia()
dictionary = views.Dictionary()
youtube = views.Youtube()
translate = views.Translate()

urlpatterns = [
    path("", views.home, name="index"),
    path("todo-list/", todo.todo, name="todo-list"),
    path("todo/edit/<int:todo_id>/", todo.edit_todo, name="edit-todo"),
    path("todo/done/<int:todo_id>/", todo.delete_todo, name="delete-todo"),
    path("notebook/", notebook.notebook, name="notebook"),
    path("notebook/edit/<int:notebook_id>/", notebook.edit_notebook, name="edit-notebook"),
    path("notebook/done/<int:notebook_id>/", notebook.delete_notebook, name="delete-notebook"),
    path("wikipedia/", wikipedia.wikipedia, name="wikipedia"),
    path("dictionary/", dictionary.dictionary, name="dictionary"),
    path("youtube/", youtube.youtube, name="youtube"),
    path("youtube/video/<str:video_id>/", youtube.show_youtube_video, name="show_youtube_video"),
    path("translate/", translate.translate, name="translate"),
]
