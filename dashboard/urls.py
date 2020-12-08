from django.urls import path
# para USAR url en lugar de PATH
from django.conf.urls import include
# para acceso controlado por LOGEO 
from django.contrib.auth.views import login_required

from . import views

# es necesario importar las VISTAS
from .views import *


urlpatterns = [
    path('', views.index, name='home'),
    # Registro de Usuarios
    path('registro', RegistroUsuario.as_view(), name='nuevoUs'),
    path('misCompetencias/', CompetenciasUsuarioListView.as_view(), name='misComp'),
    path('registroCompetencias/', RegistroCompetenciasView.as_view(), name='nuevasComp'),
    # path('actualizarCompetencias/', ActualizarCompetenciasView.as_view(), name='actualizarComp'),
    path('actualizarCompetencias/<int:pk>', ActualizarCompetenciasView.as_view(), name='actualizarComp'),
    
    # Funciones Ajax
    path(r'detalleCompetencia/', views.DetalleCompetencia, name='ajaxDetalleComp'),
]