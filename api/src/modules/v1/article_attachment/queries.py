from django.db.models import Q
from .models import ArticleAttachment

def article_attachment_unused():
    article_attachment = ArticleAttachment.objects.filter(
        article__isnull=True,
        deleted_at__isnull=True,
    )
    
    return article_attachment.order_by('-created_at')

def article_attachment_by_id(id):
    article_attachment = ArticleAttachment.objects.filter(
        id__in=id
    )
    
    return article_attachment

def article_attachment_by_multiple_id(ids):
    article_attachment = ArticleAttachment.objects.filter(
        id__in=ids
    )
    
    return article_attachment.order_by('-created_at')

def article_attachment_by_article_id(article_id):
    return ArticleAttachment.objects.filter(
        article_id=article_id,
        deleted_at__isnull=True,
    )