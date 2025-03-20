from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views



urlpatterns = [
    path('', views.comment_list, name='comments_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
