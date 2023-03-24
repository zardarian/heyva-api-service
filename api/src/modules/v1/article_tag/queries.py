from django.db.models import Q
from .models import ArticleTag

def article_tag_by_article_id(article_id):
    return ArticleTag.objects.filter(
        article=article_id,
        deleted_at__isnull=True,
    )