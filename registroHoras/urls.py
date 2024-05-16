from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),  # Ruta para cambiar la contraseña del usuario
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),  # Ruta para confirmar el cambio de contraseña
    path('', include('django.contrib.auth.urls')),  # Incluir las URLs de autenticación proporcionadas por Django
    path('', views.panel, name='panel'),  # Ruta para la vista del panel principal
    path('registrar/', views.registrar, name='registrar'),  # Ruta para la vista de registro de horas
    path('registrar_especial/', views.registrar_especial, name='registrar_especial'),  # Ruta para la vista de registro de horas especiales
    path('visualizar/', views.visualizar, name='visualizar'),  # Ruta para la vista de visualización de registros
    path('password_change/', views.password_change, name='password_change'),  # Ruta para cambiar la contraseña del usuario (vista personalizada)
    path('reporte_softland/', views.reporte_softland, name='reporte_softland'),  # Ruta para exportar datos a Excel
    path('exporte_a_excel_completo/', views.exporte_a_excel_completo, name='exporte_a_excel_completo'),  # Ruta para exportar todos los datos a Excel
    path('reporte_mensual/', views.reporte_mensual, name='reporte_mensual'),  # Ruta para generar un reporte mensual
    path('reporte_semanal/', views.reporte_semanal, name='reporte_semanal'),  # Ruta para generar un reporte semanal
    path('register/', views.register_user, name='register'),
]