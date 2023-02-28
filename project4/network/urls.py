
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("save_changes", views.save_changes, name="save_changes"),
    path("edit/<int:post_id>", views.edit_post, name="edit")


]
