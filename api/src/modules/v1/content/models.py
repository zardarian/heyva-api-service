from django.db import models

class Content(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    content_reference_id = models.CharField(unique=True, max_length=36, blank=True, null=True)
    content_type = models.ForeignKey('Dictionary', models.DO_NOTHING, db_column='content_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content'