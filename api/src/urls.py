from django.urls import path
from src import views

# modules
from src.modules.v1.user import controllers as user_controller
from src.modules.v1.dictionary import controllers as dictionary_controller
from src.modules.v1.role import controllers as role_controller
from src.modules.v1.profile import controllers as profile_controller
from src.modules.v1.article import controllers as article_controller
from src.modules.v1.article_attachment import controllers as article_attachment_controller
from src.modules.v1.mood_tracker import controllers as mood_tracker_controller
from src.modules.v1.video_content import controllers as video_content_controller
from src.modules.v1.video_content_attachment import controllers as video_content_attachment_controller
from src.modules.v1.video_content_personal import controllers as video_content_personal_controller
from src.modules.v1.video_content_attachment_personal import controllers as video_content_attachment_personal_controller

api = 'api'
version = 'v1'

urlpatterns = [
    path("", views.index),

    # User
    path("{}/{}/users/register".format(api, version), user_controller.register),
    path("{}/{}/users/verification/<id>/<registration_token>".format(api, version), user_controller.verification),
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

    # Role
    path("{}/{}/role/update/<user_id>".format(api, version), role_controller.update),

    # Profile
    path("{}/{}/profile".format(api, version), profile_controller.get_profile),
    path("{}/{}/profile/update".format(api, version), profile_controller.update),

    # Article
    path("{}/{}/article/create".format(api, version), article_controller.create),
    path("{}/{}/article/list".format(api, version), article_controller.read_list),
    path("{}/{}/article/<id>".format(api, version), article_controller.read_by_id),

    # Article Attachment
    path("{}/{}/article-attachment/create".format(api, version), article_attachment_controller.create),
    path("{}/{}/article-attachment/get-unused".format(api, version), article_attachment_controller.read_unused),

    # Mood Tracker
    path("{}/{}/mood-tracker/create".format(api, version), mood_tracker_controller.create),
    path("{}/{}/mood-tracker/list".format(api, version), mood_tracker_controller.read_list),
    path("{}/{}/mood-tracker/private-list".format(api, version), mood_tracker_controller.read_list_by_auth),

    # Video Content
    path("{}/{}/video-content/create".format(api, version), video_content_controller.create),
    path("{}/{}/video-content/list".format(api, version), video_content_controller.read_list),
    path("{}/{}/video-content/<id>".format(api, version), video_content_controller.read_by_id),

    # Video Content Attachment
    path("{}/{}/video-content-attachment/create".format(api, version), video_content_attachment_controller.create),
    path("{}/{}/video-content-attachment/get-unused".format(api, version), video_content_attachment_controller.read_unused),

    # Video Content Personal
    path("{}/{}/video-content-personal/create".format(api, version), video_content_personal_controller.create),

    # Video Content Attachment Personal
    path("{}/{}/video-content-attachment-personal/create".format(api, version), video_content_attachment_personal_controller.create),
]
