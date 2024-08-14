
from .settings import *

# Development-specific settings
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECRET_KEY='25^l5j0a(!o6am^-$6y_tnluht0n-3z=zpemm%=&(=95o%)h6o'


#dbbackup on local host

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/Users/iqbal/Desktop/shadhintrip/backup'}








# ==========comamnd to drop migratios files=======
######## find . -name "__pycache__" -type d -exec rm -r {} +  ##########


# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc" -delete
# ==========comamnd to drop migratios files=======

# ==========psql comamnd to drop tables=======