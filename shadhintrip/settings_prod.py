from .settings import *

# Production-specific settings
DEBUG=False
ALLOWED_HOSTS = ['shadhintrip.com','www.shadhintrip.com','localhost']
SECRET_KEY='25^l5j0a(!o6am^-$6y_tnluht0n-3z=zpemm%=&(=95o%)h6o'

#dbbackup on production
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/home/shadhintrip/backup/'}


# ====Ensure CSRF protection is enabled====
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
# ====Secure https Settings====
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# ====Secure hsts Settings====
SECURE_HSTS_SECONDS = 15780000 #for 6 month
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Set the session to expire after a period of inactivity (e.g., 5 minutes).
SESSION_COOKIE_AGE = 3600  # 3600 seconds (60 minutes)

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Set to True if we want to detect when the user has become inactive (not just when the cookie expires)
SESSION_SAVE_EVERY_REQUEST = True