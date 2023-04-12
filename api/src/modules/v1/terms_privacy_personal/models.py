from django.db import models

class TermsPrivacyPersonal(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    profile_code = models.ForeignKey('Profile', models.DO_NOTHING, db_column='profile_code', to_field='code', blank=True, null=True)
    terms_privacy = models.ForeignKey('TermsPrivacy', models.DO_NOTHING, blank=True, null=True)
    is_agree = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terms_privacy_personal'