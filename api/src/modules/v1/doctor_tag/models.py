from django.db import models

class DoctorTag(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    doctor = models.ForeignKey('Doctor', models.DO_NOTHING, blank=True, null=True, related_name='doctor_tag')
    tag = models.ForeignKey('Dictionary', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_tag'