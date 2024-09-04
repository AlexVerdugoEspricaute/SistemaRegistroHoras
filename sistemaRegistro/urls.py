from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para acceder al panel de administración de Django
    path('', include('registroHoras.urls')),  # Incluir las URLs de la aplicación RegistroSistema
    re_path(r'^.*$', RedirectView.as_view(pattern_name='panel', permanent=False)),  # Redirigir cualquier otra URL a la vista del panel
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)