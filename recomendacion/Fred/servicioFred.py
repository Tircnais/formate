import requests
import json
# Importando RDFLIB
from rdflib import Graph
# Importamos Lib to create file temp
import tempfile

class entitiesFred:
    """Identificacion de entidades usando FRED
    """
    def buscandoEntidades(self, mydata):
        entidadesFred = []
        if mydata is not None:
            g = Graph()
            temp = tempfile.TemporaryFile()
            with tempfile.TemporaryFile() as temp:
                # temp.write(b+''+mydata)
                temp.write(mydata)
                temp.seek(0)
                mydata = temp.read()
                print('Servicio FRED temp.name:\t',temp.name)
                # print('mydata\n',mydata)
                try:
                    # g.parse(data=mydata, format="n3")
                    g.parse(data=mydata, format="application/rdf+xml")
                except Exception:
                    raise Exception("Unexpected type '%s' for source '%s'" % (type(mydata), mydata))
            
            consultaSparql = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            SELECT Distinct?Clase WHERE {
                ?s ?p ?o .
                ?s owl:equivalentClass ?Clase .
            }
            ORDER BY ?s
            """
            # print("consultaSparql\t", consultaSparql)
            results = g.query(consultaSparql)
            # print('Results!')
            for row in results:
                #rdflib.term.URIRef('http://dbpedia.org/resource/Collaboration')
                # row = rdflib.URIRef("http://www.w3.org/People/Berners-Lee/card#i")
                row = str(row)
                row = row.replace("(rdflib.term.URIRef('", "")
                row = row.replace("'),)", "")
                # print("row\t", row)
                sbcEndpoint = SPARQLWrapper("https://dbpedia.org/sparql")
                consultaDB = """
                select Distinct?s ?o where {
                    ?s ?p ?o .
                    <%s> rdfs:label ?o .
                    Filter(?s = <%s>)
                    Filter(lang(?o) = 'en' || lang(?o) = 'es')
                }
                """ % (row, row)
                # print('consultaDB\t', consultaDB)
                sbcEndpoint.setQuery(consultaDB)
                # Retorna en datos JSON
                sbcEndpoint.setReturnFormat(JSON)
                results = sbcEndpoint.query().convert()
                for result in results["results"]["bindings"]:
                    uri = result["s"]["value"]
                    label = result["o"]["value"]
                    print("ServFred>> %s: %s" % (uri, label))
                    entidadesFred.append((uri, label))
        else:
            entidadesFred = None
        return entidadesFred

    def entidadesFred(self, text: str):
        # print('Texto a identificar\n{}'.format(text))
        # url = 'http://wit.istc.cnr.it/stlab-tools/fred'
        # url = 'http://wit.istc.cnr.it/stlab-tools/fred/?text='
        url = 'http://wit.istc.cnr.it/stlab-tools/fred?text='
        auth_token='4dd236fa-66f1-3ab3-988c-edc52266c0d0'
        # headers={'Accept': 'text/rdf+n3', 'Authorization': 'Bearer {}'.format(auth_token)}
        headers={'Accept': 'application/rdf+xml', 'Authorization': 'Bearer {}'.format(auth_token)}
        response = None
        try:
            response = requests.get(url, headers = headers)
            print("Response:\n{}\n".format(response))
            code = response.status_code
            # print('code\t{}'.format(response.content))

            # entidadesFred = response.getEntity()
            # print("Entidades FRED:\n{}\n".format(entidadesFred))
            
            respuestaFred = self.buscandoEntidades(response.content)
            # print('content\t{}'.format(respuestaFred))
            return respuestaFred
        except requests.ConnectionError as err:
            print('exceptions.ConnectionError\n', err)
            return 'err\t', err
        except requests.exceptions.ConnectionError as errC:
            print('ConnectionError\n', errC)
            return 'errC\t', errC
        except Exception as e:
            return 'e\t', e
    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")