def cargar_datos(nombre_archivo):
    '''Abre el archivo indicando como paramatro (solo acepta CSV) y lo retorna como una lista'''

    datos = []
    with open(nombre_archivo, "r") as archivo:
        next(archivo)  
        for linea in archivo:
            fila = linea.strip().split(",")
            datos.append(fila)
    return datos
  
mis_datos = cargar_datos("diabetes_50FILAS.csv") #carga el dataset en la variable global mis_datos
print(f"Se cargaron {len(mis_datos)} registros con éxito.")

# print(mis_datos[0]) #Linea de prueba para verificar que si cargo el dataset (dejar comentado)

def buscar():
    '''
        busca un valor en el dataset e imprime todas las columnas que lo contienen junto con la cantidad de veces que se encontro
        permite elegir si buscar coincidencias exactas o cualquier coincidencia
    '''

    global mis_datos

    #tomar entradas del usuario
    busqueda = []
    a = input("digite criterio busqueda: ")
    b = input("digite 1 para busqueda exacta y 2 para busqueda extendida: ")
    
    #realizar busquedas y agregar coincidencias a nueva lista
    if b == "1": 
        for linea in mis_datos:
            for celda in linea:
                try:
                    if float(a) == float(celda):
                        busqueda.append(linea)
                        break
                except:
                    continue
    else:
        for linea2 in mis_datos:
            r = " ".join(linea2)
            x = r
            if a in x:
                busqueda.append(linea2)

    
    #Imprimir resultados y numero de coincidencias totales
    print(f"Se encontraron {len(busqueda)} resultados") 

    for linea in busqueda:
        print(linea)

def estadísticas_basicas():
    '''imprime el valor maximo, minimo y promedio de la columna selecionada'''

    global mis_datos

    print("\n--- ESTADÍSTICAS BÁSICAS ---")
    print("Ingrese un número de acuerdo a la columna que desea analizar:")
    print("0: Embarazos")
    print("1: Glucosa")
    print("2: Presión arterial")
    print("3: Grosor de la piel")
    print("4: Insulina")
    print("5: IMC")
    print("6: Función de pedigrí de diabetes")
    print("7: Edad")
    print("8: Resultado")

    columna=int(input("Elige el número de columna: "))

    maximo = None
    minimo = None
    suma = 0
    contador = 0

    for fila in mis_datos:
        try:
            valor = float(fila[columna])
        except:
            continue

        if maximo is None or valor > maximo:
            maximo = valor
        if minimo is None or valor < minimo:
            minimo = valor 

        suma += valor 
        contador += 1

    if contador > 0:
        promedio = suma/contador
        print(f"Máximo: {maximo} · Mínimo: {minimo} · Promedio: {round(promedio,1)}")
    else:
        print("No hay datos en la columna")



def filtro():
    '''
        filtra los datos encontrando los valores de una columna mayores al valor 
        que ingrese el usuario.
    '''

    global mis_datos

    filtro_l = [] #cambie de filtro a filtro_l para evitar colision en la llamada recursiva

    print('Digite el numero de acuerdo a la columna la que desea filtrar: ')
    print("0: Embarazos")
    print("1: Glucosa")
    print("2: Presión arterial")
    print("3: Grosor de la piel")
    print("4: Insulina")
    print("5: IMC")
    print("6: Función de pedigrí de diabetes")
    print("7: Edad")
    print("8: Resultado")
    x = int(input())
    if x in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        y = int(input('Digite desde que valor desea filtrar: '))
        for fila in mis_datos:
            try:
                if float(fila[x]) >= y:
                    filtro_l.append(fila)
            except:
                continue
    else:
        print('Digite un numero valido')
        filtro() #llama recursivamente hasta que el usuario digite un numero correcto

    filtro_l.sort(key=lambda a: a[x])

    print(f'Se filtraron {len(mis_datos)-len(filtro_l)} resultados')
    for linea in filtro_l:
        print(linea)


            
def menu_interactivo():
    '''
        crea un menu que permite al usuario elegir la operacion deseada sobre el dataset 
        o cerrar el programa
    '''
    while True:
        print("\n BIENVENIDOS AL MENÚ INTERACTIVO DE INSULINE_LOGIC!")
        print("Ingresa 1 si deseas BUSCAR")
        print("Ingresa 2 si deseas realizar ESTADÍSTICAS BÁSICAS")
        print("Ingresa 3 si deseas FILTRAR POR CONDICIÓN")
        print("Ingresa 4 si deseas SALIR DEL PROGRAMA")
        opcion = int(input("Ingresa una opción (1, 2, 3 o 4): "))
    
        match opcion:
            case 1:
                print("Elegiste BUSCAR")
                buscar()
            case 2:
                print("Elegiste ESTADÍSTICAS BÁSICAS")
                estadísticas_basicas()
            case 3:
                print("Elegiste FILTRAR POR CONDICIÓN")
                filtro()
            case 4:
                print("Elegiste SALIR DEL PROGRAMA")
                break
            case _:
                print("Opción no válida. Intenta nuevamente.")


menu_interactivo() #llamada a la funcion menu (menu_interctivo) que permite acceder a todas las demas funciones y es un ciclo que solo termina cuando el usuario lo indica


