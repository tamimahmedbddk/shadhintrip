from .settings import *

#dbbackup on production
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/home/shadhintrip/backup/'}