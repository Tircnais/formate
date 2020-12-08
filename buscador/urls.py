from django.urls import path

# es necesario importar las VISTAS
from . import views
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View

urlpatterns = [
    path('<int:pk>', views.index.as_view(),name='busca_home'),
    path('oer', views.listadoRecursos, name='busca_rea'),
    # Funciones Ajax
    path('recursoActual/', views.cargandoRecurso, name='ajaxMuestraRecurso'),
    path('detalleCompetencia/', views.DetalleCompetencia, name='ajaxDetalle'),
]