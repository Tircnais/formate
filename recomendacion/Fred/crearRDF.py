import os

class PreparandoArchivos:
    def crearArchivo(self, datos, nombreArchivo):
        directorio = "./recomendacion/Fred/" + nombreArchivo + ".txt"
        archivo = open(directorio, "w")
        archivo.write(str(datos))
        # archivo.write(datos)
        archivo.close()


    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")