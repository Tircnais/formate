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
        rdfFred = '<?xml version="1.0"?><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/"><rdf:Description rdf:about="http://www.w3.org/"><dc:title>World Wide Web Consortium</dc:title> </rdf:Description></rdf:RDF>'
        # rdfFred = "objectFred.entidadesFred(entradaTexto)"
        # print('outFRED\n',rdfFred)
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
    

    def buscaCoincidencias(self, etiquetas: list, entidades: list):
        """Compara las etiquetas de los REA con las entidades encontradas en la Competecia Digital. Al superar el umbral establecido lo agrega a la lista. Esta lista es usara para buscar un RECURSO acorde.
        

        Args:
            etiquetas (list): LISTA de etiquetas percibidas por fastText
            entidades (list): LISTA de entidades encontradas

        Returns:
            list: Lista de coincidencias.
        """
        entidadesIdentificadas = []
        if entidades['entidadesDB'] is not None:
            entidadesIdentificadas.extend(entidades['entidadesDB'])
        if entidades['entidadesFred'] is not None:
            entidadesIdentificadas.extend(entidades['entidadesFred'])
        if entidades['entidadesDigcomp'] is not None:
            entidadesIdentificadas.extend(entidades['entidadesDigcomp'])
        entidadesIdentificadas = list(dict.fromkeys(entidadesIdentificadas))
        # Quitar duplicados en la lista'
        # print('Etiquetas(Tipo)\tEntidades(Tipo)\n{}\t{}\nEtiquetas\n{}Entidades\n{}'.format(type(etiquetas), type(entidades), etiquetas, entidades))
        coincidencias = []
        for etiqueta, medicion in etiquetas:
            print("{:<10} | {:<10}".format(etiqueta, medicion))
            # medicion = round(medicion*100, 2)
            medicion = round(medicion, 2)
            # se convieter a % (con 2 decimales)
            if len(entidadesIdentificadas) > 0:
                for uri, entidad in entidadesIdentificadas:
                    if medicion > 0.20 and etiqueta in entidad or entidad in etiqueta:
                        print('etiqueta\t{}'.format(etiqueta))
                        # print('etiqueta\t{}\nentidad\t{}'.format(etiqueta, entidad))
                        coincidencias.append((entidad, etiqueta, medicion))
        
        # print('coincidencias\n', coincidencias)
        # Consulta el triplestore de REA
        
        recursoRecomendados = []
        if len(coincidencias) > 0:
            servicioConsultas = entitiesDigcomp()
            for palabrasABuscar in coincidencias:
                print(coincidencia)
                recursoEncontrado = servicioConsultas.recomendacion(palabrasABuscar[0], palabrasABuscar[1], palabrasABuscar[1])
                recursoRecomendados.append(recursoEncontrado)
            del servicioConsultas
        else:
            recursoRecomendados = "Sin resultados"
        return recursoRecomendados


    def recursoRecomendado(self, entradaTexto: list):
        """Busco el recurso que tiene relacion con la competencia digital entrante

        Args:
            entradaTexto (list): Competencia digital entrante

        Returns:
            list: Recurso con relevancia
        """
        etiquetas = self.etiquetandoTexto(entradaTexto)
        entidades = self.entidadesEncontradas(entradaTexto)
        dicionario = {}
        dicionario['anotacion'] = entidades
        dicionario['recursos'] = self.buscaCoincidencias(etiquetas, entidades)
        return dicionario

    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")
