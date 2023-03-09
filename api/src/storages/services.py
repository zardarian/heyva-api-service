from django.conf import settings
from .locals import local_put_object, local_get_object, local_remove_object

def put_object(path, file_stream):
    if settings.STORAGE_DRIVER == 'local':
        return local_put_object(path, file_stream)

def get_object(object_name=None, expires = 1):
    if settings.STORAGE_DRIVER == 'local':
        return local_get_object(object_name)
    
def remove_object(object_name=None):
    if settings.STORAGE_DRIVER == 'local':
        return local_remove_object(object_name)