from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("verify/", views.verify_email, name="verify"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("panel/", views.panel, name="panel"),
    path("panel/change-password/", views.change_password, name="change_password"),
    path("panel/delete/", views.delete_account, name="delete_account"),
]
