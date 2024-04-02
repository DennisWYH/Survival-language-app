from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "user"
urlpatterns = [
    path("", views.profile, name="profile"),
    path("update", views.update, name="update_profile"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)