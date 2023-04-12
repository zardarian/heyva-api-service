from django.db import models

class TermsPrivacy(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    type = models.CharField(max_length=36, blank=True, null=True)
    platform = models.CharField(max_length=36, blank=True, null=True)
    version = models.CharField(max_length=36, blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    json_content = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terms_privacy'