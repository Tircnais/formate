import spotlight
import requests

class entitiesSpotlight:
    """Identificacion de entidaces usando DBpedia-spotlight
    """
    def entidadesSpotlight(self, text: str):
        """Funcion que retornar la lista de entidades encontradas usando el API (en ingles), y *annotate* la cual idenficia las entidades

        Args:
            text (str): Texto en lenguaje natural, este es que se va a enviar a procesar

        Returns:
            list: La lista contiene las entidades encontradas: URI, etiqueta, es decri, cada elemento contiene dos posiciones.
        """
        # print("Modelo FastText Usado:\t ", modeloUsado)
        # print('Texto a identificar\n{}'.format(text))
        annotations = ''
        try:
            annotations = spotlight.annotate('http://api.dbpedia-spotlight.org/en/annotate', text, confidence=0.4, support=20, spotter='Default')
        except ValueError:
            print('la respuesta JSON no se pudo decodificar.')
            # raise ValueError
        # except spotlight.SpotlightException:
        #     print('la respuesta JSON no contenía ningún campo necesario o no se formó como una excepción. Olvidó especificar explícitamente un protocolo (http / https) en la URL de la API.')
        #     raise spotlight.SpotlightException
        except requests.exceptions.HTTPError as err:
            print('Se lanza cuando el código de estado http de respuesta no era 200. Esto podría suceder si tiene un equilibrador de carga como nginx frente a su clúster destacado y no hay un solo servidor disponible, por lo que nginx arroja un 502 Bad Gateway.')
            if err.response.status_code == 403:
                return None
            else:
                raise
        except requests.exceptions.ConnectionError as error:
            print('ConnectionError\n', error)

            # if error.response.status_code == "Connection refused":
            #     return None
            # else:
            #     raise
        uris = []
        if annotations is not None:
            for elemento in annotations:
                uris.append((elemento['URI'], elemento['surfaceForm']))
                # uris.append({'URI': elemento['URI'], 'label': elemento['surfaceForm']})
                # print("similarityScore\n", elemento['similarityScore'])
                # print("percentageOfSecondRank\n", elemento['percentageOfSecondRank'])
            uris = list(dict.fromkeys(uris))
            # Quitar duplicados en la lista
        else:
            uris = None
        return uris

    
    def textoNivelConfianza(self, text: str, confianza: float):
        """Funcion que uso el *texto* y *nivel de confianza*. Retornar la lista de entidades encontradas usando el API (en ingles), y *annotate* la cual idenficia las entidades

        Args:
            text (str): Texto en lenguaje natural, este es que se va a enviar a procesar
            confianza (float): Numero decimal no mayor a 1 (0-1); siendo 1 el nivel mas alto de confianza.

        Returns:
            list: La lista contiene las entidades encontradas: URI, etiqueta, es decri, cada elemento contiene dos posiciones.
        """
        # using list comprehension to cast List to String
        # print('Texto a identificar\n{}'.format(text))
        annotations = spotlight.annotate('http://api.dbpedia-spotlight.org/en/annotate', text, confidence=confianza, support=20)
        uris = []
        for elemento in annotations:
            uris.append((elemento['URI'], elemento['surfaceForm']))
            # print("URI\n", elemento['URI'])
            # print("label\n", elemento['surfaceForm'])
            # print("similarityScore\n", elemento['similarityScore'])
            # print("percentageOfSecondRank\n", elemento['percentageOfSecondRank'])
        return uris

    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")