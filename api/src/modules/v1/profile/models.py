from django.db import models

class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    code = models.CharField(unique=True, max_length=18, blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    name_alias = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.ForeignKey('Dictionary', models.DO_NOTHING, db_column='gender', blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    slug_name = models.TextField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    user = models.OneToOneField('User', related_name='profile', on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'