# Create your views here.
# Redireccionar a paginas
from django.urls import reverse_lazy
# CRUD
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# se importan los modelos
from dashboard.models import *
# Tipos de salidas a template
from django.shortcuts import render, get_object_or_404
# Para el ajax (registro Competencias)
from django.http import JsonResponse

# necesaro para AJAX
from django.views.decorators.csrf import csrf_exempt

# Formularios (personalizados creados)
from .forms import *
# Usado en consulta lambda para contar por grupos
from django.db.models import Count

# Para las cuenta de usuario (no administradores)
from django.contrib.auth.models import User

# Vistas disponibles solo con autenticacion (LOGEO)
from django.contrib.auth.decorators import login_required

import json

# Para filter competencias del usuario LOGEADO
from django.contrib.auth.mixins import LoginRequiredMixin

# Identificar entidad
# rdflib (Consultamos el sparql)
from rdflib.serializer import Serializer
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON


class RegistroUsuario(CreateView):
    '''
        Registra el usuario al sistema solo usuarios (no administrador), al finalizar redirecciona al login.

            Parametros
            ----------
                CreateView (class): Ayuda a generar el formulario para el registro
    '''
    model = User
    form_class = UsuarioForm
    template_name = "registro.html"
    success_url = reverse_lazy('login')


def index(request):
    resumen = dict()
    resumen['Total de áreas'] = Areas.objects.all().count()
    resumen['Total de competencias'] = Competences.objects.all().count()
    resumen['Total de nivel'] = Groups.objects.all().count()
    resumen['Total de dificultad por nivel'] = Proficiencylevels.objects.all().count()
    resumen['Ejemplos disponibles'] = Examples.objects.all().count()
    # nombAreas = Areas.objects.values_list('nameareaes')
    # nombGrupos = Groups.objects.values_list('namegroupes')
    nombAreacantCopm  = Competences.objects.values('fkarea__nameareaen').annotate(numCompArea=Count('fkarea')).order_by('fkarea')
    nombAreaNumComp = [(*dict_instance.values(),) for dict_instance in nombAreacantCopm]
    # nombAreaNumComp = [f'{value[0]}: {value[1]}' for value in values]
    
    nombCompCantExam = Examples.objects.values('fkcompetence__namecompetenceen').annotate(numExampComp=Count('fkcompetence')).order_by('fkcompetence')[:20]
    nombCompNumExam = [(*dict_instance.values(),) for dict_instance in nombCompCantExam]
    
    nombGrupoCantNiveles = Proficiencylevels.objects.values('fkgroup__namegroupen').annotate(numNivelesGrupo=Count('fkgroup')).order_by('fkgroup')
    nombGrupoNumNiveles = [(*dict_instance.values(),) for dict_instance in nombGrupoCantNiveles]
    # nombGrupoNumNiveles = [f'{value[0]}: {value[1]}' for value in claveValor]
    # print(objModel.__str__)
    # print(objModel.__unicode__)
    cntxtIndex = {
        'nombAreaNumComp': nombAreaNumComp,
        'nombCompNumExam': nombCompNumExam,
        'nombGrupoNumNiveles': nombGrupoNumNiveles,
        'resumen': resumen,
    }
    return render(request, "index.html", cntxtIndex)


class CompetenciasUsuarioListView(LoginRequiredMixin, ListView):
    '''
        Lista las competencias asociadas con el usuario Logeado.

            Parametros
            ----------
                LoginRequiredMixin (class): Ayuda a obtener el ID del usuario
                ListView (class): Genera vista basada en clases
            
            Returns:
            ----------
                QuerySet: Es un dict de objetos que hace referencia a la tabla intermedia usada para el registro
    '''
    model = Competenciasusuario
    template_name = 'competenciasusuario_list.html'
    context_object_name = 'misCompetencias'
    
    def get_queryset(self):
        # print('ID user login\t', self.request.user.id)
        lista = Competenciasusuario.objects.filter(fkuser_id=self.request.user.id).order_by('fkcompetence')
        print('QUERY SET\n', lista)
        return lista


class RegistroCompetenciasView(LoginRequiredMixin, CreateView):
    '''
        Registra las competencias digitales del usuario

            Parametros
            ----------
                LoginRequiredMixin (class): Ayuda a obtener el ID del usuario
                CreateView (class): Genera vista basada en clases para crear.
            
            Returns:
            ----------
                form_valid: Reforna un formulario valido para registrar
    '''
    model = Competenciasusuario
    # form_class = RegistroCompForm
    fields = ['fkcompetence', 'tiene']
    # Aqui empezando el registro de competencia
    template_name = 'competenciasusuario_form.html'
    success_url = reverse_lazy('nuevasComp')
    
    def form_valid(self, form):
        print('ID user logeado\t', self.request.user)
        fkcompetence = form.cleaned_data['fkcompetence']
        tiene = form.cleaned_data['tiene']
        # todo el id del USUARIO LOGEADO
        form.instance.fkuser = self.request.user
        return super().form_valid(form)


class ActualizarCompetenciasView(LoginRequiredMixin, UpdateView):
    '''
        Visualiza los competencias del usuario y el valor con el que fueron guardadas

            Parametros
            ----------
                LoginRequiredMixin (class): Ayuda a obtener el ID del usuario
                CreateView (class): Genera vista basada en clases para crear.
            
            Returns:
            ----------
                form_valid: Reforna un formulario valido para modificar el registro
    '''
    model = Competenciasusuario
    fields = ['tiene']
    template_name = 'competenciasusuario_update.html'
    context_object_name = 'competenciaActual'
    success_url = reverse_lazy('misComp')

    def get_object(self):
        idcompetence = self.kwargs.get("pk")
        print("ID_Competence\t ", idcompetence)
        idUser = self.request.user
        print("ID_User\t ", idUser.id)
        instance = get_object_or_404(Competenciasusuario, fkcompetence = idcompetence, fkuser= idUser.id)
        return instance

    def form_valid(self, form):
        idUser = self.request.user
        idcompetence = self.kwargs.get("pk")
        # idcompetence = self.kwargs.id
        print("ID_User Form\t ", idUser)
        # Toma el ID de la competencia (enviado en la URL)
        print("ID_Competence Form\t ", idcompetence)
        tiene = form.instance.tiene
        user = self.request.user.first_name +" "+ self.request.user.last_name
        print("Usuario Form\t ", user)
        redirect_url = super(ActualizarCompetenciasView, self).form_valid(form)
        updateCompetencia = Competenciasusuario.objects.get(fkuser = idUser, fkcompetence = idcompetence)
        # Trae la competencia a modificar
        updateCompetencia.tiene = tiene
        updateCompetencia.save()
        tiene = form.cleaned_data['tiene']
        return redirect_url


@csrf_exempt
def DetalleCompetencia(request):
    '''
        Ajax que permite obtener el nombre del area y descripcion de la competencias seleccionada

            Parametros
            ----------
                request : request
                    Ayuda a obtener el valor de la funcion ajax
            
            Returns:
            ----------
                JsonResponse: Con el diccionario del detalla requerido
    '''
    if request.is_ajax() == True:
        context ={}
        idComp = request.POST['fkCompetencia']
        # valor que se toma del ajax seccion data
        print('ID competencia selecionada\t', idComp)
        queryset = Competences.objects.get(idcompetence=idComp)
        infoCompetencia = queryset
        print('infoCompetencia\t', infoCompetencia)
        fkArea = infoCompetencia.fkarea
        fkAreaComp = int(fkArea.idarea)
        print('fkAreaComp\t', fkAreaComp)
        queryset = Areas.objects.get(idarea = fkAreaComp)
        infoArea = queryset
        print('infoArea\t', infoArea)
        context['infoArea']= infoArea.nameareaes
        context['infoCompetencia']= infoCompetencia.descriptioncompetencees
        return JsonResponse(context, safe=False)
