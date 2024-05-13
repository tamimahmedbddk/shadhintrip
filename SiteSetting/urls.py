# urls.py (Development only, not for production)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of urlpatterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
