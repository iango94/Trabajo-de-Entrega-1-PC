def cargar_datos(nombre_archivo):
    datos = []
    with open(nombre_archivo, "r") as archivo:
        next(archivo)  
        for linea in archivo:
            fila = linea.strip().split(",")
            datos.append(fila)
    return datos
  
mis_datos = cargar_datos("diabetes_50FILAS.csv")
print(f"Se cargaron {len(mis_datos)} registros con éxito.")
print(mis_datos[0])

def buscar():
    busqueda = []
    a = input("digite criterio busqueda: ")
    b = input("digite 1 para busqueda exacta y 2 para busqueda extendida: ")
    
    if b == "1": 
        print("jjhjh")
        for linea in mis_datos:
            for celda in linea:
                if float(a) == float(celda):
                    busqueda.append(linea)
                    break
    else:
        for linea2 in mis_datos:
            r = " ".join(linea2)
            x = r
            if a in x:
                busqueda.append(linea2)

    print(f"Se encontraron {len(busqueda)} resultados")

    for linea in busqueda:
        print(linea)



def menu_interactivo():
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
            case 3:
                print("Elegiste FILTRAR POR CONDICIÓN")
            case 4:
                print("Elegiste SALIR DEL PROGRAMA")
                break
            case _:
                print("Opción no válida. Intenta nuevamente.")


menu_interactivo()

