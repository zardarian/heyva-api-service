from django.db import models
from src.modules.v1.dictionary.models import Dictionary

class Pregnancy(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    profile_code = models.ForeignKey('Profile', models.DO_NOTHING, db_column='profile_code', to_field='code', blank=True, null=True)
    status = models.ForeignKey(Dictionary, models.DO_NOTHING, db_column='status', blank=True, null=True)
    estimated_due_date = models.DateField(blank=True, null=True)
    child_birth_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pregnancy'