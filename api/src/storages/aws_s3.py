from django.conf import settings
from datetime import datetime
import boto3
import tempfile
import os

now = datetime.now()

def s3_get_object(object_name=None, expires=None):
    s3 = boto3.client(
        settings.STORAGE_DRIVER,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    if not expires:
        return "{}{}{}{}{}{}{}{}{}".format('https://', settings.AWS_STORAGE_BUCKET_NAME, '.', settings.STORAGE_DRIVER, '.', settings.AWS_S3_REGION_NAME, '.', 'amazonaws.com/', object_name)
    else:
        return s3.generate_presigned_url('get_object', Params={'Bucket' : settings.AWS_STORAGE_BUCKET_NAME, 'Key' : object_name}, ExpiresIn=expires)

def s3_remove_object(object_name=None):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=object_name)

def s3_put_object(path, file_stream):
    attributes = file_stream.name.split('.')
    file_name = "{}-{}".format(str(now.strftime("%Y%m%d%H%M")), attributes[0]) + '.' + attributes[-1]
    file_path = path + '/' + file_name

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    with open(tempfile.gettempdir() + '/' + file_name, 'wb+') as destination:
        for chunk in file_stream.chunks():
            destination.write(chunk)

    s3.put_object(Body=open(tempfile.gettempdir() + '/' + file_name, 'rb'), Bucket=settings.AWS_STORAGE_BUCKET_NAME, ContentType=file_stream.content_type, Key=file_path)
    os.remove(tempfile.gettempdir() + '/' + file_name)

    return file_path