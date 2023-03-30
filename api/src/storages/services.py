from django.conf import settings
from .locals import local_put_object, local_get_object, local_remove_object
from .aws_s3 import s3_put_object, s3_get_object, s3_remove_object

def put_object(path, file_stream):
    if settings.STORAGE_DRIVER == 'local':
        return local_put_object(path, file_stream)
    elif settings.STORAGE_DRIVER == 's3':
        return s3_put_object(path, file_stream)

def get_object(object_name=None, expires=None):
    if not object_name:
        return object_name
    
    if settings.STORAGE_DRIVER == 'local':
        return local_get_object(object_name)
    elif settings.STORAGE_DRIVER == 's3':
        return s3_get_object(object_name, expires)
    
def remove_object(object_name=None):
    if not object_name:
        return object_name
    
    if settings.STORAGE_DRIVER == 'local':
        return local_remove_object(object_name)
    elif settings.STORAGE_DRIVER == 's3':
        return s3_remove_object(object_name)