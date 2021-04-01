# Importando fastText
from recomendacion.fastText.modeloFastText import generarModelo
# Importando el servicio de DBpediaSpotlight
from recomendacion.DBpediaSpotlight.servicioSpotlight import entitiesSpotlight
# Importando el servicio de FRED
from recomendacion.Fred.servicioFred import entitiesFred
# Importando el servicio de consulta creado
from recomendacion.Triplestore.servicioConsulta import entitiesDigcomp
# Importando PLN
# from recomendacion.pln.procesamiento
# Importando rdflib para identificar entidades resultantes del API de Fred
# from rdflib.namespace import RDF, RDFS, Literal, XSD
# salida como tabla solo para revisar
from recomendacion.Fred.crearRDF import PreparandoArchivos
# Se importan la funciones creadas
from .funciones import Funciones
# usado para convertir el STRING de la BD a list
import json

class Integracion:
    """Identificando entidades y etiquetando
    """

    def etiquetandoTexto(self, entradaTexto: str):
        """Etiquetando texto para ello se emplea la lib FastText

        Args:
            entradaTexto (str): Competencia digital entrante

        Returns:
            list: Con las predicciones o etiquetas dadas a la Competencia digital
        """
        etiquetas = []
        ft = generarModelo()
        # # # Implementando fastText
        nombreModelo = "model_rea"
        modeloUsado = ft.cargarModelo(nombreModelo)
        # Cargando el modelo
        predicciones = ft.predecir(modeloUsado, entradaTexto)
        # Predecir el texto
        etiquetas = predicciones
        del ft
        # print('Texto a etiquetar\n{}\nEtiquetas para recomendar REA\n{}\nModelo FastText Usado:\t{}\n'.format(entradaTexto, etiquetas, modeloUsado))
        # print("Conteo duplicados:\t", len(etiquetas))
        return etiquetas


    def vinculandoEntidades(self, detalle: str, entidades: list):
        """Vinculación de entidad con nombre (sus siglas en ingles (NEL).NEL asignará una identidad única a las entidades mencionadas en el texto. En otras palabras, NEL es la tarea de vincular las menciones de entidades en el texto con sus entidades correspondientes en una base de conocimiento.

        Args:
            detalle (str): Cadena/oracion a analizar
            entidades (list): Lista de entidades con la URI correspondiente

        Returns:
            list: Cadena/oracion con la vinculacion realizada
        """
        enlazandoEntidades = []
        detalle = detalle.split(". ")
        # print("Recibiendo datos a vincular\t", detalle)
        for oracion in detalle:
            for uri, label in entidades:
                # reversed(list) orden descendente
                # print("Oracion\n{}\nURI\t{}\tlabel\n{}\n".format(oracion, uri, label))
                if (label in oracion):
                    enlace = '<a href="'+uri+'" target="_blank" class="badge badge-info">'+label+'</a>'
                    oracion = oracion.replace(label, enlace)
                    # print('la anotacion es:', enlace)
                    enlazandoEntidades.append(oracion)
                else:
                    # print('Sin cambios:', oracion)
                    enlazandoEntidades.append(oracion)
        enlazandoEntidades = list(dict.fromkeys(enlazandoEntidades))
        # Quitar duplicados en la lista
        return enlazandoEntidades

    def entidadesEncontradas(self, entradaTexto: str):
        """Reconocimiento de entidad nombrada (sus sgilas en ingles NER).NER nos dirá qué palabras son entidades y cuáles son sus tipos. En resumen se identifica las entidades del texto entrante.
        

        Args:
            entradaTexto (str): Competencia digital a analizar

        Returns:
            list: Lista de entidades identificadas
        """
        dictionarioEntidades = {}
        # Implementando DBpedia y Fred
        # Reconocimiento de entidades DBpedia Spotlight
        objectSpotlight = entitiesSpotlight()
        entidadesDB = objectSpotlight.entidadesSpotlight(entradaTexto)
        # print('\nEntidadesDB\n{}\nTexto a vincular\n{}\n'.format(entidadesDB, entradaTexto))
        anotacion_DB = ''
        if entidadesDB is not None:
            anotacion_DB = self.vinculandoEntidades(entradaTexto, entidadesDB)
            dictionarioEntidades['entidadesDB'] = entidadesDB
            dictionarioEntidades['vicunlancionDB'] = anotacion_DB
        else:
            dictionarioEntidades['entidadesDB'] = None
            dictionarioEntidades['vicunlancionDB'] = None
        # print('Anotacion Spotlight resultante\n{}\n'.format(dictionarioEntidades['entidadesDB']))
        # Eliminando el objeto para liberar recursos
        del objectSpotlight

        # Reconocimiento de entidades FRED
        objectFred = entitiesFred()
        entidadesFred = objectFred.entidadesFred(entradaTexto)
        if entidadesFred is not None:
            anotacion_FRED = self.vinculandoEntidades(entradaTexto, entidadesFred)    
            # dictionarioEntidades['entidadesFred'] = str(rdfFred)
            dictionarioEntidades['entidadesFred'] = entidadesFred
            dictionarioEntidades['vinculacionFred'] = anotacion_FRED
        else:
            dictionarioEntidades['entidadesFred'] = None
            dictionarioEntidades['vinculacionFred'] = None
        # Eliminando el objeto para liberar recursos
        del objectFred

        # Consulta el triplestore de Digcomp y une las entidades
        objectDigcomp = entitiesDigcomp()
        resultadoDigcomp = objectDigcomp.vinculadoEntidades(entradaTexto)
        dictionarioEntidades['entidadesDigcomp'] = resultadoDigcomp['entidadesDigcomp']
        dictionarioEntidades['vinculacionDigcomp'] = resultadoDigcomp['vinculacionDigcomp']
        del objectDigcomp
        # print("Modelo FastText. Usado:\t ", modeloUsado)
        # print('Entidades encontradas\n{}'.format(dictionarioEntidades))
        return dictionarioEntidades
    
    # se compara consigo mismo, no con el triplestore
    def buscaCoincidencias(self, prediccionCD: list, recursos: list):
        """Compara la prediccion de la CD con c/u de los REA encontrados. Al superar el umbral establecido lo agrega a la lista. Esta lista es usara para asignar el RECURSO.
        

        Args:
            prediccionCD (list): LISTA de etiquetas percibidas por fastText
            recursos (list): LISTA de REA encontradas

        Returns:
            list: Lista de coincidencias.
        """
        # print('Etiquetas(Tipo)\tEntidades(Tipo)\n{}\t{}\nEtiquetas\n{}Entidades\n{}'.format(type(etiquetas), type(entidades), etiquetas, entidades))
        recursoRecomendados = []
        umbral = 0.20
        umbralREA = umbral * 4.65
        for etiqueta, medicion in prediccionCD:
            # print('Prediccion CD\nEtiqueta: %s\tMedicion: %.2f' %(etiqueta, medicion))
            medicion = round(medicion, 2)
            # se convieter a % (con 2 decimales)
            for titulo, enlace, prediccion in recursos:
                if type(prediccion) is list:
                    # cuando hay mas de una prediccion
                    for p_eti, p_med in prediccion:
                        # print("{0} | {1}".format(p_eti, p_med))
                        p_med = round(p_med, 2)
                        if medicion >= umbral and p_med >= umbralREA:
                            # print('Umbral: \t{}\nPred CD\t{}\tPred REA\t{}'.format(umbral, medicion, p_med))
                            # si ambas predicciones (CD y el recurso) superan el umbral establecido se agrega como coicidencia
                            recursoRecomendados.append((titulo, enlace))
                else:
                    # cuando solo hay una prediccion
                    # print("{0} | {1}".format(prediccion[0], prediccion[1]))
                    prediccion = round(prediccion[1], 2)
                    if medicion >= umbral and prediccion >= umbralREA:
                        # print('Umbral: \t{}\nPred CD\t{}\tPred REA\t{}'.format(umbral, medicion, prediccion))
                        # si ambas predicciones (CD y el recurso) superan el umbral establecido se agrega como coicidencia
                        recursoRecomendados.append((titulo, enlace))
        return recursoRecomendados


    def castStrToList(self, recuperadoBD: str):
        """Convierte la cadena guardada en BD a una lista para poder trabajar mejor

        Args:
            recuperadoBD (str): Sugerencias guardadas en BD

        Returns:
            list: Recurso asignados
        """
        castList = []
        if(recuperadoBD == '' or recuperadoBD == None):
            return castList
        else:
            # print('TIPO entrante\t{}\nRecuperado\n{}\n\n\n'.format(type(recuperadoBD), recuperadoBD))
            texto_json = recuperadoBD.replace('\'', '"')
            texto_json = texto_json[1:len(texto_json)-1]
            texto_json = texto_json.split('), (')
            # jsonlista = list(texto_json)
            # .replace('(', '[').replace(')', ']')
            print("Tipo de dato\t", type(texto_json))
            for a in texto_json:
                a = a.split('", "')
                i = a[0].replace('"', '').replace('(', '').replace('\'', '"') # titulo
                j = a[1].replace('"', '').replace(')', '').replace('\'', '"') # uri
                tupla = (i, j)
                # print('tupla\t', tupla)
                castList.append(tupla)
            return castList
    

    def recursoRecomendado(self, idUser: int, idComp: int, entradaTexto: list):
        """Busco el recurso que tiene relacion con la competencia digital entrante

        Args:
            entradaTexto (list): Competencia digital entrante

        Returns:
            list: Recurso con relevancia
        """
        # fastText Etiquetas y Entidades de la CD seleccionada
        prediconCD = self.etiquetandoTexto(entradaTexto)
        # Anotacion semantica con los diversos servicios/vocab
        entidades = self.entidadesEncontradas(entradaTexto)
        
        # Consulta del Recurso(s) actual(es)
        objectFunciones = Funciones()
        recomendacionActual = objectFunciones.search_CompUsuario(idUser, idComp)
        # print('Recomendacion actual:\n{}'.format(recomendacionActual.recomendacion))
        recomendacionActual = recomendacionActual.recomendacion
        # Borramos el OBJ para liberar memoria
        del objectFunciones
        
        # Consulta para determinar los REA disponibles
        objectDigcomp = entitiesDigcomp()
        reas = objectDigcomp.recursosDisponibles()
        print('Recursos Disponibles... integracion.py LEN: ', len(reas))
        del objectDigcomp

        # Prediccion con fastText
        listaREA = []
        for oer in reas:
            # print('>>{}\n'.format(oer))
            prediccionREA = self.etiquetandoTexto(oer['titulo']+' '+oer['categoria'])
            listaREA.append((oer['titulo'], oer['enlace'], prediccionREA))
        
        sugerencias = self.buscaCoincidencias(prediconCD, listaREA)
        recomendaciones = []
        print('Cant. sugerencias\t{}\nTipo retorno\t{}\n'.format(len(sugerencias), type(sugerencias)))
        recomendacionActual = self.castStrToList(recomendacionActual)
        if recomendacionActual == '' or recomendacionActual == 'Sin resultados' or recomendacionActual == None and type(sugerencias) != list:
            recomendaciones = sugerencias
            # cuando no hay sugerencias previas pero si nuevas
        elif type(recomendacionActual) == list and type(sugerencias) == list:
            # cuand hay una lista de sugerencias previas y nuevas
            recomendaciones = recomendacionActual
            # for elemento in recomendacionActual:
            #     recomendaciones.append(elemento)
            #     # cuando ya hay una lista de recomendaciones previas
            for elemento in sugerencias:
                recomendaciones.append(elemento)
                # cuando ya hay una lista de recomendaciones nuevas
        elif type(recomendacionActual) != list:
            # cuando hay una sola recomendacion y una lista de sugerencias
            recomendaciones.append(recomendacionActual)
            for elemento in sugerencias:
                recomendaciones.append(elemento)
                # cuando ya hay una lista de recomendaciones nuevas
        else:
            # si hay una sugerencia previa y una sola sugerencia
            recomendaciones.append(recomendacionActual)
            recomendaciones.append(sugerencias)
        
        # print('Recomendaciones\n', recomendaciones)
        recomendaciones = list(dict.fromkeys(recomendaciones))
        # Quitar duplicados en la lista
        # recomendaciones = json.dumps(recomendaciones)
        # cast to JSON
        dicionario = {}
        dicionario['anotacion'] = entidades
        dicionario['recursos'] = recomendaciones
        return dicionario

    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")
