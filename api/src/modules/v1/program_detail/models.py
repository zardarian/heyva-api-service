from django.db import models

class ProgramDetail(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    program = models.ForeignKey('Program', models.DO_NOTHING, blank=True, null=True)
    content_type = models.CharField(max_length=36, blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    image_content = models.TextField(blank=True, null=True)
    video_content = models.TextField(blank=True, null=True)
    json_content = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'program_detail'