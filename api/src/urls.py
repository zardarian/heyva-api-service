from django.urls import path
from src import views

# modules
from src.modules.v1.user import controllers as user_controller
from src.modules.v1.dictionary import controllers as dictionary_controller
from src.modules.v1.role import controllers as role_controller
from src.modules.v1.profile import controllers as profile_controller
from src.modules.v1.article import controllers as article_controller
from src.modules.v1.article_attachment import controllers as article_attachment_controller
from src.modules.v1.video_content import controllers as video_content_controller
from src.modules.v1.video_content_attachment import controllers as video_content_attachment_controller
from src.modules.v1.video_content_personal import controllers as video_content_personal_controller
from src.modules.v1.video_content_attachment_personal import controllers as video_content_attachment_personal_controller
from src.modules.v1.program import controllers as program_controller
from src.modules.v1.program_detail import controllers as program_detail_controller
from src.modules.v1.program_personal import controllers as program_personal_controller
from src.modules.v1.program_personal_tracker import controllers as program_personal_tracker_controller
from src.modules.v1.doctor import controllers as doctor_controller
from src.modules.v1.doctor_appointment import controllers as doctor_appointment_controller
from src.modules.v1.content import controllers as content_controller
from src.modules.v1.tracker_type import controllers as tracker_type_controller
from src.modules.v1.tracker_daily import controllers as tracker_daily_controller
from src.modules.v1.bookmark import controllers as bookmark_controller
from src.modules.v1.terms_privacy import controllers as terms_privacy_controller
from src.modules.v1.terms_privacy_personal import controllers as terms_privacy_personal_controller

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
    path("{}/{}/users/change-password".format(api, version), user_controller.change_password),
    path("{}/{}/users/request-reset-password".format(api, version), user_controller.request_reset_password),
    path("{}/{}/users/reset-password/<id>/<reset_password_token>".format(api, version), user_controller.reset_password),

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

    # Program
    path("{}/{}/program/create".format(api, version), program_controller.create),
    path("{}/{}/program/list".format(api, version), program_controller.read_list),
    path("{}/{}/program/<id>".format(api, version), program_controller.read_by_id),

    # Program Detail
    path("{}/{}/program-detail/create".format(api, version), program_detail_controller.create),

    # Program Personal
    path("{}/{}/program-personal/create".format(api, version), program_personal_controller.create),
    path("{}/{}/program-personal/finish/<program_id>".format(api, version), program_personal_controller.finish_program),

    # Program Personal Tracker
    path("{}/{}/program-personal-tracker/create".format(api, version), program_personal_tracker_controller.create),
    path("{}/{}/program-personal-tracker/finish/<program_id>".format(api, version), program_personal_tracker_controller.finish_program),

    # Doctor
    path("{}/{}/doctor/create".format(api, version), doctor_controller.create),
    path("{}/{}/doctor/list".format(api, version), doctor_controller.read_list),
    path("{}/{}/doctor/<id>".format(api, version), doctor_controller.read_by_id),

    # Doctor Appointment
    path("{}/{}/doctor-appointment/create".format(api, version), doctor_appointment_controller.create),

    # Content
    path("{}/{}/content/list".format(api, version), content_controller.read_list),
    path("{}/{}/content/<id>".format(api, version), content_controller.read_by_id),

    # Tracker Type
    path("{}/{}/tracker-type/list".format(api, version), tracker_type_controller.read_list),

    # Tracker Daily
    path("{}/{}/tracker-daily/create".format(api, version), tracker_daily_controller.create),
    path("{}/{}/tracker-daily/insight".format(api, version), tracker_daily_controller.insight),
    path("{}/{}/tracker-daily/recommendation".format(api, version), tracker_daily_controller.recommendation),

    # Bookmark
    path("{}/{}/bookmark/create".format(api, version), bookmark_controller.create),
    path("{}/{}/bookmark/list".format(api, version), bookmark_controller.read_list),

    # Terms Privacy
    path("{}/{}/terms-privacy/get-by-type".format(api, version), terms_privacy_controller.read_by_type),
    path("{}/{}/terms-privacy/list".format(api, version), terms_privacy_controller.read_list),

    # Terms Privacy Personal
    path("{}/{}/terms-privacy-personal/create".format(api, version), terms_privacy_personal_controller.create),
    path("{}/{}/terms-privacy-personal/create-list".format(api, version), terms_privacy_personal_controller.create_list),
    path("{}/{}/terms-privacy-personal/get-by-type".format(api, version), terms_privacy_personal_controller.read_by_type),
]
