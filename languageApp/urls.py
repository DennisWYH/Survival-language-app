from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import loginHandler, aboutHandler, signupHandler, logoutHandler, progressHandler

urlpatterns = [
    path("", include("card.urls")),
    path("login/", loginHandler, name="login"),
    path('signup/', signupHandler, name='signup'),
    path('logout/', logoutHandler, name='logout'),
    path("user/", include('user.urls')),
    path('progress/', progressHandler, name='progress'),
    path("about/", aboutHandler, name="about"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)