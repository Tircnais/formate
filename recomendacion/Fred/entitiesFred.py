from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
text = 'The input natural language text.' # String | La entrada de texto en lenguaje natural.
prefix = prefix_example # String | El prefijo utilizado para el espacio de nombres de términos introducido por FRED en la salida. Si no se especifica fred: se usa por defecto. (Opcional)
namespace = namespace_example # String | El espacio de nombres utilizado para los términos introducidos por FRED en la salida. Si no se especifica, http://www.ontologydesignpatterns.org/ont/fred/domain.owl# se utiliza de forma predeterminada. (Opcional)
wsd = true # Boolean | Realice la desambiguación del sentido de la palabra en términos de entrada. Por defecto se establece en falso. (Opcional)
wfd = true # Boolean | Realice Desambiguación de marcos de palabras en términos de entrada para proporcionar alineaciones a los sintetizadores de WordNet, Super-sentidos de WordNet y clases Dolce. Por defecto se establece en falso. (Opcional)
wfdProfile = wfdProfile_example # String | El perfil asociado con la Desambiguación del Marco de Word (opcional) (predeterminado a b)
tense = true # Boolean | Incluya relaciones temporales entre eventos de acuerdo con su tiempo gramatical. Por defecto se establece en falso. (Opcional)
roles = true # Boolean | Utilice los roles de FrameNet en la ontología resultante. Por defecto se establece en falso. (Opcional)
textannotation = textannotation_example # String | El vocabulario utilizado para anotar el texto en RDF. Hay dos posibles alternativas disponibles, es decir, EARMARK y NIF. (opcional) (predeterminado para asignar)
semanticSubgraph = true # Boolean | Genere un RDF que solo exprese la semántica de una oración sin triples RDF adicionales, como los que contienen espacios de texto, parte de discursos, etc. De manera predeterminada, se establece en falso. (Opcional)


# curl -X GET "http://wit.istc.cnr.it/stlab-tools/fred?text=Miles%20Davis%20was%20an%20american%20jazz%20musician&wfd_profile=b&textannotation=earmark" -H  "accept: application/rdf+xml" -H  "Authorization: Bearer 4dd236fa-66f1-3ab3-988c-edc52266c0d0"

try:
    api_instance.stlabToolsFredGet(text, prefix=prefix, namespace=namespace, wsd=wsd, wfd=wfd, wfdProfile=wfdProfile, tense=tense, roles=roles, textannotation=textannotation, semanticSubgraph=semanticSubgraph)
except ApiException as e:
    print("Exception when calling DefaultApi->stlabToolsFredGet: %s\n" % e)

