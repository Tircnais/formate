# Que es un serializador en Django
# PASAR los datos de:
# BD: Datos -->  JSON
# JSON --> bbdd 
from rest_framework import serializers, routers, viewsets
# Importamos los modelos
from dashboard.models import *
from django.contrib.auth.models import User

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'first_name', 'last_name', 'email', 'password', 'last_login']

# API AREAS de Digcomp
class AreasDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = ['idarea', 'nameareaen', 'nameareaes']

class CompetencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competences
        fields = ['idcompetence', 'fkarea', 'codecompetence', 'namecompetenceen', 'namecompetencees', 'descriptioncompetenceen', 'descriptioncompetencees']
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['idgroup', 'namegroupen', 'namegroupes']
    
class LevelDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proficiencylevels
        fields = ['idlevel', 'fkgroup', 'namelevelen', 'nameleveles', 'descriptionlevelen', 'descriptionleveles']

class LineCompSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linecompetences
        fields = ['idline', 'fkcompetence', 'fklevel', 'verben', 'verbes', 'keywordsen', 'keywordses', 'linecompetenceen', 'linecompetencees']

class ExampleDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examples
        fields = ['idexample', 'fklevel', 'fkcompetence', 'titlescenarioen', 'titlescenarioes', 'objectivescenarioen', 'objectivescenarioes', 'descriptionexampleen', 'descriptionexamplees']
