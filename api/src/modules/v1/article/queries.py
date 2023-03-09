from django.db.models import Q
from .models import Article

def article_active(search, tag):
    article = Article.objects.filter(
        is_active=True,
        deleted_at__isnull=True
    )

    if search:
        article = article.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        )

    if tag:
        article = article.filter(
            article_tag__tag__in=tag
        )
    
    return article.distinct('id', 'created_at').order_by('-created_at')

def article_by_id(id):
    return Article.objects.filter(
        id=id,
        is_active=True,
        deleted_at__isnull=True,
    )