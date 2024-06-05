
from .settings import *

#dbbackup on local host

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/Users/iqbal/Desktop/shadhintrip-final/dbbackup'}








# ==========comamnd to drop migratios files=======
######## find . -name "__pycache__" -type d -exec rm -r {} +  ##########


# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc" -delete
# ==========comamnd to drop migratios files=======

# ==========psql comamnd to drop tables=======