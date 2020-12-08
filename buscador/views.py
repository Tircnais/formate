# Create your views here.
from django.shortcuts import render, redirect

# Se importa modelos
from dashboard.models import *
from django.contrib.auth.models import User

# Vistas
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
# necesaro para AJAX
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Se identifica y etiqueta Entidades
from .integracion import Integracion
# Se importan la funciones creadas
from .funciones import Funciones
# Importando el servicio de consulta creado
from recomendacion.Triplestore.servicioConsulta import entitiesDigcomp

class index(DetailView):
    model = User
    template_name = 'base.html'
    context_object_name = 'miUsuario'

    def get_context_data(self, **kwargs):
        context = {}
        context['misCompetencias'] = Competenciasusuario.objects.filter(fkuser=self.object.id, tiene=1).order_by('fkcompetence')
        return super().get_context_data(**context)

def listadoRecursos(request):
    servicioConsultas = entitiesDigcomp()
    reaDisponibles = servicioConsultas.recursosDisponibles()
    cntxtREA = {
        'recursos': reaDisponibles,
    }
    del servicioConsultas
    # Para visualizacion en local (reemplece en HTML|DJANGO)
    # http://localhost:7200/resource?uri=http:%2F%2Flocalhost:7200%2Foer%2Frecursos%2F1062
    return render(request, "tables.html", cntxtREA)


def detalleRecurso(request, enlace):
    # enlace Recurso
    servicioConsultas = entitiesDigcomp()
    # se llama al servicio
    reaConsultado = servicioConsultas.recursoDetallado(enlace)
    cntxtREA = {
        'recurso': recurso
    }
    del servicioConsultas
    return render(request, "recursoDetallado.html", cntxtREA)


# --------- AJAX ---------
@csrf_exempt
def cargandoRecurso(request):
    '''
        Seleccionada la compentencia carga el recurso recomendado.

            Parametros
            ----------
                request : request
                    Ayuda a obtener el recurso recomendado actual
            
            Returns:
            ----------
                JsonResponse: Con el diccionario del detalla requerido
    '''
    if request.is_ajax() == True:
        context ={}
        idComp = request.GET['fkCompetencia']
        # valor que se toma del ajax seccion data
        idUser = request.GET['pkUser']
        recursoRecomendado = Competenciasusuario.objects.get(fkcompetence=idComp, fkuser= idUser).recomendacion
        context['recomendadoActual'] = recursoRecomendado
        return JsonResponse(context, safe=False)


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
        textoNaturalEnglish = []
        idComp = request.GET['fkCompetencia']
        # valor que se toma del ajax seccion data
        idUser = request.GET['pkUser']
        infoCompetencia = Competences.objects.get(idcompetence=idComp)
        fkArea = infoCompetencia.fkarea
        infoArea = Areas.objects.get(idarea = int(fkArea.idarea))
        context['infoArea']= infoArea.nameareaes
        context['infoCompetencia']= infoCompetencia.descriptioncompetencees
        # se trae el nombre del Area en ingles
        textoNaturalEnglish.append(infoArea.nameareaen)
        # se trae el nombre del Competencia en ingles
        textoNaturalEnglish.append(infoCompetencia.namecompetenceen)
        # se trae el descripcion del Competencia en ingles
        textoNaturalEnglish.append(infoCompetencia.descriptioncompetenceen)
        recomendaciones = []
        objectIntegracion = Integracion()
        textoNaturalEnglish = '. '.join(textoNaturalEnglish)
        print('CD del usuario enviada.\n{}'.format(textoNaturalEnglish))
        respuestaDiccionario = objectIntegracion.recursoRecomendado(textoNaturalEnglish)
        # Se trae recurso recomendado y entidades (como parte del diccionario)
        anotacionSemantica = respuestaDiccionario['anotacion']
        recomendaciones = respuestaDiccionario['recursos']
        # print('Anotacion semantica\n{}\n'.format(anotacionSemantica))
        context['anotacion'] = anotacionSemantica
        del objectIntegracion

        # asignacion OER
        objectFunciones = Funciones()
        if len(recomendaciones) > 0:
            objectFunciones.update_CompUsuario(idUser, idComp, recomendaciones)
        else:
            objectFunciones.update_CompUsuario(idUser, idComp, "Sin resultados")
        context['recurso'] = objectFunciones.search_CompUsuario(idUser, idComp).recomendacion
        del objectFunciones
        # Se destruye el objeto con la funcion creada
        # print('context\n', context)
        return JsonResponse(context, safe=False)