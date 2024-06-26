from django.db import models

class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    creator = models.TextField(blank=True, null=True)
    banner = models.TextField(blank=True, null=True)
    thumbnail = models.TextField(blank=True, null=True)
    app_env = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'article'