from rdflib.serializer import Serializer
from SPARQLWrapper import SPARQLWrapper, JSON

class entitiesDigcomp:
    # endpointREA ="http://localhost:7200/repositories/02"
    def anotacion(self, nombArea: str, nombComp: str):
        # print("llega:\t", nombArea)
        # Endpoint con Server D2RQ
        sparqlendpoint = "http://localhost:2020/sparql"
        # Endpoint con GraphDB
        sparqlendpoint ="http://localhost:7200/repositories/01"
        # Consulta SPARQL para buscar en la BD la entidad encontrada
        sbcEndpoint = SPARQLWrapper(sparqlendpoint)
        consulta = """
        PREFIX dco: <http://localhost:7200/digcomp/ontology/>
        PREFIX dcr: <http://localhost:7200/digcomp/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select * where {
            ?uri_comp ?p ?es .
            ?uri_comp a dco:Competences .
            ?uri_comp dcr:nombre_competencia_digital ?es .
            ?uri_comp dcr:digitalCompetence_name ?en .
            ?uri_comp dco:isPartOfACompetenceArea ?uri_area .
            ?uri_area ?property ?nameEn .
            ?uri_area a dco:Areas .
            ?uri_area dcr:nombre_del_area ?nameEs .
            ?uri_area dcr:name_area ?nameEn .
            FILTER(regex(str(?en), "%s") || regex(str(?es), "%s") && ?nameEn = "%s" || ?nameEs = "%s")
        }
        ORDER BY ?uri_comp
        """ % (nombComp, nombComp, nombArea, nombArea)
        # FILTER(regex(str(?o), "%s"))
        # Ejecuta la consulta en el Endpoint de Virtuoso
        # print('Busca\t{}, {}\nConsulta\n{}'.format(nombArea, nombComp, consulta))
        sbcEndpoint.setQuery(consulta)
        # Retorna en datos JSON
        sbcEndpoint.setReturnFormat(JSON)
        results = sbcEndpoint.query().convert()
        # print('Resultado\t{}'.format(results))

        # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
        # Lectura de JSON y division en tripletas
        # print('Triple\n')
        lista = []
        for result in results["results"]["bindings"]:
            sComp = result["uri_comp"]["value"]
            pComp = result["p"]["value"]
            compEn = result["en"]["value"]
            compEs = result["es"]["value"]
            uriArea = result["uri_area"]["value"]
            pArea = result["property"]["value"]
            areaEn = result["nameEn"]["value"]
            areaEs = result["nameEs"]["value"]
            lista.append((sComp, pComp, compEn, compEs, uriArea, pArea, areaEn, areaEs))
            # print('{} | {} | {} '.format(sComp, pComp, compEn))
            # print('{} | {} | {} '.format(uriArea, pArea, areaEn))
        return lista
        
    
    def vinculadoEntidades(self, textoEntrada: str):
        tripletaResultante = None
        ner_nel = {}
        entidadesDigcomp = []
        vinculandoText = []
        textoEntrada = textoEntrada.split('. ')
        # print('Competencia', textoEntrada)
        nombArea = textoEntrada[0]
        nombComp = textoEntrada[1]
        desComp = textoEntrada[2]
        tripletaResultante = self.anotacion(nombArea, nombComp)
        # print('Detalle competencia\t{}\nEntidad\t{}\n'.format(texto, tripletaResultante[2]))
        
        # Endpoint Realtime con Server D2RQ
        # sparqlendpoint = "http://localhost:2020/sparql"
        # Endpoint Storage con GraphDB
        sparqlendpoint ="http://localhost:7200/repositories/01"

        if tripletaResultante is not None:
            # print('URI Comp\tpComp\tCompEn\tCompEs\tURI Area\tpArea\tArea En\tArea Es')
            for triple in tripletaResultante:
                # print("Salida_:\t", triple)
                # Info de CD
                uriComp = triple[0]
                pComp = triple[1]
                compEn = triple[2]
                compEs = triple[3]
                # Info area
                uriArea = triple[4]
                pArea = triple[5]
                areaEn = triple[6]
                areaEs = triple[7]
                # print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(uriComp, pComp, compEn, compEs, uriArea, pArea, areaEn, areaEs))
                if 'localhost' in sparqlendpoint:
                    # Resolviendo URI para GraphDB
                    uriArea = uriArea.replace("http://localhost:7200/digcomp/areas/", "http://localhost:7200/resource?uri=http:%2F%2Flocalhost:7200%2Fdigcomp%2Fareas%2F")
                    uriComp = uriComp.replace("http://localhost:7200/digcomp/competences/", "http://localhost:7200/resource?uri=http:%2F%2Flocalhost:7200%2Fdigcomp%2Fcompetences%2F")
                if nombArea == areaEn or nombArea == areaEs:
                    enlace = '<a class="badge badge-info" href="' + uriArea + '" target="_blank">' + nombArea + "</a>"
                    # print("enlaceArea", enlace)
                    entidadesDigcomp.append((uriArea, areaEn))
                    vinculandoText.append(nombArea.replace(nombArea, enlace))
                if nombComp == compEn or nombComp == compEs:
                    enlace = '<a class="badge badge-info" href="' + uriComp + '" target="_blank">' + nombComp + "</a>"
                    # print("enlaceComp", enlace)
                    entidadesDigcomp.append((uriComp, compEn))
                    vinculandoText.append(nombComp.replace(nombComp, enlace))
        else:
            print("No hay resultados para este entidad")
        vinculandoText.append(desComp)
        ner_nel['entidadesDigcomp'] = entidadesDigcomp
        ner_nel['vinculacionDigcomp'] = vinculandoText
        return ner_nel

    
    def recomendacion(self, titulo: str, descripcion: str, palabraClave: str):
        # print("llega:\t", nombArea)
        # Endpoint Storage con GraphDB
        sparqlendpoint ="http://localhost:7200/repositories/02"
        sbcEndpoint = SPARQLWrapper(sparqlendpoint)

        # Consulta SPARQL para buscar en la BD la entidad encontrada
        consulta = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX oerr: <http://localhost:7200/oer/resource/>
        select * where {
            ?uri_oer ?p ?es .
            ?uri_oer a oerr:Course .
            ?uri_oer oerr:title ?title .
            ?uri_oer oerr:title ?titulo .
            ?uri_oer oerr:description ?description .
            ?uri_oer oerr:description ?descripcion .
            ?uri_oer oerr:richKeyword ?richKeyword .
            ?uri_oer oerr:richKeyword ?palabraClave .
            FILTER(regex(str(?title), "%s") || regex(str(?titulo), "%s") || regex(str(?description), "%s") || regex(str(?descripcion), "%s") || regex(str(?richKeyword), "%s") || regex(str(?palabraClave), "%s"))
        }
        ORDER BY ?uri_oer
        """ % (titulo, titulo, descripcion, descripcion, palabraClave, palabraClave)
        # print('Busca\t{}, {}, {}\nConsulta\n{}'.format(titulo, descripcion, palabraClave, consulta))
        sbcEndpoint.setQuery(consulta)
        # Retorna en datos JSON
        sbcEndpoint.setReturnFormat(JSON)
        results = sbcEndpoint.query().convert()
        # print('Resultado\t{}'.format(results))

        # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
        # Lectura de JSON y division en tripletas
        # print('Triple\n')
        lista = []
        for result in results["results"]["bindings"]:
            uri = result["uri_oer"]["value"]
            titulo = result["title"]["value"]
            descripcion = result["description"]["value"]
            recurso = {}
            recurso['uri'] = uri
            recurso['titulo'] = titulo
            recurso['descripcion'] = descripcion
            lista.append(recurso)
        return lista

    def recursosDisponibles(self):
        # Endpoint Storage con GraphDB
        # Apertura del endpoint para ejecutar la consulta
        sparqlendpoint ="http://localhost:7200/repositories/02"
        sbcEndpoint = SPARQLWrapper(sparqlendpoint)

        # Consulta SPARQL para lista recursos disponibles
        # Titulo, disciplina, URI
        consulta = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX oerr: <http://localhost:7200/oer/resource/>
        select distinct ?title ?namediscipline ?uri_oer where {
            ?uri_oer ?p ?es .
            ?uri_oer a oerr:Course .
            ?uri_oer oerr:title ?title .
            ?uri_oer oerr:hasDiscipline ?discipline .
    		?discipline rdfs:label ?namediscipline .
        }
        ORDER BY ?uri_oer
        """
        # Apertura del endpoint para ejecutar la consulta
        sbcEndpoint.setQuery(consulta)
        # Retorna en datos JSON
        sbcEndpoint.setReturnFormat(JSON)
        results = sbcEndpoint.query().convert()

        lista = []
        for result in results["results"]["bindings"]:
            titulo = result["title"]["value"]
            categoria = result["namediscipline"]["value"]
            ver_mas = result["uri_oer"]["value"]
            recurso = {}
            recurso['titulo'] = titulo
            recurso['categoria'] = categoria
            recurso['enlace'] = ver_mas
            lista.append(recurso)
            # print('recurso disponible\t', recurso)
        return lista
    
    def recursoDetallado(self, uri: str):
        """Detalle del recurso, usando la URI del mismo para buscar lo.

        Args:
            uri (str): enlace del recurso presentado
        
        Returns:
            recurso (dict): Detalle encontrado del recurso
        """        
        # Endpoint Storage con GraphDB
        # Apertura del endpoint para ejecutar la consulta
        sparqlendpoint ="http://localhost:7200/repositories/02"
        sbcEndpoint = SPARQLWrapper(sparqlendpoint)

        # Consulta SPARQL para lista recursos disponibles
        consulta = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX oerr: <http://localhost:7200/oer/resource/>
        PREFIX : <http://localhost:7200/oer/ontology/>
        select distinct ?uri_oer ?label ?o where {
            ?uri_oer ?p ?o .
            ?uri_oer a oerr:Course .
            ?p rdfs:label ?label .
            FILTER(STR(?uri_oer) = "%s")
        }
        ORDER BY ?p
        """ % (uri)
        # Apertura del endpoint para ejecutar la consulta
        sbcEndpoint.setQuery(consulta)
        # Retorna en datos JSON
        sbcEndpoint.setReturnFormat(JSON)
        results = sbcEndpoint.query().convert()

        lista = []
        for result in results["results"]["bindings"]:
            predicado = result["p"]["value"]
            objeto = result["o"]["value"]
            recurso = {}
            recurso['predicado'] = predicado
            recurso['objeto'] = objeto
            lista.append(recurso)
        return lista


    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")