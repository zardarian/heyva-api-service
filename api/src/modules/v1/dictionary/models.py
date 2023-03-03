from django.db import models

class Dictionary(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    type = models.CharField(max_length=18)
    name = models.TextField()
    parent = models.CharField(max_length=36, blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'dictionary'