from django.conf import settings
from datetime import datetime
import pathlib
import os

now = datetime.now()

def local_put_object(path, file_stream):
    attributes = file_stream.name.split('.')
    file_name = "{}-{}".format(str(now.strftime("%Y%m%d%H%M")), attributes[0]) + '.' + attributes[-1]
    file_path = path + '/' + file_name

    pathlib.Path(settings.MEDIA_ROOT + '/' + path).mkdir(parents=True, exist_ok=True)
    with open(settings.MEDIA_ROOT + '/' + file_path, 'wb+') as destination:
        for chunk in file_stream.chunks():
            destination.write(chunk)

    return file_path

def local_get_object(object_name=None):
    data = settings.BASE_URL + settings.MEDIA_URL + object_name

    return data

def local_remove_object(object_name=None):
    os.remove(settings.MEDIA_ROOT + '/' +object_name)