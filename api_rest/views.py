# Create your views here.
# Importamos los modelos
from dashboard.models import *
# Importamos los modelos serializados
from .serializers import *
# PARA el uso del API (al final)
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Grupos de Vistas definen el comportamiento de la vista.
#-----------------------API USUARIOS--------------------#
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#-----------------------API DIGCOMP--------------------#
class AreasdViewSet(viewsets.ModelViewSet):
    queryset = Areas.objects.all()
    serializer_class = AreasDSerializer

class CompetencesViewSet(viewsets.ModelViewSet):
    queryset = Competences.objects.all()
    serializer_class = CompetencesSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer

class NivelesdViewSet(viewsets.ModelViewSet):
    queryset = Proficiencylevels.objects.all()
    serializer_class = LevelDSerializer

class DetalleCompetenciaViewSet(viewsets.ModelViewSet):
    queryset = Linecompetences.objects.all()
    serializer_class = LineCompSerializer

class EjemploCompetenciaViewSet(viewsets.ModelViewSet):
    queryset = Examples.objects.all()
    serializer_class = ExampleDSerializer

#-----------------------API View--------------------#
class AreasList(APIView):
 
    def get(self, request):
        area = Areas.objects.all()
        serializer = AreasDSerializer(area, many=True)
        return Response(serializer.data)

class AreaDetails(APIView):
 
    def get_object(self, id):
        try:
            return Areas.objects.get(id=id)
        except Areas.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        area = self.get_object(id)
        serializer = AreasDSerializer(area)
        return Response(serializer.data)