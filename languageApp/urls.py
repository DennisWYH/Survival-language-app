from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_handler, about_handler, signup_handler, logout_handler, progress_handler

urlpatterns = [
    path("", include("card.urls")),
    path("login/", login_handler, name="login"),
    path('signup/', signup_handler, name='signup'),
    path('logout/', logout_handler, name='logout'),
    path("user/", include('user.urls')),
    path('progress/', progress_handler, name='progress'),
    path("about/", about_handler, name="about"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)