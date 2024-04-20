from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("lang/<str:language>/", views.index, name="index"),
    path("lang/<str:language>/<int:card_id>/", views.detail, name="detail"),
    path("lang/<str:language>/game", views.game, name="game"),
    path("<int:card_id>/update-answer/", views.update_answer, name="update_answer"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'card.views.server_error'