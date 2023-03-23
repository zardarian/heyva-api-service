from django.db import models

class MoodTracker(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    profile_code = models.ForeignKey('Profile', models.DO_NOTHING, db_column='profile_code', to_field='code', blank=True, null=True)
    mood_feel = models.TextField(blank=True, null=True)
    mood_source = models.TextField(blank=True, null=True)
    more = models.TextField(blank=True, null=True)
    mood_value = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mood_tracker'