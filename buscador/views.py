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

def detalleRecurso(request):
    uri = request.GET['uri']
    # enlace Recurso
    servicioConsultas = entitiesDigcomp()
    # se llama al servicio
    reaConsultado = servicioConsultas.recursoDetallado(uri)
    # uri = 'http://localhost:7200/oer/recursos/'+ uri
    cntxtREA = {
        'recurso': reaConsultado
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
        objectIntegracion = Integracion()
        recursoRecomendado = objectIntegracion.castStrToList(recursoRecomendado)
        del objectIntegracion
        sugerenciasPrevias = []
        infoREA = dict()
        print('VIEW Sugerencia actual\n',recursoRecomendado)
        print('VIEW Tipo de dato que regresa\n', type(recursoRecomendado))
        if (recursoRecomendado == '' or recursoRecomendado == None or type(recursoRecomendado) == 'str'):
            # no hay sugerencias previas
            # sugerenciasPrevias = infoREA = {'title': 'OERs', 'uri': 'Not availables'}
            sugerenciasPrevias = None
        elif (type(recursoRecomendado) == 'list'):
            # lista de sugerencias
            for rea in recursoRecomendado:
                print('Recurso\n{} - {}'.format(rea[0], rea[1]))
                # infoREA = {'title': rea[0], 'uri': rea[1]}
                # sugerenciasPrevias.append(infoREA)
                sugerenciasPrevias.append((rea[0], rea[1]))
        else:
            # una sola sugerencia
            # infoREA = {'title': recursoRecomendado[0], 'uri': recursoRecomendado[1]}
            # sugerenciasPrevias.append(infoREA)
            sugerenciasPrevias.append((recursoRecomendado[0], recursoRecomendado[1]))
        context['recurso'] = sugerenciasPrevias
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
        print('CD del usuario enviada.\n{}\n\n'.format(textoNaturalEnglish))
        respuestaDiccionario = objectIntegracion.recursoRecomendado(idUser, idComp, textoNaturalEnglish)
        # Se trae recurso recomendado y entidades (como parte del diccionario)
        anotacionSemantica = respuestaDiccionario['anotacion']
        recomendaciones = respuestaDiccionario['recursos']
        # print('Anotacion semantica\n{}\n'.format(anotacionSemantica))
        context['anotacion'] = anotacionSemantica
        del objectIntegracion

        # busca las recomendaciones realizadas
        objectFunciones = Funciones()
        listaSugerencias = objectFunciones.update_CompUsuario(idUser, idComp, recomendaciones)
        sugerencias = []
        infoREA = dict()
        if (listaSugerencias == '' or listaSugerencias == None or type(listaSugerencias) == 'str'):
            # no hay sugerencias previas
            sugerencias = infoREA = {'title': 'OERs', 'uri': 'Not availables'}
        elif (type(listaSugerencias) == 'list'):
            # lista de sugerencias
            for rea in listaSugerencias:
                print('Recurso\n{} - {}'.format(rea[0], rea[1]))
                infoREA = {'title': rea[0], 'uri': rea[1]}
                sugerencias.append(infoREA)
        else:
            # una sola sugerencia
            infoREA = {'title': listaSugerencias[0], 'uri': listaSugerencias[1]}
            sugerencias.append(infoREA)
        context['recurso'] = sugerencias
        del objectFunciones
        # Se destruye el objeto con la funcion creada
        # print('context\n', context)
        return JsonResponse(context, safe=False)