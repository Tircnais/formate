# se importan los modelos (BD)
from dashboard.models import *


class Funciones:
    # Funciones generica para la asignacion del recursos

    def log_error(self, donde, idComp, recursos, error):
        dictErrors = {
            'donde': donde,
            'idComp': idComp,
            'noAsigno': recursos,
            'error': error
        }
        return dictErrors
    

    def search_CompUsuario(self, idUser, idCompetencia):
        '''
        Busca la competencia digital del usuario (usando el *FK User* *ID CD*), retorna la instancia de la competencia digital del usuario si existe.
            Parametros
            ----------
                idUser (int): ID de usuario
                idCompetencia (int): ID de competencia digital
            
            Returns:
                instance: Objeto de la competencia digital del usuario buscado o None en caso no existir
        '''
        try:
            return Competenciasusuario.objects.get(fkuser=idUser, fkcompetence= idCompetencia)
        except Competenciasusuario.DoesNotExist as errorNoExiste:
            return None
    
    def update_CompUsuario(self, idUser: int, idCompetencia: int, recursos: list):
        '''
        Asigna el *Recurso Educativo Abierto (REA)* a la competencia digital del usuario si encontro o no errores y el numero total de errores. Con esto termina de la logica de procesamiento de manera que no es necesario un retorno
            Parametros
            ----------
                idUser (int): PK del usuario logeado en ese instante
                idCompetencia (int): ID de Competencia digital del Usuario a actualizar
                recursos (list): Lista de recuros sugeridos
            
            Retoorna
            ----------
                recursos (list): Lista de recuros asignados
            
        '''
        existe = self.search_CompUsuario(idUser, idCompetencia)
        # print('existe', existe.pk)
        if existe is not None:
            # encontrado
            try:
                actual = Competenciasusuario.objects.get(fkuser=idUser, fkcompetence= idCompetencia)
                # recursos = str(recursos)
                actual.recomendacion = recursos
                actual.save()
                return recursos
            except Competenciasusuario.DoesNotExist as errorNoExiste:
                error = self.log_error(donde='actualizando Competencia digital de Usuario', idComp=idCompetencia, recursos=recursos, error=str(errorNoExiste))
                print('error\n{}\nSe intentar nuevamente.'.format(error))
                self.update_CompUsuario(idUser, idCompetencia, recursos)
                # Si hay error llama a la misma funcion para actulizar se (*solo va a salir si la operacion es exitosa*)
        else:
            self.update_CompUsuario(idUser, idCompetencia, recursos)
            # Lo vuelve a buscar
        
    
    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")