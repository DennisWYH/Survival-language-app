from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
]
if settings.DEBUG:  # only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)