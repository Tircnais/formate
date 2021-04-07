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
        infoCompetencia = Competences.objects.get(idcompetence=idComp)
        fkArea = infoCompetencia.fkarea
        infoArea = Areas.objects.get(idarea = int(fkArea.idarea))

        ### TAB 1
        area = infoArea.nameareaen
        descripcion = infoCompetencia.descriptioncompetenceen
        context['infoArea']= area
        context['infoCompetencia']= descripcion

        ### TAB 2
        textoNaturalEnglish = []
        fkArea = infoCompetencia.fkarea
        infoArea = Areas.objects.get(idarea = int(fkArea.idarea))
        # se trae el nombre del Area en ingles
        textoNaturalEnglish.append(infoArea.nameareaen)
        # se trae el nombre del Competencia en ingles
        textoNaturalEnglish.append(infoCompetencia.namecompetenceen)
        # se trae el descripcion del Competencia en ingles
        textoNaturalEnglish.append(infoCompetencia.descriptioncompetenceen)
        objectIntegracion = Integracion()
        textoNaturalEnglish = '. '.join(textoNaturalEnglish)
        anotacionSemantica = objectIntegracion.entidadesEncontradas(textoNaturalEnglish)
        del objectIntegracion
        print('CD del usuario enviada.\n{}\n\n'.format(textoNaturalEnglish))
        context['anotacion'] = anotacionSemantica
        
        ### TAB 3
        recursoRecomendado = Competenciasusuario.objects.get(fkcompetence=idComp, fkuser= idUser).recomendacion
        objectIntegracion = Integracion()
        recursoRecomendado = objectIntegracion.castStrToList(recursoRecomendado)
        del objectIntegracion
        sugerenciasPrevias = []
        if(recursoRecomendado == '' or recursoRecomendado == None or len(recursoRecomendado) == 0):
            # no hay sugerencias previas
            sugerenciasPrevias = None
            print('Sug. Previas\n', recursoRecomendado)
        else:
            # si hay sugerencias previas
            print('VIEW Sugerencia actual\tTipo: {}\tTam: {}'.format(type(recursoRecomendado), len(recursoRecomendado)))
            for uri in recursoRecomendado:
                # print('VIEW recurso\t', uri)
                objEntidades = entitiesDigcomp()
                recurso = objEntidades.recursoDetallado(uri)
                # se obtiene el detalle como lista, cada elemento es un diccionario
                del objEntidades
                # elimina el obj creado para liberar memoria
                coincidencia = False
                for detalle in recurso:
                    for clave, valor in detalle.items():
                        if(clave == 'Title' or clave == 'title' or clave == 'ttitle'):
                            # print('>>', clave, valor)
                            sugerenciasPrevias.append((valor, uri))
                            # si es el titulo se agrega a la lista
                            coincidencia = True
                            break
                            # encuentra una coicidencia pasa al siguiente recurso
                    if coincidencia:
                        break
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
        idComp = request.GET['fkCompetencia']
        # valor que se toma del ajax seccion data
        idUser = request.GET['pkUser']
        infoCompetencia = Competences.objects.get(idcompetence=idComp)

        ### TAB 2
        textoNaturalEnglish = []
        fkArea = infoCompetencia.fkarea
        infoArea = Areas.objects.get(idarea = int(fkArea.idarea))
        # se trae el nombre del Area en ingles
        textoNaturalEnglish.append(infoArea.nameareaen)
        # se trae el nombre del Competencia en ingles
        textoNaturalEnglish.append(infoCompetencia.namecompetenceen)
        # se trae el descripcion del Competencia en ingles
        textoNaturalEnglish.append(infoCompetencia.descriptioncompetenceen)
        textoNaturalEnglish = '. '.join(textoNaturalEnglish)
        objectIntegracion = Integracion()
        anotacionSemantica = objectIntegracion.entidadesEncontradas(textoNaturalEnglish)
        del objectIntegracion
        context['anotacion'] = anotacionSemantica
        
        ### TAB 3
        recomendaciones = []
        objectIntegracion = Integracion()
        respuestaDiccionario = objectIntegracion.recursoRecomendado(idUser, idComp, textoNaturalEnglish)
        # Se trae recurso recomendado y entidades (como parte del diccionario)
        recomendaciones = respuestaDiccionario['recursos']
        # print('Anotacion semantica\n{}\n'.format(anotacionSemantica))
        context['anotacion'] = anotacionSemantica
        del objectIntegracion

        objectFunciones = Funciones()
        listaSugerencias = objectFunciones.update_CompUsuario(idUser, idComp, recomendaciones)
        del objectFunciones
        
        sugerencias = []
        objEntidades = entitiesDigcomp()
        for uri in listaSugerencias:
            print('VIEW recurso\t', uri)
            recurso = objEntidades.recursoDetallado(uri)
            # se obtiene el detalle como lista, cada elemento es un diccionario
            coincidencia = False
            for detalle in recurso:
                for clave, valor in detalle.items():
                    if(clave == 'Title' or clave == 'title' or clave == 'ttitle'):
                        # print('>>', clave, valor)
                        sugerencias.append((valor, uri))
                        # si es el titulo se agrega a la list
                        coincidencia = True
                        # encuentra una coicidencia pasa al siguiente recurso
                        break
                if coincidencia:
                    break
        del objEntidades

        if (sugerencias == '' or sugerencias == None or type(sugerencias) == 'str' or len(sugerencias) == 0):
            # no hay sugerencias previas
            sugerencias = None
        context['recurso'] = sugerencias
        # Se destruye el objeto con la funcion creada
        print('VIEW Sugerencia actual\tTipo: {}\tTam: {}'.format(type(sugerencias), len(sugerencias)))
        return JsonResponse(context, safe=False)