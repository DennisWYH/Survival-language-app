from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, about_view

urlpatterns = [
    path("", include("card.urls")),
    path("login/", login_view, name="login"),
    path("user/", include('user.urls')),
    path("about/", about_view, name="about"),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
