from django.urls import path
from src import views

# modules
from src.modules.v1.user import controllers as user_controller
from src.modules.v1.dictionary import controllers as dictionary_controller

api = 'api'
version = 'v1'

urlpatterns = [
    path("", views.index),

    # User
    path("{}/{}/users/register".format(api, version), user_controller.register),
    path("{}/{}/users/login".format(api, version), user_controller.login),
    path("{}/{}/users/refresh-token".format(api, version), user_controller.refresh_token),
    path("{}/{}/users".format(api, version), user_controller.get_user),

    # Dictionary
    path("{}/{}/dictionary/create".format(api, version), dictionary_controller.create),
    path("{}/{}/dictionary/update/<id>".format(api, version), dictionary_controller.update),
    path("{}/{}/dictionary/delete/<id>".format(api, version), dictionary_controller.delete),
    path("{}/{}/dictionary/activate/<id>".format(api, version), dictionary_controller.activate),
    path("{}/{}/dictionary/deactivate/<id>".format(api, version), dictionary_controller.deactivate),
    path("{}/{}/dictionary/get-by-type".format(api, version), dictionary_controller.read_by_type),
]