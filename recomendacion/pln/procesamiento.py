def anotacion(mi_entidad):
    # print("llega:\t", mi_entidad)
    llegada = mi_entidad.split("_")
    # Endpoint con Virtuoso
    sbcEndpoint = SPARQLWrapper("http://192.168.1.10:8890/sparql/")
    # Consulta SPARQL para buscar en la BD la entidad encontrada
    consulta = """
    SELECT ?s ?p ?o
    WHERE 
    { 
        ?s ?p ?o .
        FILTER (regex(str(?s), "%s") || regex(str(?o), "%s"))
    }""" % (mi_entidad, mi_entidad)
    # Ejecuta la consulta en el Endpoint de Virtuoso
    sbcEndpoint.setQuery(consulta)
    # Retorna en datos JSON
    sbcEndpoint.setReturnFormat(JSON)
    results = sbcEndpoint.query().convert()

    # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
    # Lectura de JSON y division en tripletas
    for result in results["results"]["bindings"]:
        triple = dict()
        triple['sujeto'] = result["s"]["value"]
        triple['predicado'] = result["p"]["value"]
        triple['objeto'] = result["o"]["value"]
        print(triple)
        # return triple

def entidadesEncontradas(competencia):
    # Se usa FastText
    tripleta = dict()
    tripleta = self.anotacion(competencia) # Usar un for
    print(competencia)


# Busqueda de la entidad
def tripletas_del_grafo(datos, palabra):
    # Endpoint con Virtuoso
    sbcEndpoint = SPARQLWrapper("http://192.168.56.1:8890/sparql/")
    # Consulta SPARQL para buscar en la BD la entidad encontrada
    consulta = """
        SELECT ?s ?p ?o
        WHERE 
        { 
            ?s ?p ?o .
            FILTER (regex(str(?s), "%s") || regex(str(?o), "%s"))
        }
        """ % (palabra, palabra)

    # Ejecuta la consulta en el Endpoint de Virtuoso
    sbcEndpoint.setQuery(consulta)
    # Retorna en datos JSON
    sbcEndpoint.setReturnFormat(JSON)
    results = sbcEndpoint.query().convert()

    # Dentro del JSON en el atriibuto "results" con el atributo "bindings"
    # Lectura de JSON y division en tripletas
    for result in results["results"]["bindings"]:
        triple = dict()
        triple['sujeto'] = result["s"]["value"]
        triple['predicado'] = result["p"]["value"]
        triple['objeto'] = result["o"]["value"]
        datos.append(triple)
        # print("Funcion:\t", triple)
    return datos