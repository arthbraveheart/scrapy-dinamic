from storages.backends.s3 import S3Storage

class MediaStorage(S3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        super(MediaStorage, self).__init__(*args, **kwargs)

class StaticStorage(S3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(StaticStorage, self).__init__(*args, **kwargs)