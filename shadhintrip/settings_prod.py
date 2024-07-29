from .settings import *

# Production-specific settings
DEBUG=False
ALLOWED_HOSTS = ['markcc.shop','www.markcc.shop','localhost']
SECRET_KEY='25^l5j0a(!o6am^-$6y_tnluht0n-3z=zpemm%=&(=95o%)h6o'

#dbbackup on production
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/home/shadhintrip/backup/'}