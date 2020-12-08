from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.template.loader import render_to_string

# Usando render para un error aun sin documentacion aprender en DJANGO
from django.shortcuts import render

def bad_request(request):
    # , exception
    nombre_template = '400.html'
    return HttpResponseBadRequest(render_to_string(nombre_template, request=request))

def no_autorizado(request):
    nombre_template = '401.html'
    return render(request, nombre_template, status=401)

def permission_denied(request, exception):
    nombre_template = '403.html'
    # HttpResponseForbidden
    return HttpResponseForbidden(request, nombre_template, status=403)

def no_encontrada(request, exception):
    nombre_template = '404.html'
    # if request.path.startswith('/app1'):
    #     nombre_template = 'app1_404.html'
    # elif request.path.startswith('/app2'):
    #     nombre_template = 'app2_404.html'
    # return HttpResponseNotFound(render_to_string(nombre_template), status=404)
    return HttpResponseNotFound(render_to_string(nombre_template, request=request))

def server_error(request):
    nombre_template = '500.html'
    # HttpResponseServerError
    # return HttpResponseServerError(request, nombre_template, status=500)
    return HttpResponseServerError(render_to_string(nombre_template, request=request))
