from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("list/", views.BoardListView.as_view(), name="board_list"),
    path("write/", views.BoardWriteView.as_view(), name="board_write"),
    path("detail/<int:pk>/", views.BoardDetailView.as_view(), name="board_detail"),
    path("delete/<int:pk>/", views.BoardDeleteView.as_view(), name="board_delete"),
    path("update/<int:pk>/", views.BoardUpdateView.as_view(), name="board_update"),
    path("like/<int:pk>/", views.LikesView.as_view(), name="board_like"),
    path("comment/write", views.CommentWriteView.as_view(), name="comment_write"),
    path("comment/delete/<int:pk>", views.CommentDeleteView.as_view(), name="comment_delete"),
]
