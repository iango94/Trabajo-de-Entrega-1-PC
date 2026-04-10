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

def menu_interactivo():
    while True:
        print("\n"¡BIENVENIDOS AL MENÚ INTERACTIVO DE INSULINE_LOGIC!"")
        print("Ingresa 1 si deseas BUSCAR")
        print("Ingresa 2 si deseas realizar ESTADÍSTICAS BÁSICAS")
        print("Ingresa 3 si deseas FILTRAR POR CONDICIÓN")
        print("Ingresa 4 si deseas SALIR DEL PROGRAMA")
        opcion = int(input("Ingresa una opción (1, 2, 3 o 4): "))
    
        match opcion:
            case 1:
                print("Elegiste BUSCAR")
            case 2:
                print("Elegiste ESTADÍSTICAS BÁSICAS")
            case 3:
                print("Elegiste FILTRAR POR CONDICIÓN")
            case 4:
                print("Elegiste SALIR DEL PROGRAMA")
                break
            case _:
                print("Opción no válida. Intenta nuevamente.")
menu()   
              
