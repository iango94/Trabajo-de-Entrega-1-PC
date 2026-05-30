# interfaz.py
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Importamos las funciones del módulo de archivos
from archivos import cargar_y_limpiar, exportar_csv, guardar_historial, cargar_historial
# Importamos las funciones del módulo de análisis (¡Obligatorio para la nota!)
import analisis

class VentanaPrincipal(QWidget):

    def __init__(self):
        self.df = None
        super().__init__()
        self.setWindowTitle("Proyecto Dataset Diabetes - DataLab Hub")
        self.setGeometry(100, 100, 1100, 800)
        self.crear_ui()

    def crear_ui(self):
        # Layout principal
        layout_principal = QVBoxLayout()
        
        # Título
        titulo = QLabel("Proyecto Dataset Diabetes - Insulin_Logic")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(titulo)
        
        # Caja de Busqueda
        self.caja_busqueda = QLineEdit()
        self.caja_busqueda.setPlaceholderText("Ingrese un valor para buscar o filtrar (Ej: 120)")
        layout_principal.addWidget(self.caja_busqueda)
        
        # SELECTOR DE COLUMNA
        self.combo_columna = QComboBox()
        self.combo_columna.addItems(["Pregnancies", "Glucose", "BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age","Outcome"])
        layout_principal.addWidget(self.combo_columna)
        
        # AREA DE RESULTADOS
        self.area_texto = QTextEdit()
        self.area_texto.setMaximumHeight(180)
        self.area_texto.setReadOnly(True)
        layout_principal.addWidget(self.area_texto)
        
        # Botones
        layout_botones = QHBoxLayout()
        self.boton_cargar = QPushButton("Cargar Dataset")
        self.boton_buscar = QPushButton("Buscar")
        self.boton_estadisticas = QPushButton("Estadísticas")
        self.boton_filtrar = QPushButton("Filtrar")
        self.boton_historial = QPushButton("Historial")
        self.boton_exportar = QPushButton("Exportar CSV")
        self.boton_salir = QPushButton("Salir")
        
        layout_botones.addWidget(self.boton_cargar)
        layout_botones.addWidget(self.boton_buscar)
        layout_botones.addWidget(self.boton_estadisticas)
        layout_botones.addWidget(self.boton_filtrar)
        layout_botones.addWidget(self.boton_historial)
        layout_botones.addWidget(self.boton_exportar)
        layout_botones.addWidget(self.boton_salir)
        layout_principal.addLayout(layout_botones)
        
        # Área gráfica (Matplotlib embebido con 2 subplots)
        self.figura = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figura)
        layout_principal.addWidget(self.canvas)
        
        self.setLayout(layout_principal)
        
        # CONEXIÓN DE SEÑALES (Eventos)
        self.boton_cargar.clicked.connect(self.cargar_dataset)
        self.boton_buscar.clicked.connect(self.buscar)
        self.boton_estadisticas.clicked.connect(self.estadisticas)
        self.boton_filtrar.clicked.connect(self.filtrar)
        self.boton_historial.clicked.connect(self.historial)
        self.boton_exportar.clicked.connect(self.exportar)
        self.boton_salir.clicked.connect(self.close)

    # ==== FUNCIONES CONECTORAS ====
    
    def cargar_dataset(self):
        # Cambia esta ruta si tu archivo se llama diferente o está en otra carpeta
        self.df = cargar_y_limpiar("../Data/diabetes_COMPLETO.csv")
        if self.df is not None:
            self.area_texto.setText(f"Dataset cargado correctamente. Registros: {len(self.df)}")
            guardar_historial("Dataset cargado")
            self.actualizar_graficos() # Renderiza los gráficos automáticamente al cargar
        else:
            self.area_texto.setText("Error al cargar dataset. Verifique la ruta del archivo.")

    def buscar(self):
        if self.df is None:
            self.area_texto.setText("Primero cargue el dataset")
            return
        valor = self.caja_busqueda.text().strip()

        if valor == "":
            self.area_texto.setText("Ingrese un valor en la caja de texto superior para buscar")
            return
            
        # Búsqueda general en cualquier columna
        resultados = self.df[self.df.astype(str).apply(lambda fila: fila.str.contains(valor, case=False).any(), axis=1)]
        
        if len(resultados) == 0:
            self.area_texto.setText("No se encontraron coincidencias")
        else:
            self.area_texto.setText(f"Resultados encontrados ({len(resultados)}):\n" + resultados.head(20).to_string())
            guardar_historial(f"Búsqueda: {valor}")

    def estadisticas(self):
        if self.df is None:
            self.area_texto.setText("Primero cargue el dataset")
            return
        columna = self.combo_columna.currentText()
        
        # LLAMADA AL MÓDULO DE ANÁLISIS (Sin lógica interna aquí)
        res_estadisticas = analisis.obtener_estadisticas_columna(self.df, columna)
        
        self.area_texto.setText(f"Estadísticas para {columna}:\n{res_estadisticas}")
        guardar_historial(f"Estadísticas de: {columna}")

    def filtrar(self):
        if self.df is None:
            self.area_texto.setText("Primero cargue el dataset")
            return
        
        columna = self.combo_columna.currentText()
        valor_limite = self.caja_busqueda.text().strip()
        
        if not valor_limite:
            self.area_texto.setText("Escriba un valor numérico límite en la caja de texto superior para filtrar (>=).")
            return

        # LLAMADA AL MÓDULO DE ANÁLISIS
        df_filtrado = analisis.filtrar_por_condicion(self.df, columna, valor_limite)
        
        if df_filtrado is not None and not df_filtrado.empty:
            self.area_texto.setText(f"Registros que cumplen la condición ({len(df_filtrado)}):\n{df_filtrado.head(30).to_string()}")
            guardar_historial(f"Filtrado {columna} >= {valor_limite}")
        else:
            self.area_texto.setText("No se encontraron registros o el valor ingresado no es numérico.")

    def historial(self):
        df_historial = cargar_historial()
        if df_historial is not None and not df_historial.empty:
            texto = df_historial.to_string(index=False)
            self.area_texto.setText("=== HISTORIAL DE ACCIONES ===\n" + texto)
        else:
            self.area_texto.setText("No hay historial disponible")
        
    def exportar(self):
        if self.df is not None:
            nombre = "resultados/datos_exportados.csv"
            exportar_csv(self.df, nombre)
            self.area_texto.setText(f"Datos exportados exitosamente en: {nombre}")
            guardar_historial("Exportación a CSV")
        else:
            self.area_texto.setText("No hay datos cargados para exportar")

    def actualizar_graficos(self):
        """Genera los 2 gráficos solicitados usando las funciones de analisis.py"""
        self.figura.clear()
        
        # Crear los dos subplots uno al lado del otro (1 fila, 2 columnas)
        ax1 = self.figura.add_subplot(121)
        ax2 = self.figura.add_subplot(122)
        
        # Gráfico 1: Barras (Glucosa promedio por Edad)
        edades, glucosas = analisis.generar_datos_grafico_barras(self.df)
        if edades:
            # Tomamos una muestra o los primeros 15 registros para que se vea legible el gráfico de barras
            ax1.bar(edades[:15], glucosas[:15], color='teal', alpha=0.7)
            ax1.set_title("Glucosa Promedio por Edad (Muestra)")
            ax1.set_xlabel("Edad")
            ax1.set_ylabel("Glucosa")

        # Gráfico 2: Línea (BMI promedio según número de Embarazos)
        embarazos, bmis = analisis.generar_datos_grafico_linea(self.df)
        if embarazos:
            ax2.plot(embarazos, bmis, marker='o', color='crimson', linestyle='-')
            ax2.set_title("BMI Promedio vs Embarazos")
            ax2.set_xlabel("Número de Embarazos")
            ax2.set_ylabel("BMI Promedio")
            
        self.figura.tight_layout()
        self.canvas.draw()
