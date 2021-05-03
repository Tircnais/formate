import fasttext as ftText

class generarModelo():
    def crearModelo(self, archivo):
        model = ftText.train_supervised(input=archivo, lr=0.45, dim=100, epoch=200, wordNgrams=2, ws=5, loss='softmax')
        return model
    
    def guardarModelo(self, modelo, nombreModelo):
        '''
        Guardar el modelo generado. Se usa el modelo y el nombre con el que se va a guardar (*Ej.* modelo.save("directorio") El directorio esta en la funcion)

            Parametros
            ----------
                modelo : Modelo *generado* de fastText
                nombreModelo: Nombre con el que se guarda el modelo
            
            Returns:
            ----------
                model: Modelo *guardado* fastText
        '''
        # carga el modelo guardado
        directorio = "./recomendacion/data/" + nombreModelo + ".bin"
        # print("Directorio modelo:\t", directorio)
        modeloGuardado = modelo.save_model(directorio)
        return modeloGuardado

    def cargarModelo(self, nombreModelo):
        '''
        Cargando el modelo *fastText* a usar unicamente el *nombre* sin la extension del modelo

            Parametros
            ----------
                nombreModelo : String
                    Nombre del modelo a usar
            
            Returns:
            ----------
                model: Modelo fastText
        '''
        directorio = "./recomendacion/fastText/" + nombreModelo + ".bin"
        # print("Directorio modelo:\t", directorio)
        model = ftText.load_model(directorio)
        return model

    def predecir(self, modelo, texto):
        '''
        Funcion que recibe el modelo fastText y texto. Retorna una lista con las etiquetas pronosticadas en base al modelo fastText usado

            Parametros
            ----------
                modelo: Model fastText
                text: Texto en lenguaje natural
            
            Returns:
            ----------
                model: Modelo fastText
        '''
        predicciones = modelo.predict(text=texto, k=-1, threshold=0.01)
        resultadoPredicion = []
        # print('Texto a predicir\n{}'.format(texto))
        # print("Modelo FastText Usado:\t ", modeloUsado)
        
        # print("Predicciones\n{:<10} | {:<10}".format('Etiqueta','Valoracion'))
        for etiqueta, medicion in zip(predicciones[0], predicciones[1]):
            # print("{:<10} | {:<10}".format(etiqueta, medicion))
            etiqueta = etiqueta.replace('__label__', '')
            etiqueta = etiqueta.replace('-', ' ')
            etiqueta = etiqueta.replace(',', '')
            resultadoPredicion.append((etiqueta, medicion))
        resultadoPredicion = list(dict.fromkeys(resultadoPredicion))
        # Quitar duplicados en la lista
        return resultadoPredicion

    def validarModelo(self, modeloValidar, archivoValid):
        # print("Archivo validar:\t", archivoValid)
        resultados = modeloValidar.test(archivoValid)
        return resultados

    def __del__(self):
        # Destructores, eliminar un objeto simplellamada al método:dell obj (del Objeto)
        class_name = self.__class__.__name__
        # print(class_name, "Objeto destruido")