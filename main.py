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
