from django.db import models

class TrackerDetail(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    tracker_type = models.ForeignKey('TrackerType', models.DO_NOTHING, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=36, blank=True, null=True)
    json_content = models.JSONField(blank=True, null=True)
    order = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tracker_detail'