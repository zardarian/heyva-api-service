from django.db import models

class VideoContentAttachment(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    video_content = models.ForeignKey('VideoContent', models.DO_NOTHING, blank=True, null=True)
    attachment_order = models.BigIntegerField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    attachment_title = models.TextField(blank=True, null=True)
    attachment_length = models.BigIntegerField(blank=True, null=True)
    thumbnail = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'video_content_attachment'
