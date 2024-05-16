from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para acceder al panel de administración de Django
    path('', include('registroHoras.urls')),  # Incluir las URLs de la aplicación RegistroSistema
    re_path(r'^.*$', RedirectView.as_view(pattern_name='panel', permanent=False)),  # Redirigir cualquier otra URL a la vista del panel
]