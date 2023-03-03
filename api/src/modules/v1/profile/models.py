from django.db import models

class Profile(models.Model):
    id = models.CharField(max_length=36, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=36, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=36, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=36, blank=True, null=True)
    code = models.CharField(max_length=18, blank=True, null=True)
    full_name = models.TextField(blank=True, null=True)
    name_alias = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=36, blank=True, null=True)
    avatar = models.TextField(blank=True, null=True)
    slug_name = models.TextField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'