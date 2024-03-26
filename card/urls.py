from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "card"
urlpatterns = [
    # ex: /card
    path("", views.index, name="index"),
    # ex: /card/en
    path("<str:language>/", views.index, name="index"),
    # ex: /card/about
    path("about/", views.about, name="about"),
    # ex: /card/3/
    path("<int:card_id>/", views.detail, name="detail"),
    # ex: /card/3/update-answer/
    path("<int:card_id>/update-answer/", views.update_answer, name="update_answer"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)