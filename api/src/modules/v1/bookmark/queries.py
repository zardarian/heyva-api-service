from django.db.models import Q
from .models import Bookmark

def bookmark_active(search, tag, profile_code):
    bookmark = Bookmark.objects.filter(
        profile_code=profile_code,
        deleted_at__isnull=True
    )

    if search:
        bookmark = bookmark.extra(
            tables=['article', 'video_content', 'program'],
            where=[
                '''
                    (article.id = bookmark.content_reference_id and article.title ilike %s)
                    or (video_content.id = bookmark.content_reference_id and video_content.title ilike %s)
                    or (program.id = bookmark.content_reference_id and program.title ilike %s)
                '''
            ],
            params=[
                "{}{}{}".format('%', search, '%'),
                "{}{}{}".format('%', search, '%'),
                "{}{}{}".format('%', search, '%')
            ]
        )

    if tag:
        bookmark = bookmark.extra(
            tables=['article_tag', 'video_content_tag', 'program_tag'],
            where=[
                '''
                    (article_tag.article_id = bookmark.content_reference_id and article_tag.tag_id = any(%s))
                    or (video_content_tag.video_content_id = bookmark.content_reference_id and video_content_tag.tag_id = any(%s))
                    or (program_tag.program_id = bookmark.content_reference_id and program_tag.tag_id = any(%s))
                '''
            ],
            params=[
                tag,
                tag,
                tag
            ]
        )
    
    return bookmark.distinct('content_reference_id', 'created_at').order_by('-created_at')