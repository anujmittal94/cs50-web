
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/<int:user_id>", views.user_page, name = "user_page"),
    path("following", views.following_page, name = "following_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
    path("delete/<int:post_id>", views.delete_post, name="delete_post")
]
