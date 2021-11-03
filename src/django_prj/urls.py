from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import base




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('django_app/', include('django_app.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
