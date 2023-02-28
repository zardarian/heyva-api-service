from django.urls import path
from src import views

# modules
from src.modules.v1.user import controllers as user_controller

api = 'api'
version = 'v1'

urlpatterns = [
    path("", views.index),

    # User
    path("{}/{}/users/register".format(api, version), user_controller.register),
    path("{}/{}/users/login".format(api, version), user_controller.login),
    path("{}/{}/users/refresh-token".format(api, version), user_controller.refresh_token),
    path("{}/{}/users".format(api, version), user_controller.get_user),
]