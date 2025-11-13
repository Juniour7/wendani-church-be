from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False
    custom_domain = "churchmedia.kahawawendanisda.org"
