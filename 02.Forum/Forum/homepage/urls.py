from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("post/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path(
        "post/<int:pk>/comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),
]
