
# Aqui se almacenan las funciones que se reusan pero no hacen parte directa de la logica
import datetime as dt
import csv
import json
import os
import pandas as pd

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def guardar_historial(opcion: int, valor, resultados):
    """
    Correcciones realizadas:
        se movio la funcion de main.py a utilidades.py
        se cambio el if-elif-else por un match->case (No es recomendable usar if en cadenas de mas de 3 opciones)
        se agrego un caso por defecto al match->case que levanta un error indicando que no existe ese caso
        se movio la apertura del archivo hasta despues del match->case (El archivo debe abrirse y cerrarce en el menor numero de operaciones posibles)
    """
    
    match opcion:
        case 1:
            t = 'Cargar dataset'
        case 2:
            t = 'Buscar coincidencia'
        case 3:
            t = 'Estadisticas basicas'
        case 4:
            t = 'Filtrar por'
        case 5:
            t = 'Seleccion dataset'
        case '2':
            t = 'Pacientes en riesgo'
        case '3':
            t = 'Guardar filtro'
        case '4':
            t = 'Cargar resultados'
        case '5':
            t = 'Visualizar historial'
        case '6':
            t = 'Funcionalidad opcional'
        case _:
            raise ValueError("Opcion no definida")
    

    resultados = str(resultados) + " resultados"
    
    cadena = [dt.datetime.now().strftime("%Y-%m-%d %H:%M"), t, valor, resultados]

    with open(os.path.join(DIR, "resultados/historial.csv"), mode='a', encoding='utf-8') as hist:

        guardar = csv.writer(hist, delimiter=",")
        guardar.writerow(cadena)

def guardar_dataset(datos):
    while True:
        archivo = input("Digite el nombre del archivo a guardar sin extension: ")
        if "." in archivo:
            print("No utilice puntos ni caracteres especiales")
            continue
        else:
            archivo += ".csv"
            ruta = os.path.join(DIR, f"resultados\\{archivo}")
            with open(ruta, mode='w', newline='', encoding='utf-8') as busqueda:
                headers = list(datos[0].keys())
                #print(headers) #Linea de prueba
                wr = csv.DictWriter(busqueda, headers, delimiter=",")
                wr.writeheader()
                wr.writerows(datos)
                return True
        return False

def guardar_stadisticas_dataset(datos):
    ruta = os.path.join(DIR, f"resultados\\resumen.json")
    
    with open(ruta, 'w', encoding='utf-8') as aw:
        json.dump(datos, aw, indent=4)

# analisis.pY
def obtener_estadisticas_columna(df, columna):
    """Retorna las estadísticas básicas de una columna."""
    if df is None or columna not in df.columns:
        return "No hay datos o la columna no existe."
    return df[columna].describe().to_string()

def filtrar_por_condicion(df, columna, valor_limite):
    """Filtra las filas donde la columna sea mayor o igual al valor límite."""
    if df is None or columna not in df.columns:
        return None
    try:
        limite = float(valor_limite)
        # Filtramos
        resultado = df[df[columna] >= limite]
        # Lo ordenamos como lo hacía tu código original
        resultado = resultado.sort_values(by=columna)
        return resultado
    except ValueError:
        return None

def generar_datos_grafico_barras(df):
    """Calcula la glucosa promedio por rango de edad (reemplazo de sismos por departamento)."""
    if df is None:
        return None, None
    # Agrupamos por edad y sacamos promedio de Glucosa
    agrupado = df.groupby('Age')['Glucose'].mean().reset_index()
    return agrupado['Age'].tolist(), agrupado['Glucose'].tolist()

def generar_datos_grafico_linea(df):
    """Calcula el BMI promedio por nivel de embarazo (reemplazo de sismos por mes)."""
    if df is None:
        return None, None
    # Agrupamos por cantidad de embarazos (Pregnancies) y sacamos promedio de BMI
    agrupado = df.groupby('Pregnancies')['BMI'].mean().reset_index()
    return agrupado['Pregnancies'].tolist(), agrupado['BMI'].tolist()
    
        
