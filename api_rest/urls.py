from django.urls import path
# para USAR url en lugar de PATH
from django.conf.urls import include

# es necesario importar las VISTAS
from .views import *

# PARA LAS API
from rest_framework import routers
# Routers para las API (Ej. http://127.0.0.1:8000/api_rest/api/niveles/)
# La API necesita un Serializador, Vista y esta ruta
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('areasdigcomp', AreasdViewSet)
router.register('competencias', CompetencesViewSet)
router.register('grupos', GroupViewSet)
router.register('niveles', NivelesdViewSet)
router.register('det_competencias', DetalleCompetenciaViewSet)
router.register('ejemplo', EjemploCompetenciaViewSet)

urlpatterns = [
    path('', include(router.urls), name='api-rest'),
    path('list_rareas/', AreasList.as_view()),
    path('detail_area/<int:id>/', AreaDetails.as_view()),
]