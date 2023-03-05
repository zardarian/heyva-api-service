from django.db import models
from src.modules.v1.dictionary.models import Dictionary

class Interest(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    profile_code = models.CharField(max_length=18, blank=True, null=True)
    interests = models.ForeignKey(Dictionary, models.DO_NOTHING, db_column='interests', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interest'