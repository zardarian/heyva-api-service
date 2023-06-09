from django.conf import settings
from django.db.models import Q
from .models import Content

def content_active(search, tag, app_env):
    content = Content.objects.filter(
        is_active=True,
        deleted_at__isnull=True
    )

    if search:
        content = content.extra(
            tables=['article', 'video_content', 'program'],
            where=[
                '''
                    (article.id = content.content_reference_id and article.title ilike %s and article.app_env = %s)
                    or (video_content.id = content.content_reference_id and video_content.title ilike %s)
                    or (program.id = content.content_reference_id and program.title ilike %s)
                '''
            ],
            params=[
                "{}{}{}".format('%', search, '%'), app_env,
                "{}{}{}".format('%', search, '%'),
                "{}{}{}".format('%', search, '%')
            ]
        )
    else:
        content = content.extra(
            tables=['article', 'video_content', 'program'],
            where=[
                '''
                    (article.id = content.content_reference_id and article.app_env = %s)
                    or (video_content.id = content.content_reference_id)
                    or (program.id = content.content_reference_id)
                '''
            ],
            params=[
                app_env,
            ]
        )

    if tag:
        content = content.extra(
            tables=['article_tag', 'video_content_tag', 'program_tag'],
            where=[
                '''
                    (article_tag.article_id = content.content_reference_id and article_tag.tag_id = any(%s))
                    or (video_content_tag.video_content_id = content.content_reference_id and video_content_tag.tag_id = any(%s))
                    or (program_tag.program_id = content.content_reference_id and program_tag.tag_id = any(%s))
                '''
            ],
            params=[
                tag,
                tag,
                tag
            ]
        )
    
    return content.distinct('content_reference_id', 'created_at').order_by('-created_at')

def content_by_id(id):
    return Content.objects.filter(
        content_reference_id=id,
        is_active=True,
        deleted_at__isnull=True
    )