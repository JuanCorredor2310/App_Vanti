from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QPushButton, QScrollArea, QLineEdit
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import QEventLoop, QSize, Qt
import ruta_principal as mod_rp
import json
from datetime import datetime

global ruta_principal, ruta_codigo, ruta_constantes, rutanuevo_sui, ruta_archivos, ruta_fuentes, ruta_imagenes, fuente_texto, azul_vanti, dic_colores, nombre_aplicativo, lista_anios, dic_meses, lista_meses, lista_trimestres,reportes_disponibles,fecha_actual,lista_carpetas_extra,dic_DANE_nombres,dic_DANE_nombres_inicio
global ruta_fuente, grupo_vanti, ruta_fuente_negrilla
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
ruta_fuentes = mod_rp.v_fuentes()
ruta_imagenes = mod_rp.v_imagenes()
grupo_vanti = "Grupo Vanti"
ruta_fuente = ruta_fuentes + "Muli.ttf"
ruta_fuente_negrilla = ruta_fuentes + "Muli-Bold.ttf"
nombre_aplicativo = "App Vanti"
def leer_archivos_json(archivo):
    with open(archivo) as file:
            data = json.load(file)
    return data
dic_colores = leer_archivos_json(ruta_constantes+"colores.json")["datos"]
lista_carpetas_extra = leer_archivos_json(ruta_constantes+"carpetas_extra.json")["carpeta_2"]
lista_anios = list(leer_archivos_json(ruta_constantes+"anios.json")["datos"].values())
dic_meses = leer_archivos_json(ruta_constantes+"tabla_18.json")["datos"]
lista_meses = list(dic_meses.values())
lista_trimestres = list(leer_archivos_json(ruta_constantes+"trimestres.json")["datos"].values())
reportes_disponibles = leer_archivos_json(ruta_constantes+"reportes_disponibles.json")["datos"]
fecha_actual = datetime.now()
dic_DANE_nombres = leer_archivos_json(ruta_constantes+"mercado_relevante_DANE_nombres.json")
dic_DANE_nombres_inicio = leer_archivos_json(ruta_constantes+"mercado_relevante_DANE_nombres_inicio.json")

def crear_label(texto, central_widget, font="normal", color="white", font_size=30, background_color="#030918", line_edit=False):
    if line_edit:
        label = QLineEdit("", central_widget)
        label.setPlaceholderText(texto)
        label.setFixedWidth(800)
    else:
        label = QLabel(texto, central_widget)
    label.setStyleSheet(f"color: {color}; background-color: {background_color};")
    if font == "normal":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    elif font == "bold":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    label.setFont(QFont(font_family, font_size))
    return label

def crear_cuadro(central_widget, dimensiones, color="white", size=0.7):
    screen_width, screen_height = dimensiones
    largo_x = int(screen_width * size)
    largo_y = int(screen_height * size)
    ubi_x = int((screen_width-largo_x)/2)
    ubi_y = int((screen_height-largo_y)/2)
    cuadro = QLabel("", central_widget)
    cuadro.setStyleSheet(f"background-color: {color};")
    cuadro.setGeometry(ubi_x, ubi_y, largo_x, largo_y)
    return cuadro

def crear_boton(texto, central_widget, font="normal", color=dic_colores["azul_v"], font_size=32, padding=20, radius = 15):
    boton = QPushButton(texto, central_widget)
    if font == "normal":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    elif font == "bold":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    boton.setStyleSheet(f"""QPushButton {{color: {color};padding: {padding}px;font-size: {font_size}px;
                            border: 0.5px solid white;border-radius: {radius}px;font-family: '{font_family}';background-color: #ffffff;}}""")
    return boton

def crear_label_imagen(ruta, central_widget):
    logo_label = QLabel(central_widget)
    logo_label.setPixmap(QPixmap(ruta))
    return logo_label

def mostrar_label(label):
    label.show()

def esconder_label(label):
    label.hide()

def calcular_factor_escala(screen_width, screen_height, base_width=1920, base_height=1200):
    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    return min(scale_x, scale_y)

def escalar_valor(valor, factor_escala):
    return round(valor * factor_escala)

def escalar_icono(pixmap, ancho_deseado, alto_deseado, factor_escala):
    ancho_escalado = escalar_valor(ancho_deseado, factor_escala)
    alto_escalado = escalar_valor(alto_deseado, factor_escala)
    return pixmap.scaled(
        ancho_escalado, 
        alto_escalado, 
        aspectRatioMode=1,
        transformMode=Qt.SmoothTransformation)

def escalar_qsize(size, factor_escala):
    return QSize(
        escalar_valor(size.width(), factor_escala),
        escalar_valor(size.height(), factor_escala)
    )

def crear_pantalla_incial():
    app = QApplication([])
    app.setWindowIcon(QIcon(ruta_imagenes+"vanti_logo.ico"))
    window = QMainWindow()
    window.setWindowIcon(QIcon(ruta_imagenes+"vanti_logo.ico"))
    central_widget = QWidget(window)
    central_widget.setStyleSheet("background-color: #030918;")
    window.setCentralWidget(central_widget)
    screen = app.primaryScreen()
    screen_size = screen.size()
    screen_width = screen_size.width()
    screen_height = screen_size.height()
    dimensiones = (screen_width, screen_height)

    factor_escala = calcular_factor_escala(screen_width, screen_height)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"vanti.png")
    nuevo_ancho = escalar_valor(320, factor_escala)
    nuevo_alto = escalar_valor(80, factor_escala)
    pixmap = pixmap.scaled(nuevo_ancho, nuevo_alto, aspectRatioMode=1)
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(int(screen_width-image_button.sizeHint().width())-20,int(screen_height-image_button.sizeHint().height())-20)
    mostrar_label(image_button)
    window.setCentralWidget(central_widget)
    window.setWindowTitle(nombre_aplicativo)
    #window.setGeometry(100, 100, 300, 200)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0x03, 0x09, 0x18))
    window.setPalette(palette)
    window.setStyleSheet("""QWidget {background-color: #030918;}
                        QLabel {margin: 20px;}""")
    window.showMaximized()
    window.show()
    return app, window, central_widget, dimensiones

def pantalla_inicio(app, window, central_widget, dimensiones):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)

    app_vanti = crear_label("APP VANTI", central_widget, font="bold", font_size=100)
    x = round((screen_width-app_vanti.sizeHint().width())*0.5)-50
    app_vanti.move(x, escalar_valor(100, factor_escala))
    mostrar_label(app_vanti)
    titulo_1 = crear_label("Vicepresidencia de Estrategia y Finanzas", central_widget, font_size=50)
    x = round((screen_width-titulo_1.sizeHint().width())*0.5)
    titulo_1.move(x, escalar_valor(400, factor_escala))
    mostrar_label(titulo_1)
    titulo_2 = crear_label("Dirección Regulación, Márgenes y Tarifas", central_widget, font_size=35)
    x = round((screen_width-titulo_2.sizeHint().width())*0.5)
    titulo_2.move(x, escalar_valor(650, factor_escala))
    mostrar_label(titulo_2)
    button = crear_boton("INICIAR", central_widget, font_size=80, font="bold")
    x = round((screen_width-button.sizeHint().width())*0.5)
    button.move(x,escalar_valor(900, factor_escala))
    button.setParent(central_widget)
    mostrar_label(button)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"vanti_logo.png")
    logo_size = escalar_valor(155, factor_escala)
    pixmap = pixmap.scaled(logo_size, logo_size, aspectRatioMode=1)
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(1400, factor_escala),escalar_valor(165, factor_escala))
    mostrar_label(image_button)

    event_loop = QEventLoop()
    def on_button_clicked():
        event_loop.quit()
        esconder_label(app_vanti)
        esconder_label(titulo_1)
        esconder_label(titulo_2)
        esconder_label(button)
        esconder_label(image_button)
    button.clicked.connect(on_button_clicked)
    event_loop.exec_()

def menu_inicial(app, window, central_widget, dimensiones, estado=None, info=None):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)

    titulo = "INICIO"
    label_1 = crear_label(titulo, central_widget, font="bold", font_size=100)
    x = round((screen_width-label_1.sizeHint().width())*0.5)
    label_1.move(x, escalar_valor(35, factor_escala))
    mostrar_label(label_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(size)
    long = escalar_valor(20, factor_escala)
    image_button.move(long,long)
    mostrar_label(image_button)
    boton_1 = crear_boton("Configuración inicial", central_widget, font_size=45)
    boton_2 = crear_boton("Herramientas de trabajo", central_widget, font_size=45)
    boton_3 = crear_boton("Reportes comerciales", central_widget, font_size=45)
    boton_4 = crear_boton("Reportes tarifarios", central_widget, font_size=45)
    boton_5 = crear_boton("Reportes técnicos", central_widget, font_size=45)
    boton_6 = crear_boton("KPIs", central_widget, font_size=45)
    boton_7 = crear_boton("Dashboard", central_widget, font_size=70)
    botones = [boton_1, boton_2, boton_3, boton_4, boton_5, boton_6, boton_7]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width+60)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,escalar_valor(400, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,escalar_valor(600, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_5.move(x,escalar_valor(800, factor_escala))
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,escalar_valor(400, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,escalar_valor(600, factor_escala))
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    boton_6.move(x,escalar_valor(800, factor_escala))
    boton_6.setParent(central_widget)
    mostrar_label(boton_6)
    x = round((((screen_width)-max_width)*0.5))
    boton_7.move(x,escalar_valor(1000, factor_escala))
    boton_7.setParent(central_widget)
    mostrar_label(boton_7)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    long = escalar_valor(80, factor_escala)
    image_button_1.setIconSize(QSize(long, long))  # Ajusta el tamaño del ícono
    long = escalar_valor(150, factor_escala)
    image_button_1.setFixedSize(long, long)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    image_button_2 = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"vanti_logo.png")
    long = escalar_valor(140, factor_escala)
    pixmap = pixmap.scaled(long,long, aspectRatioMode=1)
    icon = QIcon(pixmap)
    image_button_2.setIcon(icon)
    image_button_2.setIconSize(pixmap.size())
    image_button_2.move(escalar_valor(1260, factor_escala),escalar_valor(115, factor_escala))
    mostrar_label(image_button_2)

    dic_texto = {"Configuración inicial":"Configuración del aplicativo. Recomendado si no existen las carpetas o archivos necesarios en el dispositivo",
                "Herramientas de trabajo":"Almacenamiento, manipulación o estandarización de archivos",
                "Reportes comerciales":"Actividades con reportes comerciales como información por sectores de consumo, información por sectores de consumo subsidiadios,\ncompensaciones, desviaciones significativas, reporte DANE, reporte Secretaria de Hacienda de Bogotá D.C.\nComprobación de la calidad de la información o comparación entre archivos de certificación, calidad (CLD) y/o producción (PRD)",
                "Reportes tarifarios":"Actividades con reportes tarifarios\n",
                "Reportes técnicos":"Actividades con reportes técnicos como indicadores técnicos (IPLI,IO,IRST-EG) o\nreporte de suspensiones",
                "KPIs":"KPIs y/o indicadores de cumplimientos de reportes regulatorios como porcentaje de atención a solicitudes,\nreportes trimestrales, matriz de requerimientos, gastos AOM, pagos contribuciones MME o\ntarifas distribuidoras de GN en Colombia",
                "Dashboard":"Creación y almacenamiento slides Dashboard "}
    event_loop = QEventLoop()
    def on_button_clicked(evento):
        nonlocal estado, info
        event_loop.quit()
        esconder_label(label_1)
        esconder_label(image_button)
        esconder_label(image_button_1)
        esconder_label(image_button_2)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(boton_5)
        esconder_label(boton_6)
        esconder_label(boton_7)
        if evento == "volver":
            pantalla_inicio(app, window, central_widget, dimensiones)
        elif evento == "config_inicial":
            estado, info = menu_config_inicial(app, window, central_widget, dimensiones)
        elif evento == "edicion_archivos":
            estado, info = menu_edicion_archivos(app, window, central_widget, dimensiones)
        elif evento == "reportes_comerciales":
            estado, info = menu_reportes_comerciales(app, window, central_widget, dimensiones)
        elif evento == "reportes_tarifarios":
            estado = evento
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_inicial", estado, c_meses=12)
        elif evento == "reportes_tecnicos":
            estado,info = menu_reportes_tecnicos(app, window, central_widget, dimensiones)
        elif evento == "KPIs":
            estado, info = menu_KPIs(app, window, central_widget, dimensiones)
        elif evento == "dashboard":
            estado = evento
            estado, info = menu_dashboard(app, window, central_widget, dimensiones, estado=estado)
        else:
            pantalla_inicio(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("config_inicial"))
    boton_2.clicked.connect(lambda:on_button_clicked("edicion_archivos"))
    boton_3.clicked.connect(lambda:on_button_clicked("reportes_comerciales"))
    boton_4.clicked.connect(lambda:on_button_clicked("reportes_tarifarios"))
    boton_5.clicked.connect(lambda:on_button_clicked("reportes_tecnicos"))
    boton_6.clicked.connect(lambda:on_button_clicked("KPIs"))
    boton_7.clicked.connect(lambda:on_button_clicked("dashboard"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto, dimensiones=dimensiones))
    event_loop.exec_()
    return estado, info

def menu_config_inicial(app, window, central_widget, dimensiones, estado=None, info={}):
    estado = None
    info = {}

    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Configuración inicial"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    mostrar_label(titulo_espacios)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    long = escalar_valor(80, factor_escala)
    image_button_1.setIconSize(QSize(long, long))
    long = escalar_valor(150, factor_escala)
    image_button_1.setFixedSize(long, long)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Creación de espacio de trabajo":"Creación de las carpetas necesarias para el correcto funcionamiento del aplicativo.\nCreación y/o actualización de constantes como tablas, archivos o imágenes usados por el aplicativo.",
                "Agregar año actual":"Incluir el año actual a la información generada (archivos y carpetas) por el aplicativo.\nSe debe ejecutar está función al inicio de cada año",
                "Editar un reporte existente":"Edición de archvios de tipo .json\nEstos archivos representan las reglamentaciones utilizadas por cada reporte de la SSPD  según el lineamiento específico.",
                "Crear un nuevo reporte":"Creación de un nuevo tipo de reporte a utilizar (creación de un archivo .json a partir de un archivo _json.xlsx)\n"}
    boton_1 = crear_boton("Creación de espacio de trabajo", central_widget)
    boton_2 = crear_boton("Agregar año actual", central_widget)
    boton_3 = crear_boton("Editar un reporte existente", central_widget)
    boton_4 = crear_boton("Crear un nuevo reporte", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,escalar_valor(500, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,escalar_valor(800, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,escalar_valor(500, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,escalar_valor(800, factor_escala))
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado
        nonlocal info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(image_button_1)
        estado_anterior = "menu_config_inicial"
        if texto == "volver":
            estado, info = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "crear_carpetas":
            op = texto
            texto = "Creación de carpetas y constantes"
            estado, info = confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op, estado_anterior)
        elif texto == "agregar_anio":
            op = texto
            texto = f"Agregar año actual ({fecha_actual.year})"
            estado, info = confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op, estado_anterior)
        elif texto == "editar_reporte":
            estado, info = seleccionar_reporte(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="menu_inicial")
        elif texto == "agregar_reporte":
            estado, info = seleccionar_categoria(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="menu_inicial")
        else:
            estado, info = menu_inicial(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("crear_carpetas"))
    boton_2.clicked.connect(lambda:on_button_clicked("agregar_anio"))
    boton_3.clicked.connect(lambda:on_button_clicked("editar_reporte"))
    boton_4.clicked.connect(lambda:on_button_clicked("agregar_reporte"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado, info

def menu_edicion_archivos(app, window, central_widget, dimensiones, estado=None, info={}):
    estado = None
    info = {}

    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Herramientas de trabajo"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    mostrar_label(titulo_espacios)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Conversión archivos .txt a .csv":"Convesión de archivos .txt a .csv en un ubicación seleccionada",
                "Almacenar archivos":"Almacenamiento de archivos en la carpeta \'Guardar_archivos\' en el formato del aplicativo\nEl formato necesario es: \'Reporte_Filial_Año_Mes\'",
                "Estandarización de cabeceras":"Generación de archivos de tipo _form_estandar.csv\nEstos archivos contienen las columnas escritas según la información del lineamiento y los archivos .json",
                "Generar archivos resumen":"Generación de archivos de tipo _resumen.csv\nEstos archivos contienen las columnas escritas según la información del lineamiento y los archivos .json",
                "Revisión de archivos existentes":"Revisión de los archivos disponibles en las carpetas con el fin de conocer la información\nalmacenada y disponible para el procesamiento del aplicativo",
                "Revisión de reportes existentes":"Revisión de los reportes disponibles y aceptados por el aplicativo según los archivos .json\n",
                "Búsqueda de carpetas comprimidas (.zip)":"Búsqueda de carpetas comprimidas (.zip) en las carpetas de los reportes (NUEVO SUI)\n"}
    boton_1 = crear_boton("Conversión archivos .txt a .csv", central_widget)
    boton_2 = crear_boton("Almacenar archivos", central_widget)
    boton_3 = crear_boton("Estandarización de cabeceras", central_widget)
    boton_4 = crear_boton("Generar archivos resumen", central_widget)
    boton_5 = crear_boton("Revisión de archivos existentes", central_widget)
    boton_6 = crear_boton("Revisión de reportes existentes", central_widget)
    boton_7 = crear_boton("Búsqueda de carpetas comprimidas (.zip)", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4, boton_5, boton_6, boton_7]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,escalar_valor(400, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,escalar_valor(600, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_5.move(x,escalar_valor(800, factor_escala))
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,escalar_valor(400, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,escalar_valor(600, factor_escala))
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    boton_6.move(x,escalar_valor(800, factor_escala))
    boton_6.setParent(central_widget)
    mostrar_label(boton_6)
    x = round((screen_width-boton_7.sizeHint().width())*0.5)
    boton_7.move(x,escalar_valor(1000, factor_escala))
    boton_7.setParent(central_widget)
    mostrar_label(boton_7)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado, info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(boton_5)
        esconder_label(boton_6)
        esconder_label(boton_7)
        esconder_label(image_button_1)
        if texto == "volver":
            estado, info = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "almacenar_archivos":
            estado = texto
        elif texto == "convertir_archivos":
            estado = texto
            estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado=estado, estado_anterior="menu_edicion_archivos")
        elif texto == "archivos_estandar":
            estado = texto
            estado, info = menu_seleccion(app, window, central_widget, dimensiones, estado=estado, estado_anterior="menu_edicion_archivos", c_meses=12)
        elif texto == "archivos_resumen":
            estado = texto
            estado, info = menu_seleccion(app, window, central_widget, dimensiones, estado=estado, estado_anterior="menu_edicion_archivos, c_meses=12")
        elif texto == "archivos_existentes":
            estado = texto
            estado, info = menu_seleccion(app, window, central_widget, dimensiones, estado=estado, estado_anterior="menu_edicion_archivos", c_meses=12)
        elif texto == "reportes_existentes":
            estado = texto
            estado, info = menu_dashboard(app, window, central_widget, dimensiones, estado=estado, estado_anterior="menu_edicion_archivos")
        elif texto == "busqueda_carpetas_comprimidas":
            estado = texto
        else:
            estado, info = menu_inicial(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("convertir_archivos"))
    boton_2.clicked.connect(lambda:on_button_clicked("almacenar_archivos"))
    boton_3.clicked.connect(lambda:on_button_clicked("archivos_estandar"))
    boton_4.clicked.connect(lambda:on_button_clicked("archivos_resumen"))
    boton_5.clicked.connect(lambda:on_button_clicked("archivos_existentes"))
    boton_6.clicked.connect(lambda:on_button_clicked("reportes_existentes"))
    boton_7.clicked.connect(lambda: on_button_clicked("busqueda_carpetas_comprimidas"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado, info

def menu_reportes_comerciales(app, window, central_widget, dimensiones, estado=None, info={}):
    estado = None
    info = {}

    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Reportes comerciales"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    mostrar_label(titulo_espacios)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Reporte comercial por sector de consumo":"Reportes comerciales por sector de consumo. La información puede incluir el consumo de GN por cada sector, total de usuarios, filtrar la información por código DANE,\ncantidad total de facturas emitidas, valor facturado por consumo y/o facturación total ",
                "Reporte comercial para compensaciones":"Reporte comercial para compensaciones. El reporte puede contener los datos del inventario de suscriptores\ncon el fin de obtener información adicional de los usuarios compensados",
                "Desviaciones significativas":"Reporte de la información y comportamiento de las desviaciones significativas obtenidas en las mediciones realizadas\ndel consumo de GN de los usuarios",
                "Comprobación de la calidad de la información":"Comprobación de la calidad de la información para los reportes comerciales, con el fin de identificar posibles errores\no discrepacancias en los datos previa a la certificación de reportes",
                "Reportes DANE":"Generación de reportes por sector de consumo para ser presentado\nante el Departamento Administrativo Nacional de Estadística",
                "Reportes SH (Secretaria de Hacienda de Bogotá D.C.)":"Generación de reportes del inventario de suscriptores y su información asociada para la ciudad de Bogotá D.C.",
                "Comparación entre archivos de certificación, calidad (CLD) y/o producción (PRD)":"Comparación de los reportes comerciales, obtenidos en la plataforma SAP,\nen las áreas de Calidad, Certificación y Producción de la plataforma"}
    boton_1 = crear_boton("Reporte comercial por sector de consumo", central_widget)
    boton_2 = crear_boton("Reporte comercial para compensaciones", central_widget)
    boton_3 = crear_boton("Desviaciones significativas", central_widget)
    boton_4 = crear_boton("Comprobación de la calidad de la información", central_widget)
    boton_5 = crear_boton("Reportes DANE", central_widget)
    boton_6 = crear_boton("Reportes SH (Secretaria de Hacienda de Bogotá D.C.)", central_widget)
    boton_7 = crear_boton("Comparación archivos de certificación, CLD y PRD", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4, boton_5, boton_6, boton_7]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,escalar_valor(400, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,escalar_valor(600, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_5.move(x,escalar_valor(800, factor_escala))
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,escalar_valor(400, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,escalar_valor(600, factor_escala))
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    boton_6.move(x,escalar_valor(800, factor_escala))
    boton_6.setParent(central_widget)
    mostrar_label(boton_6)
    x = round((((screen_width)-max_width)*0.5))
    boton_7.move(x,escalar_valor(1000, factor_escala))
    boton_7.setParent(central_widget)
    mostrar_label(boton_7)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado, info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(boton_5)
        esconder_label(boton_6)
        esconder_label(boton_7)
        esconder_label(image_button_1)
        if texto == "volver":
            estado,info = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "reporte_comercial":
            estado,info = menu_reporte_comercial(app, window, central_widget, dimensiones, estado, info)
        elif texto == "reporte_compensaciones":
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reportes_comerciales", estado, info, c_meses=12)
        elif texto == "desviaciones_significativas":
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reportes_comerciales", estado, info, c_meses=12)
        elif texto == "reporte_DANE":
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reportes_comerciales", estado, info, incluir_anual=False)
        elif texto == "reporte_SH":
            estado = texto
            estado,info = seleccionar_periodo(app, window, central_widget, dimensiones, estado, info, "menu_reportes_comerciales", incluir_anual=False, c_meses=12)
        elif texto == "comparacion_CER_CLD_PRD":
            estado = texto
            estado,info = menu_CLD_PRD(app, window, central_widget, dimensiones, estado, info, estado_anterior="menu_reportes_comerciales")
        elif texto == "calidad_informacion":
            estado = texto
            estado,info = menu_comercial_calidad_info(app, window, central_widget, dimensiones, estado, info, estado_anterior="menu_reportes_comerciales")
        else:
            estado,info = menu_inicial(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("reporte_comercial"))
    boton_2.clicked.connect(lambda:on_button_clicked("reporte_compensaciones"))
    boton_3.clicked.connect(lambda:on_button_clicked("desviaciones_significativas"))
    boton_4.clicked.connect(lambda:on_button_clicked("calidad_informacion"))
    boton_5.clicked.connect(lambda:on_button_clicked("reporte_DANE"))
    boton_6.clicked.connect(lambda:on_button_clicked("reporte_SH"))
    boton_7.clicked.connect(lambda:on_button_clicked("comparacion_CER_CLD_PRD"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado,info

def menu_reporte_comercial(app, window, central_widget, dimensiones, estado=None, info={}):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)

    titulo = "Reportes comerciales\npor sector de consumo"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Todos los sectores de consumo":"Reportes comerciales para todos los sectores de consumo. La información puede incluir el consumo de GN por cada sector, total de usuarios,\nfiltrar la información por código DANE, cantidad total de facturas emitidas, valor facturado por consumo y/o facturación total ",
                "Sectores de consumo con subsidios o contribuciones":"Reportes comerciales para los sectores de consumo con subsidios o contribuciones. La información puede incluir el consumo de GN por cada sector, total de usuarios,\nfiltrar la información por código DANE, cantidad total de facturas emitidas, valor facturado por consumo y/o facturación total "}
    boton_1 = crear_boton("Todos los sectores de consumo", central_widget)
    boton_2 = crear_boton("Sectores de consumo con subsidios\no contribuciones", central_widget)
    botones = [boton_1, boton_2]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,escalar_valor(700, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,escalar_valor(700, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado
        nonlocal info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(image_button_1)
        if texto == "volver":
            estado,info = menu_reportes_comerciales(app, window, central_widget, dimensiones)
        elif texto == "reporte_comercial_sector_consumo":
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reporte_comercial", estado, info)
        elif texto == "reporte_comercial_sector_consumo_subsidio":
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reporte_comercial", estado, info, c_meses=12)
        else:
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reporte_comercial", estado, info)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("reporte_comercial_sector_consumo"))
    boton_2.clicked.connect(lambda:on_button_clicked("reporte_comercial_sector_consumo_subsidio"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado,info

def menu_reportes_tecnicos(app, window, central_widget, dimensiones, estado=None, info={}):
    estado = None
    info = {}

    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Reportes técnicos"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    mostrar_label(titulo_espacios)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Reporte indicadores técnicos":"Reportes de indicadore técnicos. Información disponibles para índice de Presión en Líneas Individuales (IPLI), índice de Odorización (IO)\ne índice de Respuesta a Servicio Técnico - Escape de Gas (IRST-EG)",
                "Reporte suspensiones":"Reporte de suspensiones realizadas",
                "Reporte de Indicador de Respuesta a Servicio Técnico (IRST-EG)":"Reporte de índice de Respuesta a Servicio Técnico - Escape de Gas (IRST-EG)"}
    boton_1 = crear_boton("Reporte indicadores técnicos (IPLI, IO, IRST-EG)", central_widget)
    boton_2 = crear_boton("Reporte suspensiones", central_widget)
    boton_3 = crear_boton("Reporte de Indicador de Respuesta a Servicio Técnico (IRST-EG)", central_widget)
    botones = [boton_1, boton_2, boton_3]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round((((screen_width)-max_width)*0.5))
    boton_1.move(x,escalar_valor(400, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_2.move(x,escalar_valor(600, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_3.move(x,escalar_valor(800, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado, info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(image_button_1)
        if texto == "volver":
            estado,info = menu_inicial(app, window, central_widget, dimensiones)
        else:
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reportes_tecnicos", estado, info, c_meses=12)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("reporte_indicadores"))
    boton_2.clicked.connect(lambda:on_button_clicked("reporte_suspensiones"))
    boton_3.clicked.connect(lambda:on_button_clicked("reporte_IRST"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado,info

def menu_KPIs(app, window, central_widget, dimensiones, estado=None, info={}):
    estado = None
    info = {}

    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Reportes KPIs"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    mostrar_label(titulo_espacios)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    mostrar_label(image_button_1)
    dic_texto = {"Porcentaje de cumplimientos regulatorios":f"Porcentaje de cumplimientos regulatorios según los reportes certificados por\nel {grupo_vanti} (certificados en plazo y fuera de plazo) en el año actual",
                "Información reclamos por cada 10.000 facturas":"Relación de reclamos realidos por cada 10.000 facturas emitidas.\nInformación reportada trimestralmente",
                "Información para matriz de requerimientos":"Información para matriz de requerimientos según los reportes por \nel {grupo_vanti} en el año actual ante el MME, SSPD, CREG y otras entidades gubernamentales",
                "Gastos AOM":"Gastos Administrativos, Operativos y Mantenimiento realizados por el {grupo_vanti}",
                "Pagos contribuciones MME":"Cuentas por cobrar (CxC) del MME para el pago de subsidios para el {grupo_vanti}"}
    boton_1 = crear_boton("Porcentaje de cumplimientos regulatorios", central_widget)
    boton_2 = crear_boton("Información reclamos por cada 10.000 facturas (trimestral)", central_widget)
    boton_3 = crear_boton("Información para matriz de requerimientos", central_widget)
    boton_4 = crear_boton("Gastos AOM", central_widget)
    boton_5 = crear_boton("Pagos contribuciones MME", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4, boton_5]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round((((screen_width)-max_width)*0.5))
    boton_1.move(x,escalar_valor(350, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_2.move(x,escalar_valor(500, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_3.move(x,escalar_valor(650, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_4.move(x,escalar_valor(800, factor_escala))
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    boton_5.move(x,escalar_valor(950, factor_escala))
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado, info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(boton_5)
        esconder_label(image_button_1)
        if texto == "volver":
            estado,info = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "reclamos_facturas":
            estado = texto
            estado,info = menu_seleccion_trimestres(app, window, central_widget, dimensiones, "menu_reportes_tecnicos", estado)
        else:
            estado = texto
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("cumplimientos_regulatorios"))
    boton_2.clicked.connect(lambda:on_button_clicked("reclamos_facturas"))
    boton_3.clicked.connect(lambda:on_button_clicked("matriz_requerimientos"))
    boton_4.clicked.connect(lambda:on_button_clicked("gastos_AOM"))
    boton_5.clicked.connect(lambda:on_button_clicked("contribuciones_MME"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado,info

def menu_CLD_PRD(app, window, central_widget, dimensiones, estado=None, info={}, estado_anterior=None):
    estado = None
    info = {}

    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Menú selección de comparación"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=50)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    mostrar_label(titulo_espacios)
    titulo = "CER - CLD - PRD"
    titulo_espacios_1 = crear_label(titulo, central_widget, font="bold", font_size=50)
    x = round((screen_width-titulo_espacios_1.sizeHint().width())*0.5)
    titulo_espacios_1.move(x, escalar_valor(180, factor_escala))
    mostrar_label(titulo_espacios_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Comparación Certificación - Calidad - Producción (GRC1-SAP)":"Comparación entre los GRC1 para la información cerificada, y descargada de los ambientes de producción (PRD) y calidad (CLD)"}
    boton_1 = crear_boton("Comparación Certificación - Calidad - Producción (GRC1-SAP)", central_widget)
    boton_2 = crear_boton("Comparación Certificación - Calidad (GRC1-SAP)", central_widget)
    boton_3 = crear_boton("Comparación Certificación - Producción (GRC1-SAP)", central_widget)
    boton_4 = crear_boton("Comparación Calidad - Producción (GRC1-SAP)", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round((((screen_width)-max_width)*0.5))
    boton_1.move(x,escalar_valor(450, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_2.move(x,escalar_valor(600, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_3.move(x,escalar_valor(750, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_4.move(x,escalar_valor(900, factor_escala))
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado, info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(titulo_espacios_1)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(image_button_1)
        if texto == "volver":
            estado,info = menu_inicial(app, window, central_widget, dimensiones)
        else:
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="menu_CLD_PRD", incluir_anual=False)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("comparacion_CER_CLD_PRD"))
    boton_2.clicked.connect(lambda:on_button_clicked("comparacion_CER_CLD"))
    boton_3.clicked.connect(lambda:on_button_clicked("comparacion_CER_PRD"))
    boton_4.clicked.connect(lambda:on_button_clicked("comparacion_CLD_PRD"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado,info

def menu_comercial_calidad_info(app, window, central_widget, dimensiones, estado=None, info={}, estado_anterior=None):
    estado = None
    info = {}

    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Menú comprobación de"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=50)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(40, factor_escala))
    mostrar_label(titulo_espacios)
    titulo = "calidad de la información (comercial)"
    titulo_espacios_1 = crear_label(titulo, central_widget, font="bold", font_size=45)
    x = round((screen_width-titulo_espacios_1.sizeHint().width())*0.5)
    titulo_espacios_1.move(x, escalar_valor(180, factor_escala))
    mostrar_label(titulo_espacios_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Comprobación de información para inventario de suscriptores":"Análisis del informe GRTT2 para comprobar la calidad de la información (generación de información a certificar)",
                "Correción de errores para inventario de suscriptores":"Cargue del archivo \'_error.csv\' para corregir los errores encontrados en en el informe GRTT2",
                "Generar información para inventario de suscriptores":"Generación de información para el inventario de suscriptores como \'NIU\',\'Codigo_DANE\',\'Direccion\',\'Cedula_Catastral\',\'Estrato\',\'Longitud\',\'Latitud\',\'Estado\'",
                "Generar información de facturación para usuarios regulados / no regulados":"Generación de información de facturación para usuarios regulados / no regulados como \'NIU\', \'Cantidad_facturas\', \'Consumo\', \'Valor_consumo_facturado\', \'Valor_total_facturado\', \'Codigo_DANE\', \'Sector_consumo\'",
                "Generar información de usuarios con número de equipo":"Generar información de usuarios con número de equipo"}
    boton_1 = crear_boton("Comprobación de info.\npara inventario de suscriptores", central_widget)
    boton_2 = crear_boton("Corrección de errores\npara inventario de suscriptores", central_widget)
    boton_3 = crear_boton("Generar info. para\ninventario de suscriptores", central_widget)
    boton_4 = crear_boton("Generar info.para\nusuarios regulados / no regulados", central_widget)
    boton_5 = crear_boton("Generar info.para\nusuarios con número de equipo", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4, boton_5]
    max_width = max([boton.sizeHint().width() for boton in botones])+20
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,escalar_valor(450, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_2.move(x,escalar_valor(700, factor_escala))
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_3.move(x,escalar_valor(450, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_4.move(x,escalar_valor(700, factor_escala))
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    x = round((screen_width-boton_5.sizeHint().width())*0.5)
    boton_5.move(x,escalar_valor(950, factor_escala))
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado, info
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(titulo_espacios_1)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(boton_5)
        esconder_label(image_button_1)
        if texto == "volver":
            estado,info = menu_inicial(app, window, central_widget, dimensiones)
        else:
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="menu_comercial_calidad_info", incluir_anual=False)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("comprobar_info_GRTT2"))
    boton_2.clicked.connect(lambda:on_button_clicked("corregir_errores_GRTT2"))
    boton_3.clicked.connect(lambda:on_button_clicked("generar_info_GRTT2"))
    boton_4.clicked.connect(lambda:on_button_clicked("generar_info_usuarios_R_NR"))
    boton_5.clicked.connect(lambda: on_button_clicked("generar_info_usuarios_con_equipo"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    event_loop.exec_()
    return estado,info

def menu_seleccion(app, window, central_widget, dimensiones, estado_anterior=None, estado=None, info={}, incluir_anual=True, c_meses=13):
    c_meses -= 1
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)

    titulo = "Selección información"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    t_filial = crear_label("Filiales", central_widget, font="bold", font_size=50)
    t_filial.move(escalar_valor(50, factor_escala), escalar_valor(150, factor_escala))
    t_filial.setParent(central_widget)
    mostrar_label(t_filial)
    t_periodo = crear_label("Periodos", central_widget, font="bold", font_size=50)
    t_periodo.move(escalar_valor(700, factor_escala), escalar_valor(150, factor_escala))
    t_periodo.setParent(central_widget)
    mostrar_label(t_periodo)
    if incluir_anual:
        boton_2 = crear_boton("", central_widget, font_size=60, padding=5)
        boton_2.setFixedSize(escalar_valor(60, factor_escala),escalar_valor(60, factor_escala))
        boton_2.move(escalar_valor(1200, factor_escala),escalar_valor(210, factor_escala))
        boton_2.setParent(central_widget)
        mostrar_label(boton_2)
        t_anual = crear_label("Anual", central_widget, font="bold", font_size=40)
        t_anual.move(escalar_valor(1300, factor_escala), escalar_valor(170, factor_escala))
        t_anual.setParent(central_widget)
        mostrar_label(t_anual)
    anual = False
    f1 = crear_boton("", central_widget, font_size=60, padding=5)
    f1.setFixedSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala))
    f1.move(escalar_valor(50, factor_escala), escalar_valor(350, factor_escala))
    f1.setParent(central_widget)
    mostrar_label(f1)
    t_f1 = crear_label("VANTI", central_widget, font="bold", font_size=40)
    t_f1.move(escalar_valor(150, factor_escala), escalar_valor(310, factor_escala))
    t_f1.setParent(central_widget)
    mostrar_label(t_f1)
    f2 = crear_boton("", central_widget, font_size=60, padding=5)
    f2.setFixedSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala))
    f2.move(escalar_valor(50, factor_escala),escalar_valor(500, factor_escala))
    f2.setParent(central_widget)
    mostrar_label(f2)
    t_f2 = crear_label("GNCB", central_widget, font="bold", font_size=40)
    t_f2.move(escalar_valor(150, factor_escala), escalar_valor(460, factor_escala))
    t_f2.setParent(central_widget)
    mostrar_label(t_f2)
    f3 = crear_boton("", central_widget, font_size=60, padding=5)
    f3.setFixedSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala))
    f3.move(escalar_valor(50, factor_escala),escalar_valor(650, factor_escala))
    f3.setParent(central_widget)
    mostrar_label(f3)
    t_f3 = crear_label("GNCR", central_widget, font="bold", font_size=40)
    t_f3.move(escalar_valor(150, factor_escala), escalar_valor(610, factor_escala))
    t_f3.setParent(central_widget)
    mostrar_label(t_f3)
    f4 = crear_boton("", central_widget, font_size=60, padding=5)
    f4.setFixedSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala))
    f4.move(escalar_valor(50, factor_escala), escalar_valor(800, factor_escala))
    f4.setParent(central_widget)
    mostrar_label(f4)
    t_f4 = crear_label("GOR", central_widget, font="bold", font_size=40)
    t_f4.move(escalar_valor(150, factor_escala), escalar_valor(760, factor_escala))
    t_f4.setParent(central_widget)
    mostrar_label(t_f4)
    f5 = crear_boton("", central_widget, font_size=60, padding=5)
    f5.setFixedSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala))
    f5.move(escalar_valor(50, factor_escala), escalar_valor(950, factor_escala))
    f5.setParent(central_widget)
    mostrar_label(f5)
    t_f5 = crear_label("Todas", central_widget, font="bold", font_size=40)
    t_f5.move(escalar_valor(150, factor_escala), escalar_valor(910, factor_escala))
    t_f5.setParent(central_widget)
    mostrar_label(t_f5)
    dic_botones_filiales = {"VANTI":[f1,t_f1,False], "GNCB":[f2,t_f2,False], "GNCR":[f3,t_f3,False], "GOR":[f4,t_f4,False], "Todas":[f5,t_f5,False]}
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3 = crear_boton("Limpiar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_3.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_3.move(escalar_valor(1700, factor_escala),escalar_valor(150, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    if len(lista_anios) >=3 :
        lista_anios_sel = lista_anios[-3:]
    else:
        lista_anios_sel = lista_anios.copy()
    lista_fechas_sel = []
    dic_fechas = {}
    x_fecha = escalar_valor(620, factor_escala)
    for anio in lista_anios_sel:
        y_fecha = escalar_valor(300, factor_escala)
        for mes in lista_meses:
            llave = anio+" / "+mes[:3]
            lista_fechas_sel.append(llave)
            dic_fechas[llave] = [(anio, mes), False, crear_boton("", central_widget, font_size=42, padding=1, radius=5), crear_label(llave, central_widget, font_size=15)]
            dic_fechas[llave][2].setFixedSize(escalar_valor(48, factor_escala),escalar_valor(48, factor_escala))
            dic_fechas[llave][2].setParent(central_widget)
            dic_fechas[llave][3].setParent(central_widget)
            dic_fechas[llave][2].move(x_fecha,y_fecha)
            dic_fechas[llave][3].move(x_fecha + escalar_valor(100, factor_escala), y_fecha - escalar_valor(10, factor_escala))
            y_fecha += escalar_valor(65, factor_escala)
            mostrar_label(dic_fechas[llave][2])
            mostrar_label(dic_fechas[llave][3])
        x_fecha += escalar_valor(450, factor_escala)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala))
    mostrar_label(image_button)

    event_loop = QEventLoop()
    def comprobar_dic(dic, pos):
        for i in dic.values():
            if i[pos]:
                return True
        return False
    def comprobar_aceptar():
        nonlocal dic_botones_filiales
        nonlocal dic_fechas
        v_dic_botones_filiales = comprobar_dic(dic_botones_filiales, 2)
        v_dic_fechas = comprobar_dic(dic_fechas, 1)
        return v_dic_botones_filiales and v_dic_fechas
    def cambiar_botones(llave):
        nonlocal dic_botones_filiales
        boton = dic_botones_filiales[llave][0]
        if llave != "Todas":
            if boton.text() == "X":
                boton.setText("")
                dic_botones_filiales[llave][2] = False
            elif boton.text() == "":
                boton.setText("X")
                dic_botones_filiales[llave][2] = True
            boton.setParent(central_widget)
            mostrar_label(boton)
        else:
            if boton.text() == "X":
                texto = ""
                valor = False
            elif boton.text() == "":
                texto = "X"
                valor = True
            for key, _ in dic_botones_filiales.items():
                boton_for = dic_botones_filiales[key][0]
                boton_for.setText(texto)
                dic_botones_filiales[key][2] = valor
                boton_for.setParent(central_widget)
                mostrar_label(boton_for)
        if dic_botones_filiales["VANTI"][0].text() == "X" and dic_botones_filiales["GNCR"][0].text() and dic_botones_filiales["GNCB"][0].text() and dic_botones_filiales["GOR"][0].text():
            dic_botones_filiales["Todas"][2] = True
            dic_botones_filiales["Todas"][0].setText("X")
            mostrar_label(dic_botones_filiales["Todas"][0])
        if dic_botones_filiales["Todas"][0].text() == "X":
            for llave in dic_botones_filiales:
                dic_botones_filiales[llave][2] = True
                dic_botones_filiales[llave][0].setText("X")
                mostrar_label(dic_botones_filiales[llave][0])
    def cambiar_botones_x(boton):
        nonlocal anual
        if boton.text() == "X":
            boton.setText("")
            anual = False
        elif boton.text() == "":
            boton.setText("X")
            anual = True
        if anual:
            llave_activa = boton_fecha_selected()
            if llave_activa:
                cambio = False
                contador = 0
                for llave, valor in dic_fechas.items():
                    valor[2].setText("")
                    valor[1] = False
                for i, (llave, valor) in enumerate(reversed(dic_fechas.items())):
                    if llave == llave_activa:
                        cambio = True
                    if cambio:
                        valor[2].setText("X")
                        valor[1] = True
                        contador += 1
                    if contador > c_meses:
                        cambio = False
    def cambiar_botones_fecha(llave):
        nonlocal dic_fechas
        boton = dic_fechas[llave][2]
        if boton.text() == "X":
            boton.setText("")
            dic_fechas[llave][1] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_fechas[llave][1] = True
        mostrar_label(boton)
        comprobar_anual(llave)
    def boton_fecha_selected():
        nonlocal dic_fechas
        for llave, valor in reversed(dic_fechas.items()):
            if valor[1]:
                return llave
        return None
    def comprobar_anual(llave_sel):
        nonlocal anual
        nonlocal dic_fechas
        if anual:
            cambio = False
            contador = 0
            for llave, valor in dic_fechas.items():
                valor[2].setText("")
                valor[1] = False
            for i, (llave, valor) in enumerate(reversed(dic_fechas.items())):
                if llave == llave_sel:
                    cambio = True
                if cambio:
                    valor[2].setText("X")
                    valor[1] = True
                    contador += 1
                if contador > c_meses:
                    cambio = False
    def limpiar_botones(boton):
        nonlocal incluir_anual
        if incluir_anual:
            nonlocal boton_2
            boton_2.setText("")
        nonlocal dic_fechas, dic_botones_filiales, anual
        anual = False
        for _, value in dic_fechas.items():
            value[2].setText("")
            value[1] = False
        for _, value in dic_botones_filiales.items():
            value[0].setText("")
            value[2] = False
    def on_button_clicked(texto):
        nonlocal estado, info, anual
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(t_filial)
            esconder_label(f1)
            esconder_label(f2)
            esconder_label(f3)
            esconder_label(f4)
            esconder_label(f5)
            esconder_label(t_f1)
            esconder_label(t_f2)
            esconder_label(t_f3)
            esconder_label(t_f4)
            esconder_label(t_f5)
            esconder_label(boton_1)
            esconder_label(t_periodo)
            esconder_label(image_button)
            if incluir_anual:
                esconder_label(t_anual)
                esconder_label(boton_2)
            esconder_label(boton_3)
            for _, value in dic_fechas.items():
                esconder_label(value[3])
                esconder_label(value[2])
            if texto == "volver":
                if estado_anterior == "menu_reporte_comercial":
                    estado,info = menu_reporte_comercial(app, window, central_widget, dimensiones)
                elif estado_anterior == "menu_reportes_comerciales":
                    estado,info = menu_reportes_comerciales(app, window, central_widget, dimensiones)
                elif estado_anterior == "menu_inicial":
                    estado,info = menu_inicial(app, window, central_widget, dimensiones)
                elif estado_anterior == "menu_edicion_archivos":
                    estado,info = menu_edicion_archivos(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif estado_anterior == "menu_CLD_PRD":
                    estado,info = menu_CLD_PRD(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif estado_anterior == "menu_comercial_calidad_info":
                    estado,info = menu_comercial_calidad_info(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif "reportes_tarifarios" in estado:
                    estado,info = menu_inicial(app, window, central_widget, dimensiones)
                elif any(texto in estado for texto in ("reporte_IRST", "reporte_suspensiones", "reporte_indicadores")):
                    estado,info = menu_reportes_tecnicos(app, window, central_widget, dimensiones)
                else:
                    estado,info = menu_reportes_comerciales(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                info["Fecha"] = dic_fechas
                info["Filial"] = dic_botones_filiales
                if estado == "archivos_estandar" or estado == "archivos_resumen" or estado == "archivos_existentes":
                    estado, info = seleccionar_reporte_categoria(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="menu_seleccion")
                elif estado == "comparacion_CER_CLD_PRD":
                    opciones = {"regenerar":True}
                    estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                elif estado == "comparacion_CER_CLD" or estado == "comparacion_CER_PRD" or estado == "comparacion_CLD_PRD":
                    opciones = {"regenerar":True, "cantidad_filas":True}
                    estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                elif estado == "comprobar_info_GRTT2" or estado == "corregir_errores_GRTT2" or estado == "generar_info_usuarios_R_NR":
                    opciones = {"regenerar":True}
                    estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                elif estado == "generar_info_GRTT2":
                    opciones = {"regenerar":True, "usuarios_activos":True}
                    estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                elif estado == "generar_info_usuarios_con_equipo":
                    opciones = {"regenerar":True}
                    estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                else:
                    if anual and "anual" not in estado:
                        estado += "_anual"
                        estado = estado.replace("_mensual", "")
                    elif "mensual" not in estado and "anual" not in estado:
                        estado += "_mensual"
                        estado = estado.replace("_anual", "")
                    if "reporte_comercial_sector_consumo" in estado:
                        opciones = {"regenerar":True, "codigo_DANE":True, "valor_facturado":True, "facturas":True}
                        if dic_botones_filiales["Todas"][0].text() == "X":
                            opciones["sumatoria"] = True
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "reporte_comercial_sector_consumo_subsidio" in estado:
                        opciones = {"regenerar":True, "codigo_DANE":True, "valor_facturado":True, "facturas":True}
                        if dic_botones_filiales["Todas"][0].text() == "X":
                            opciones["sumatoria"] = True
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "reporte_compensaciones" in estado:
                        opciones = {"regenerar":True, "inventario":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "desviaciones_significativas" in estado:
                        opciones = {"regenerar":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "reporte_DANE" in estado:
                        opciones = {"regenerar":True, "codigo_DANE":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "reportes_tarifarios" in estado:
                        opciones = {"regenerar":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "reporte_indicadores" in estado:
                        opciones = {"regenerar":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "reporte_suspensiones" in estado:
                        opciones = {"regenerar":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    elif "reporte_IRST" in estado:
                        opciones = {"regenerar":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
                    else:
                        opciones = {"regenerar":True, "codigo_DANE":True, "sumatoria":True, "valor_facturado":True, "facturas":True}
                        estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado_anterior="menu_seleccion", estado=estado, info=info, opciones=opciones)
    f1.clicked.connect(lambda: cambiar_botones("VANTI"))
    f2.clicked.connect(lambda: cambiar_botones("GNCB"))
    f3.clicked.connect(lambda: cambiar_botones("GNCR"))
    f4.clicked.connect(lambda: cambiar_botones("GOR"))
    f5.clicked.connect(lambda: cambiar_botones("Todas"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    if incluir_anual:
        boton_2.clicked.connect(lambda:cambiar_botones_x(boton_2))
    boton_3.clicked.connect(lambda:limpiar_botones(boton_3))
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    for llave, value in dic_fechas.items():
        value[2].clicked.connect(lambda _, l=llave: cambiar_botones_fecha(l))
    event_loop.exec_()
    return estado,info

def unir_listas_anio_tri(lista_anios, lista_tri):
    lista_anio_tri = []
    for j in lista_anios:
        for i in lista_tri:
            lista_anio_tri.append(f"{j} - {i}")
    return lista_anio_tri

def menu_seleccion_trimestres(app, window, central_widget, dimensiones, estado_anterior=None, estado=None, info={}):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)

    titulo = "Selección información trimestral"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=55)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    t_periodo = crear_label("Periodos", central_widget, font="bold", font_size=45)
    x = round((screen_width-t_periodo.sizeHint().width())*0.5)
    t_periodo.move(x, escalar_valor(150, factor_escala))
    t_periodo.setParent(central_widget)
    mostrar_label(t_periodo)
    anual = True
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3 = crear_boton("Limpiar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_3.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_3.move(escalar_valor(1700, factor_escala), escalar_valor(150, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    if len(lista_anios) >=3 :
        lista_anios_sel = lista_anios[-3:]
    else:
        lista_anios_sel = lista_anios.copy()
    lista_fechas_sel = []
    dic_fechas = {}
    x_fecha = escalar_valor(80, factor_escala)
    lista_trimestre_anios = unir_listas_anio_tri(lista_anios_sel, lista_trimestres)
    for anio in lista_anios_sel:
        y_fecha = escalar_valor(350, factor_escala)
        for trim in lista_trimestres:
            llave = anio+" / "+trim
            lista_fechas_sel.append(llave)
            dic_fechas[llave] = [(anio, trim), False, crear_boton("", central_widget, font_size=70, padding=1, radius=5), crear_label(llave, central_widget, font_size=30)]
            dic_fechas[llave][2].setFixedSize(escalar_valor(110, factor_escala), escalar_valor(110, factor_escala))
            dic_fechas[llave][2].setParent(central_widget)
            dic_fechas[llave][3].setParent(central_widget)
            dic_fechas[llave][2].move(x_fecha,y_fecha)
            dic_fechas[llave][3].move(x_fecha + escalar_valor(95, factor_escala), y_fecha - escalar_valor(10, factor_escala))
            y_fecha += escalar_valor(180, factor_escala)
            mostrar_label(dic_fechas[llave][2])
            mostrar_label(dic_fechas[llave][3])
        x_fecha += escalar_valor(620, factor_escala)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala))
    mostrar_label(image_button)

    event_loop = QEventLoop()
    def comprobar_dic(dic, pos):
        for i in dic.values():
            if i[pos]:
                return True
        return False
    def comprobar_aceptar():
        nonlocal dic_fechas
        v_dic_fechas = comprobar_dic(dic_fechas, 1)
        return v_dic_fechas
    def cambiar_botones_fecha(llave):
        nonlocal dic_fechas
        boton = dic_fechas[llave][2]
        if boton.text() == "X":
            boton.setText("")
            dic_fechas[llave][1] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_fechas[llave][1] = True
        mostrar_label(boton)
        comprobar_anual(llave)
    def comprobar_anual(llave_sel):
        nonlocal anual
        nonlocal dic_fechas
        if anual:
            cambio = False
            contador = 0
            for llave, valor in dic_fechas.items():
                valor[2].setText("")
                valor[1] = False
            for i, (llave, valor) in enumerate(reversed(dic_fechas.items())):
                if llave == llave_sel:
                    cambio = True
                if cambio:
                    valor[2].setText("X")
                    valor[1] = True
                    contador += 1
                if contador > 3:
                    cambio = False
    def limpiar_botones(boton):
        for llave, value in dic_fechas.items():
            value[2].setText("")
            value[1] = False
    def on_button_clicked(texto):
        nonlocal estado, info, anual
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(boton_1)
            esconder_label(t_periodo)
            esconder_label(boton_3)
            esconder_label(image_button)
            for llave, value in dic_fechas.items():
                esconder_label(value[3])
                esconder_label(value[2])
            if texto == "volver":
                estado,info = menu_KPIs(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                info["Fecha"] = dic_fechas
                info["Trimestres"] = lista_trimestre_anios
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    boton_3.clicked.connect(lambda:limpiar_botones(boton_3))
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    for llave, value in dic_fechas.items():
        value[2].clicked.connect(lambda _, l=llave: cambiar_botones_fecha(l))
    event_loop.exec_()
    return estado,info

def menu_dashboard(app, window, central_widget, dimensiones, estado_anterior=None, estado=None, info={}):
    mes_actual = int(fecha_actual.month)-1
    anio_actual = int(fecha_actual.year)
    if mes_actual == 0:
        mes_actual = 12
        anio_actual = anio_actual-1
    mes_actual = dic_meses[str(mes_actual)]
    anio_actual = str(anio_actual)
    fecha_DB_actual = f"{anio_actual} / {mes_actual}"
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Selección información Dashboard"
    if estado == "reportes_existentes":
        titulo = "Selección información anual"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=55)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    anual = True
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1110, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3 = crear_boton("Limpiar", central_widget, font_size=25)
    boton_3.move(escalar_valor(1700, factor_escala),escalar_valor(280, factor_escala))
    boton_3.setParent(central_widget)
    boton_4 = crear_boton("Actual", central_widget, font_size=25)
    boton_4.move(escalar_valor(1700, factor_escala),escalar_valor(180, factor_escala))
    boton_4.setParent(central_widget)
    botones = [boton_3, boton_4]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width+15)
    mostrar_label(boton_3)
    mostrar_label(boton_4)

    if len(lista_anios) >= 4:
        lista_anios_sel = lista_anios[-4:]
    else:
        lista_anios_sel = lista_anios.copy()
    lista_fechas_sel = []
    dic_fechas = {}
    x_fecha = escalar_valor(65, factor_escala)
    for anio in lista_anios_sel:
        y_fecha = escalar_valor(300, factor_escala)
        for mes in lista_meses:
            llave = anio+" / "+mes
            lista_fechas_sel.append(llave)
            dic_fechas[llave] = [(anio, mes), False, crear_boton("", central_widget, font_size=42, padding=1, radius=5), crear_label(llave, central_widget, font_size=15)]
            dic_fechas[llave][2].setFixedSize(escalar_valor(48, factor_escala),escalar_valor(48, factor_escala))
            dic_fechas[llave][2].setParent(central_widget)
            dic_fechas[llave][3].setParent(central_widget)
            dic_fechas[llave][2].move(x_fecha,y_fecha)
            dic_fechas[llave][3].move(x_fecha + escalar_valor(85, factor_escala), y_fecha - escalar_valor(10, factor_escala))
            y_fecha += escalar_valor(65, factor_escala)
            mostrar_label(dic_fechas[llave][2])
            mostrar_label(dic_fechas[llave][3])
        x_fecha += escalar_valor(425, factor_escala)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala))
    mostrar_label(image_button)

    event_loop = QEventLoop()
    def comprobar_dic(dic, pos):
        for i in dic.values():
            if i[pos]:
                return True
        return False
    def comprobar_aceptar():
        nonlocal dic_fechas
        v_dic_fechas = comprobar_dic(dic_fechas, 1)
        return v_dic_fechas
    def cambiar_botones_fecha(llave):
        nonlocal dic_fechas
        boton = dic_fechas[llave][2]
        if boton.text() == "X":
            boton.setText("")
            dic_fechas[llave][1] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_fechas[llave][1] = True
        mostrar_label(boton)
        comprobar_anual(llave)
    def comprobar_anual(llave_sel):
        nonlocal anual
        nonlocal dic_fechas
        if anual:
            cambio = False
            contador = 0
            for llave, valor in dic_fechas.items():
                valor[2].setText("")
                valor[1] = False
            for i, (llave, valor) in enumerate(reversed(dic_fechas.items())):
                if llave == llave_sel:
                    cambio = True
                if cambio:
                    valor[2].setText("X")
                    valor[1] = True
                    contador += 1
                if contador > 12:
                    cambio = False
    def limpiar_botones():
        for _, value in dic_fechas.items():
            value[2].setText("")
            value[1] = False
    def elegir_actual():
        limpiar_botones()
        cambio = False
        contador = 0
        for i, (llave, valor) in enumerate(reversed(dic_fechas.items())):
            if llave == fecha_DB_actual:
                cambio = True
            if cambio:
                valor[2].setText("X")
                valor[1] = True
                contador += 1
            if contador > 12:
                cambio = False
    def on_button_clicked(texto):
        nonlocal estado, info, anual, estado_anterior
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(boton_1)
            esconder_label(boton_3)
            esconder_label(boton_4)
            esconder_label(image_button)
            for _, value in dic_fechas.items():
                esconder_label(value[3])
                esconder_label(value[2])
            if texto == "volver":
                if estado_anterior == "menu_edicion_archivos":
                    estado, info = menu_edicion_archivos(app, window, central_widget, dimensiones, estado, info)
                else:
                    estado,info = menu_inicial(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                fecha_personalizada = fechas_anuales(dic_fechas)
                if estado == "reportes_existentes":
                    info["Reporte_anual"] = {'fecha_personalizada': [(fecha_personalizada[0][0], fecha_personalizada[0][1]), (fecha_personalizada[1][0], fecha_personalizada[1][1])]}
                    estado, info = seleccionar_reporte_categoria(app, window, central_widget, dimensiones, estado, info, estado_anterior="menu_dashboard")
                elif estado == "dashboard":
                    info["Reporte"] = {'ubicacion': ['Reportes Nuevo SUI'], 
                                    'anios': None,
                                    'filial': ['VANTI', 'GNCB', 'GNCR', 'GOR'], 
                                    'meses': None,
                                    'tipo': ['Comercial', 'Tarifario', 'Tecnico'], 
                                    'clasificacion': None, 
                                    'fecha_personalizada': [(fecha_personalizada[0][0], fecha_personalizada[0][1]), (fecha_personalizada[1][0], fecha_personalizada[1][1])]}
                    estado, info = opciones_adicionales_dashboard(app, window, central_widget, dimensiones, estado, info, fecha_personalizada)
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    boton_3.clicked.connect(limpiar_botones)
    boton_4.clicked.connect(elegir_actual)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    for llave, value in dic_fechas.items():
        value[2].clicked.connect(lambda _, l=llave: cambiar_botones_fecha(l))
    event_loop.exec_()
    return estado,info

def fechas_anuales(dic):
    c = 0
    lista_fechas = []
    for _, valor in dic.items():
        if valor[1]:
            if c == 0:
                lista_fechas.append([valor[0][0],valor[0][1]])
                c += 1
            else:
                lista_fechas.append([valor[0][0],valor[0][1]])
                c = 0
    lista_fecha_anual = [(lista_fechas[0][0],lista_fechas[0][1]),(lista_fechas[-1][0],lista_fechas[-1][1])]
    return lista_fecha_anual

def opciones_adicionales_dashboard(app, window, central_widget, dimensiones, estado=None, info={}, fecha_personalizada=None):
    opciones = {"regenerar_mensual":True, "regenerar_anual":True}
    dic_adicionales_texto = {"regenerar_mensual":"Regenerar reportes para el último mes seleccionado",
                            "regenerar_anual":"Regenerar reportes para todos los meses seleccionados"}
    dic_explicacion = {"regenerar_mensual":"Regenerar todos los reportes necesarios para el Dashboard para el último mes seleccionadob (tiempo estimado: 11 minutos)",
                        "regenerar_anual":"Regenerar todos los reportes necesarios para el Dashboard para todos los meses seleccionados (tiempo estimado: 132 minutos)"}
    if not len(opciones):
        return estado, info
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Opciones adicionales"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=45)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    titulo_espacios_1 = crear_label(f"Dashboard ({fecha_personalizada[0][1][:3]}/{fecha_personalizada[0][0]} - {fecha_personalizada[1][1][:3]}/{fecha_personalizada[1][0]})", central_widget, font="bold", font_size=45)
    x = round((screen_width-titulo_espacios_1.sizeHint().width())*0.5)
    titulo_espacios_1.move(x, escalar_valor(150, factor_escala))
    titulo_espacios_1.setParent(central_widget)
    mostrar_label(titulo_espacios_1)

    label_codigo_DANE = crear_label("", central_widget, font="bold", font_size=12)
    label_codigo_DANE.move(escalar_valor(50, factor_escala), escalar_valor(980, factor_escala))
    label_codigo_DANE.setParent(central_widget)
    esconder_label(label_codigo_DANE)
    label_check = QPushButton("", central_widget)
    pixmap_check = QPixmap(ruta_imagenes+"check.png")
    pixmap_check = pixmap_check.scaled(escalar_valor(320, factor_escala), escalar_valor(80, factor_escala), aspectRatioMode=1)
    icon_check = QIcon(pixmap_check)
    label_check.setIcon(icon_check)
    label_check.setIconSize(pixmap_check.size())
    label_check.move(escalar_valor(1660, factor_escala), escalar_valor(980, factor_escala))
    esconder_label(label_check)
    lista_x_pos = [escalar_valor(200, factor_escala), escalar_valor(780, factor_escala), escalar_valor(1400, factor_escala)]
    c_x = 0
    c_y = escalar_valor(500, factor_escala)
    c_c = 0
    cambio = escalar_valor(300, factor_escala)
    dic_opciones_botones = {}
    dic_texto = {}
    for llave, valor in opciones.items():
        dic_texto[dic_adicionales_texto[llave]] = dic_explicacion[llave]
        if llave not in dic_opciones_botones:
            dic_opciones_botones[llave] = None
        boton_for = crear_boton("", central_widget, font_size=60, padding=10, radius=10)
        label_for = crear_label(dic_adicionales_texto[llave], central_widget, font_size=30)
        boton_for.setFixedSize(escalar_valor(110, factor_escala), escalar_valor(110, factor_escala))
        boton_for.setParent(central_widget)
        label_for.setParent(central_widget)
        boton_for.move(lista_x_pos[c_x], c_y)
        label_for.move(lista_x_pos[c_x] + escalar_valor(150, factor_escala), c_y)
        dic_opciones_botones[llave] = [False, boton_for, label_for]
        mostrar_label(label_for)
        mostrar_label(boton_for)
        c_c += 1
        c_y += cambio
        if c_c > 5:
            c_x += 1
            c_c = 0
            c_y = escalar_valor(350, factor_escala)
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala)))
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    image_button_2 = QPushButton("", central_widget)
    pixmap_2 = QPixmap(ruta_imagenes+"lupa.png")
    icon_2 = QIcon(pixmap_2)
    image_button_2.setIcon(icon_2)
    image_button_2.setIconSize(QSize(escalar_valor(45, factor_escala), escalar_valor(45, factor_escala)))
    image_button_2.setFixedSize(escalar_valor(45, factor_escala), escalar_valor(45, factor_escala))
    image_button_2.move(escalar_valor(740, factor_escala), escalar_valor(1000, factor_escala))
    mostrar_label(image_button_1)

    event_loop = QEventLoop()
    def cambiar_botones_reporte(llave):
        nonlocal dic_opciones_botones
        boton = dic_opciones_botones[llave][1]
        if boton.text() == "X":
            boton.setText("")
            dic_opciones_botones[llave][0] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_opciones_botones[llave][0] = True
        if llave == "regenerar_mensual":
            if dic_opciones_botones[llave][1].text() == "X":
                dic_opciones_botones[llave][0] = True
                dic_opciones_botones["regenerar_anual"][0] = False
                dic_opciones_botones["regenerar_anual"][1].setText("")
        elif llave == "regenerar_anual":
            if dic_opciones_botones[llave][1].text() == "X":
                dic_opciones_botones[llave][0] = True
                dic_opciones_botones["regenerar_mensual"][0] = False
                dic_opciones_botones["regenerar_mensual"][1].setText("")
        mostrar_label(dic_opciones_botones["regenerar_anual"][1])
        mostrar_label(dic_opciones_botones["regenerar_mensual"][1])
    def on_button_clicked(texto):
        nonlocal estado, info
        if texto == "aceptar" or texto == "volver":
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(titulo_espacios_1)
            esconder_label(label_check)
            esconder_label(image_button)
            esconder_label(boton_1)
            esconder_label(label_codigo_DANE)
            esconder_label(image_button_1)
            esconder_label(image_button_2)
            for _, valor in dic_opciones_botones.items():
                esconder_label(valor[1])
                esconder_label(valor[2])
            if texto == "volver":
                estado, info = menu_dashboard(app, window, central_widget, dimensiones, estado=estado, info=info)
            elif texto == "aceptar":
                info["Opciones_adicionales"] = dic_opciones_botones
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    for llave, valor in dic_opciones_botones.items():
        valor[1].clicked.connect(lambda _, l=llave: cambiar_botones_reporte(l))
    event_loop.exec_()
    return estado, info

def seleccionar_reporte(app, window, central_widget, dimensiones, estado=None, info={}, estado_anterior=""):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    elegir_1 = False
    if estado_anterior == "menu_inicial":
        elegir_1 = True

    titulo = "Selección de reportes"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    t_comercial = crear_label("Reportes comerciales", central_widget, font="bold", font_size=32)
    t_comercial.move(escalar_valor(50, factor_escala), escalar_valor(150, factor_escala))
    t_comercial.setParent(central_widget)
    mostrar_label(t_comercial)
    t_tarifario = crear_label("Reportes tarifarios", central_widget, font="bold", font_size=32)
    t_tarifario.move(escalar_valor(780, factor_escala), escalar_valor(150, factor_escala))
    t_tarifario.setParent(central_widget)
    mostrar_label(t_tarifario)
    t_tecnico = crear_label("Reportes técnicos", central_widget, font="bold", font_size=32)
    t_tecnico.move(escalar_valor(1400, factor_escala), escalar_valor(150, factor_escala))
    t_tecnico.setParent(central_widget)
    mostrar_label(t_tecnico)
    dic_reportes = {}
    lista_x_reportes = [escalar_valor(50, factor_escala), escalar_valor(780, factor_escala), escalar_valor(1400, factor_escala)]
    for i, (llave, valor) in enumerate(reportes_disponibles.items()):
        y_reporte = escalar_valor(300, factor_escala)
        for elemento in valor:
            if elemento != "GRTT2SAP":
                if llave not in dic_reportes:
                    dic_reportes[llave] = {}
                if elemento not in dic_reportes[llave]:
                    dic_reportes[llave][elemento] = None
                boton_for = crear_boton("", central_widget, font_size=42, padding=10, radius=10)
                label_for = crear_label(elemento, central_widget, font_size=20)
                boton_for.setFixedSize(escalar_valor(56, factor_escala),escalar_valor(56, factor_escala))
                boton_for.setParent(central_widget)
                label_for.setParent(central_widget)
                boton_for.move(lista_x_reportes[i] + escalar_valor(80, factor_escala),y_reporte)
                label_for.move(lista_x_reportes[i] + escalar_valor(180, factor_escala), y_reporte - escalar_valor(15, factor_escala))
                dic_reportes[llave][elemento] = [False, boton_for, label_for]
                mostrar_label(label_for)
                mostrar_label(boton_for)
                y_reporte += escalar_valor(80, factor_escala)
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Reportes comerciales":[("GRC1","Información comercial de usuarios regulados"),("GRC2","Información comercial de suministro, transporte, distribución y comercialización"),("GRC3","Información de compensación sector residencial y\nno residencial usuarios regulados"),("GRTT2","Inventario de suscriptores"),("DS56","Usuarios con consumos estacionales"),("DS57","Investigaciones por Desviaciones Significativas"),("DS58"," Resultados Investigaciones por Desviaciones Significativas")],
                "Reportes tarifarios":[("GRT1","Estructura tarifaria de gas combustible por redes"),("GRT3","Opción tarifaria")],
                "Reportes técnicos":[("GRS1","Información de suspensiones"),("GRCS1","Información de Respuesta a Servicio Técnico"),("GRCS2","Consolidación de indicadores"),("GRCS3","Información de Presión en Líneas Individuales y Nivel de Odorización"),("GRCS7","Revisiones previas y Revisiones Periódicas Obligatorias - RPO"),("GRCS9","Revisiones Periódicas Obligatorias y revisiones previas\n - cuentas no normalizadas")]}

    event_loop = QEventLoop()
    def cambiar_botones_reporte(llave, valor):
        nonlocal dic_reportes
        if elegir_1:
            for llave_bus, dic_llave in dic_reportes.items():
                for reporte, lista_reporte in dic_llave.items():
                    boton_for = dic_reportes[llave_bus][reporte][1]
                    boton_for.setText("")
                    mostrar_label(boton_for)
        boton = dic_reportes[llave][valor][1]
        if boton.text() == "X":
            boton.setText("")
            dic_reportes[llave][valor][0] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_reportes[llave][valor][0] = True
        mostrar_label(boton)

    def comprobar_dic(dic, pos):
        for llave, dic_llave in dic.items():
            for reporte, lista_reporte in dic_llave.items():
                if lista_reporte[pos]:
                    return True
        return False
    def comprobar_aceptar():
        return comprobar_dic(dic_reportes, 0)
    def on_button_clicked(texto):
        nonlocal estado, info
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(t_comercial)
            esconder_label(t_tarifario)
            esconder_label(t_tecnico)
            esconder_label(image_button)
            esconder_label(boton_1)
            esconder_label(image_button_1)
            for llave, dic_llave in dic_reportes.items():
                for reporte, lista_reporte in dic_llave.items():
                    esconder_label(lista_reporte[1])
                    esconder_label(lista_reporte[2])
            if texto == "volver":
                if estado_anterior == "menu_inicial":
                    estado, info = menu_config_inicial(app, window, central_widget, dimensiones)
                else:
                    estado, info = menu_seleccion(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                if estado_anterior == "menu_inicial":
                    info["Reporte"] = dic_reportes
                elif estado == "archivos_estandar" or estado == "archivos_resumen":
                    info["Reporte"] = dic_reportes
                else:
                    estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado, info)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    for llave, dic_llave in dic_reportes.items():
        for reporte, lista_reporte in dic_llave.items():
            lista_reporte[1].clicked.connect(lambda _, l=llave, v=reporte: cambiar_botones_reporte(l, v))
    event_loop.exec_()
    return estado,info

def seleccionar_reporte_categoria(app, window, central_widget, dimensiones, estado=None, info={}, estado_anterior=""):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Selección de reportes"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    boton_com = crear_boton("", central_widget, font_size=42, padding=2, radius=10)
    boton_com.setFixedSize(escalar_valor(56, factor_escala), escalar_valor(56, factor_escala))
    boton_com.setParent(central_widget)
    boton_com.move(escalar_valor(15, factor_escala),escalar_valor(275, factor_escala))
    mostrar_label(boton_com)
    t_comercial = crear_label("Reportes comerciales", central_widget, font="bold", font_size=28)
    t_comercial.move(escalar_valor(55, factor_escala), escalar_valor(250, factor_escala))
    t_comercial.setParent(central_widget)
    mostrar_label(t_comercial)
    boton_tar = crear_boton("", central_widget, font_size=42, padding=2, radius=10)
    boton_tar.setFixedSize(escalar_valor(56, factor_escala), escalar_valor(56, factor_escala))
    boton_tar.setParent(central_widget)
    boton_tar.move(escalar_valor(745, factor_escala),escalar_valor(275, factor_escala))
    mostrar_label(boton_tar)
    t_tarifario = crear_label("Reportes tarifarios", central_widget, font="bold", font_size=28)
    t_tarifario.move(escalar_valor(785, factor_escala), escalar_valor(250, factor_escala))
    t_tarifario.setParent(central_widget)
    mostrar_label(t_tarifario)
    boton_tec = crear_boton("", central_widget, font_size=42, padding=2, radius=10)
    boton_tec.setFixedSize(escalar_valor(56, factor_escala),escalar_valor(56, factor_escala))
    boton_tec.setParent(central_widget)
    boton_tec.move(escalar_valor(1365, factor_escala),escalar_valor(275, factor_escala))
    mostrar_label(boton_tec)
    t_tecnico = crear_label("Reportes técnicos", central_widget, font="bold", font_size=28)
    t_tecnico.move(escalar_valor(1405, factor_escala), escalar_valor(250, factor_escala))
    t_tecnico.setParent(central_widget)
    mostrar_label(t_tecnico)
    dic_categorias = {"Comercial":[False, boton_com, t_comercial],
                    "Tarifario":[False, boton_tar, t_tarifario],
                    "Tecnico":[False, boton_tec, t_tecnico]}
    dic_reportes = {}
    lista_x_reportes = [escalar_valor(50, factor_escala), escalar_valor(780, factor_escala), escalar_valor(1400, factor_escala)]
    for i, (llave, valor) in enumerate(reportes_disponibles.items()):
        y_reporte = escalar_valor(400, factor_escala)
        for elemento in valor:
            if elemento != "GRTT2SAP":
                if llave not in dic_reportes:
                    dic_reportes[llave] = {}
                if elemento not in dic_reportes[llave]:
                    dic_reportes[llave][elemento] = None
                boton_for = crear_boton("", central_widget, font_size=42, padding=2, radius=10)
                label_for = crear_label(elemento, central_widget, font_size=20)
                boton_for.setFixedSize(escalar_valor(56, factor_escala),escalar_valor(56, factor_escala))
                boton_for.setParent(central_widget)
                label_for.setParent(central_widget)
                boton_for.move(lista_x_reportes[i] + escalar_valor(80, factor_escala),y_reporte)
                label_for.move(lista_x_reportes[i] + escalar_valor(180, factor_escala), y_reporte - escalar_valor(15, factor_escala))
                dic_reportes[llave][elemento] = [False, boton_for, label_for]
                mostrar_label(label_for)
                mostrar_label(boton_for)
                y_reporte += escalar_valor(80, factor_escala)
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala)))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Reportes comerciales":[("GRC1","Información comercial de usuarios regulados"),("GRC2","Información comercial de suministro, transporte, distribución y comercialización"),("GRC3","Información de compensación sector residencial y\nno residencial usuarios regulados"),("GRTT2","Inventario de suscriptores"),("DS56","Usuarios con consumos estacionales"),("DS57","Investigaciones por Desviaciones Significativas"),("DS58"," Resultados Investigaciones por Desviaciones Significativas")],
                "Reportes tarifarios":[("GRT1","Estructura tarifaria de gas combustible por redes"),("GRT3","Opción tarifaria")],
                "Reportes técnicos":[("GRS1","Información de suspensiones"),("GRCS1","Información de Respuesta a Servicio Técnico"),("GRCS2","Consolidación de indicadores"),("GRCS3","Información de Presión en Líneas Individuales y Nivel de Odorización"),("GRCS7","Revisiones previas y Revisiones Periódicas Obligatorias - RPO"),("GRCS9","Revisiones Periódicas Obligatorias y revisiones previas\n - cuentas no normalizadas")]}

    event_loop = QEventLoop()
    def cambiar_botones_reporte(llave, valor):
        nonlocal dic_reportes
        boton = dic_reportes[llave][valor][1]
        if boton.text() == "X" and not dic_categorias[llave][0]:
            boton.setText("")
            dic_reportes[llave][valor][0] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_reportes[llave][valor][0] = True
        mostrar_label(boton)
    def comprobar_dic(dic, pos):
        for _, dic_llave in dic.items():
            for _, lista_reporte in dic_llave.items():
                if lista_reporte[pos]:
                    return True
        return False
    def comprobar_aceptar():
        return comprobar_dic(dic_reportes, 0)
    def cambiar_botones_categoria(llave):
        nonlocal dic_categorias, dic_reportes
        boton = dic_categorias[llave][1]
        if boton.text() == "X":
            boton.setText("")
            dic_categorias[llave][0] = False
            mostrar_label(dic_categorias[llave][1])
        elif boton.text() == "":
            boton.setText("X")
            dic_categorias[llave][0] = True
            mostrar_label(dic_categorias[llave][1])
            for _, lista_reporte in dic_reportes[llave].items():
                lista_reporte[1].setText("X")
                lista_reporte[0] = True
                mostrar_label(lista_reporte[1])
    def on_button_clicked(texto):
        nonlocal estado, info
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(t_comercial)
            esconder_label(t_tarifario)
            esconder_label(t_tecnico)
            esconder_label(boton_com)
            esconder_label(boton_tar)
            esconder_label(boton_tec)
            esconder_label(image_button)
            esconder_label(boton_1)
            esconder_label(image_button_1)
            for _, dic_llave in dic_reportes.items():
                for _, lista_reporte in dic_llave.items():
                    esconder_label(lista_reporte[1])
                    esconder_label(lista_reporte[2])
            if texto == "volver":
                if estado_anterior == "menu_inicial":
                    estado, info = menu_config_inicial(app, window, central_widget, dimensiones)
                elif estado_anterior == "menu_seleccion":
                    estado, info = menu_seleccion(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif estado_anterior == "menu_dashboard":
                    estado, info = menu_dashboard(app, window, central_widget, dimensiones, estado=estado, info=info)
                else:
                    estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado=estado, info=info)
            elif texto == "aceptar":
                if estado_anterior == "menu_inicial":
                    info["Reporte"] = dic_reportes
                elif estado == "convertir_archivos":
                    info["Reporte"] = dic_reportes
                    info["Categoria"] = dic_categorias
                    estado, info = seleccionar_periodo(app, window, central_widget, dimensiones, estado, info, estado_anterior="seleccionar_reporte_categoria", c_meses=12)
                elif estado == "archivos_estandar" or estado == "archivos_resumen" or estado == "archivos_existentes" or estado == "reportes_existentes":
                    info["Reporte"] = dic_reportes
                    info["Categoria"] = dic_categorias
                else:
                    estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado, info)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    for llave, dic_llave in dic_reportes.items():
        for reporte, lista_reporte in dic_llave.items():
            lista_reporte[1].clicked.connect(lambda _, l=llave, v=reporte: cambiar_botones_reporte(l, v))
    for llave, lista in dic_categorias.items():
        lista[1].clicked.connect(lambda _, l=llave: cambiar_botones_categoria(l))
    event_loop.exec_()
    return estado,info

def seleccionar_periodo(app, window, central_widget, dimensiones, estado=None, info={}, estado_anterior="", incluir_anual=True, c_meses=12):
    c_meses -= 1
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    titulo = "Selección de periodo"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    if incluir_anual:
        boton_2 = crear_boton("", central_widget, font_size=60, padding=5)
        boton_2.setFixedSize(escalar_valor(60, factor_escala), escalar_valor(60, factor_escala))
        boton_2.move(escalar_valor(1200, factor_escala),escalar_valor(210, factor_escala))
        boton_2.setParent(central_widget)
        mostrar_label(boton_2)
        t_anual = crear_label("Anual", central_widget, font="bold", font_size=40)
        t_anual.move(escalar_valor(1300, factor_escala), escalar_valor(170, factor_escala))
        t_anual.setParent(central_widget)
        mostrar_label(t_anual)
    anual = False
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3 = crear_boton("Limpiar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_3.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_3.move(escalar_valor(1700, factor_escala),escalar_valor(150, factor_escala))
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    if len(lista_anios) >=3 :
        lista_anios_sel = lista_anios[-3:]
    else:
        lista_anios_sel = lista_anios.copy()
    lista_fechas_sel = []
    dic_fechas = {}
    x_fecha = escalar_valor(65, factor_escala)
    for anio in lista_anios_sel:
        y_fecha = escalar_valor(300, factor_escala)
        for mes in lista_meses:
            llave = anio+" / "+mes
            lista_fechas_sel.append(llave)
            dic_fechas[llave] = [(anio, mes), False, crear_boton("", central_widget, font_size=42, padding=1, radius=5), crear_label(llave, central_widget, font_size=15)]
            dic_fechas[llave][2].setFixedSize(escalar_valor(48, factor_escala),escalar_valor(48, factor_escala))
            dic_fechas[llave][2].setParent(central_widget)
            dic_fechas[llave][3].setParent(central_widget)
            dic_fechas[llave][2].move(x_fecha,y_fecha)
            dic_fechas[llave][3].move(x_fecha + escalar_valor(85, factor_escala), y_fecha - escalar_valor(10, factor_escala))
            y_fecha += escalar_valor(65, factor_escala)
            mostrar_label(dic_fechas[llave][2])
            mostrar_label(dic_fechas[llave][3])
        x_fecha += escalar_valor(425, factor_escala)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala))
    mostrar_label(image_button)

    event_loop = QEventLoop()
    def comprobar_dic(dic, pos):
        for i in dic.values():
            if i[pos]:
                return True
        return False
    def comprobar_aceptar():
        nonlocal dic_fechas
        v_dic_fechas = comprobar_dic(dic_fechas, 1)
        return v_dic_fechas
    def cambiar_botones_x(boton):
        nonlocal anual
        if boton.text() == "X":
            boton.setText("")
            anual = False
        elif boton.text() == "":
            boton.setText("X")
            anual = True
        if anual:
            llave_activa = boton_fecha_selected()
            if llave_activa:
                cambio = False
                contador = 0
                for llave, valor in dic_fechas.items():
                    valor[2].setText("")
                    valor[1] = False
                for i, (llave, valor) in enumerate(reversed(dic_fechas.items())):
                    if llave == llave_activa:
                        cambio = True
                    if cambio:
                        valor[2].setText("X")
                        valor[1] = True
                        contador += 1
                    if contador > c_meses:
                        cambio = False
    def cambiar_botones_fecha(llave):
        nonlocal dic_fechas
        boton = dic_fechas[llave][2]
        if boton.text() == "X":
            boton.setText("")
            dic_fechas[llave][1] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_fechas[llave][1] = True
        mostrar_label(boton)
        comprobar_anual(llave)
    def boton_fecha_selected():
        nonlocal dic_fechas
        for llave, valor in reversed(dic_fechas.items()):
            if valor[1]:
                return llave
        return None
    def comprobar_anual(llave_sel):
        nonlocal anual
        nonlocal dic_fechas
        if anual:
            cambio = False
            contador = 0
            for llave, valor in dic_fechas.items():
                valor[2].setText("")
                valor[1] = False
            for i, (llave, valor) in enumerate(reversed(dic_fechas.items())):
                if llave == llave_sel:
                    cambio = True
                if cambio:
                    valor[2].setText("X")
                    valor[1] = True
                    contador += 1
                if contador > c_meses:
                    cambio = False
    def limpiar_botones(boton):
        if incluir_anual:
            nonlocal boton_2
            boton_2.setText("")
        nonlocal dic_fechas, anual
        anual = False
        for llave, value in dic_fechas.items():
            value[2].setText("")
            value[1] = False
    def on_button_clicked(texto):
        nonlocal estado, info, anual
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(boton_1)
            if incluir_anual:
                esconder_label(t_anual)
                esconder_label(boton_2)
            esconder_label(boton_3)
            for llave, value in dic_fechas.items():
                esconder_label(value[3])
                esconder_label(value[2])
            if texto == "volver":
                if estado_anterior == "seleccionar_reporte_categoria":
                    estado, info = seleccionar_reporte_categoria(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif estado_anterior == "menu_reportes_comerciales":
                    estado, info = menu_reportes_comerciales(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif estado_anterior == "seleccionar_carpetas":
                    estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif estado == "convertir_archivos":
                    estado, info = seleccionar_reporte_categoria(app, window, central_widget, dimensiones, estado=estado, info=info)
                else:
                    estado, info = menu_inicial(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                info["Fecha"] = dic_fechas
                if estado == "convertir_archivos":
                    opciones = {"conservar_archivos": True}
                    estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="seleccionar_periodo", opciones=opciones)
                elif estado == "reporte_SH":
                    opciones = {"regenerar": True}
                    estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="seleccionar_periodo", opciones=opciones)
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    if incluir_anual:
        boton_2.clicked.connect(lambda:cambiar_botones_x(boton_2))
    boton_3.clicked.connect(lambda:limpiar_botones(boton_3))
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    for llave, value in dic_fechas.items():
        value[2].clicked.connect(lambda _, l=llave: cambiar_botones_fecha(l))
    event_loop.exec_()
    return estado, info

def seleccionar_categoria(app, window, central_widget, dimensiones, estado=None, info={}, estado_anterior=""):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    elegir_1 = False
    if estado_anterior == "menu_inicial":
        elegir_1 = True

    titulo = "Selección de reportes"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    lista_categorias = ["Reporte comercial", "Reporte tarifario", "Reporte técnico"]
    dic_categorias = {}
    lista_y = [escalar_valor(300, factor_escala),escalar_valor(450, factor_escala),escalar_valor(600, factor_escala)]
    for i in range(len(lista_categorias)):
        y_reporte = lista_y[i]
        elemento = lista_categorias[i]
        label_for = crear_label(elemento, central_widget, font_size=20)
        boton_for = crear_boton("", central_widget, font_size=42, padding=10, radius=10)
        boton_for.setFixedSize(escalar_valor(56, factor_escala), escalar_valor(56, factor_escala))
        boton_for.setParent(central_widget)
        label_for.setParent(central_widget)
        boton_for.move(escalar_valor(700, factor_escala),y_reporte)
        label_for.move(escalar_valor(800, factor_escala),y_reporte - escalar_valor(20, factor_escala))
        mostrar_label(boton_for)
        mostrar_label(label_for)
        dic_categorias[elemento] = [False, boton_for, label_for]
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala)))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(escalar_valor(150, factor_escala),escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    mostrar_label(image_button_1)
    label_nuevo_reporte = crear_label("", central_widget, font="bold", font_size=30)
    label_nuevo_reporte.move(escalar_valor(50, factor_escala), escalar_valor(980, factor_escala))
    label_nuevo_reporte.setParent(central_widget)
    esconder_label(label_nuevo_reporte)
    v_line_edit = crear_label("Nuevo reporte: ", central_widget, font_size=25, line_edit=True)
    v_line_edit.move(escalar_valor(700, factor_escala),escalar_valor(1000, factor_escala))
    v_line_edit.setParent(central_widget)
    mostrar_label(v_line_edit)
    label_check = QPushButton("", central_widget)
    pixmap_check = QPixmap(ruta_imagenes+"check.png")
    pixmap_check = pixmap_check.scaled(escalar_valor(320, factor_escala),escalar_valor(80, factor_escala), aspectRatioMode=1)
    icon_check = QIcon(pixmap_check)
    label_check.setIcon(icon_check)
    label_check.setIconSize(pixmap_check.size())
    label_check.move(escalar_valor(1660, factor_escala),escalar_valor(980, factor_escala))
    esconder_label(label_check)
    dic_texto = {"Reportes comerciales":"Valores de facturación, consumo y lecturas de clientes R y NR",
                "Reportes tarifarios":"Componentes tarifarios de los diferentes sectores de mercado para clientes R y NR",
                "Reportes técnicos":"Información respecto a los indicadores de calidad por la prestación de servicio público de GN"}

    event_loop = QEventLoop()
    def guardar_nombre(label_nuevo_reporte):
        codigo = v_line_edit.text().upper().strip()
        if len(codigo):
            QApplication.processEvents()
            label_nuevo_reporte.setText(codigo)
            mostrar_label(label_nuevo_reporte)
            QApplication.processEvents()
            mostrar_label(label_check)
    def cambiar_botones_reporte(llave):
        nonlocal dic_categorias
        if elegir_1:
            for elemento, lista_elemento in dic_categorias.items():
                boton_for = lista_elemento[1]
                boton_for.setText("")
                mostrar_label(boton_for)
        boton = dic_categorias[llave][1]
        if boton.text() == "X":
            boton.setText("")
            dic_categorias[elemento][0] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_categorias[elemento][0] = True
        mostrar_label(boton)
    def comprobar_dic(dic, pos):
        for _, lista_elemento in dic.items():
            if lista_elemento[pos]:
                return True
        return False
    def comprobar_aceptar():
        return comprobar_dic(dic_categorias, 0) and len(label_nuevo_reporte.text())
    def on_button_clicked(texto):
        nonlocal estado, info
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(image_button)
            esconder_label(boton_1)
            esconder_label(image_button_1)
            esconder_label(v_line_edit)
            esconder_label(label_nuevo_reporte)
            esconder_label(label_check)
            for _, lista_elemento in dic_categorias.items():
                esconder_label(lista_elemento[1])
                esconder_label(lista_elemento[2])
            if texto == "volver":
                if estado_anterior == "menu_inicial":
                    estado, info = menu_config_inicial(app, window, central_widget, dimensiones)
                elif estado_anterior == "menu_edicion_archivos":
                    estado, info = menu_edicion_archivos(app, window, central_widget, dimensiones, estado=estado, info=info)
                else:
                    estado, info = menu_seleccion(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                if estado_anterior == "menu_inicial":
                    info["Categoria"] = dic_categorias
                    info["Nuevo_reporte"] = label_nuevo_reporte.text()
                else:
                    estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado, info)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    v_line_edit.returnPressed.connect(lambda: guardar_nombre(label_nuevo_reporte))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    for elemento, lista_elemento in dic_categorias.items():
        lista_elemento[1].clicked.connect(lambda _, l=elemento: cambiar_botones_reporte(l))
    event_loop.exec_()
    return estado,info

def seleccionar_carpetas(app, window, central_widget, dimensiones, estado=None, info={}, estado_anterior=""):
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)

    titulo = "Selección de carpetas"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    dic_carpetas = {}
    lista_x_reportes = [escalar_valor(50, factor_escala), escalar_valor(900, factor_escala)]
    c_x = 0
    c_y = escalar_valor(300, factor_escala)
    c_c = 0
    for valor in lista_carpetas_extra:
        if valor not in dic_carpetas:
            dic_carpetas[valor] = None
        boton_for = crear_boton("", central_widget, font_size=48, padding=10, radius=10)
        label_for = crear_label(valor, central_widget, font_size=30)
        boton_for.setFixedSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala))
        boton_for.setParent(central_widget)
        label_for.setParent(central_widget)
        boton_for.move(lista_x_reportes[c_x] + escalar_valor(80, factor_escala), c_y)
        label_for.move(lista_x_reportes[c_x] + escalar_valor(180, factor_escala), c_y - escalar_valor(25, factor_escala))
        dic_carpetas[valor] = [False, boton_for, label_for]
        mostrar_label(label_for)
        mostrar_label(boton_for)
        c_c += 1
        c_y += escalar_valor(120, factor_escala)
        if c_c > 5:
            c_x += 1
            c_c = 0
            c_y = escalar_valor(300, factor_escala)
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala), escalar_valor(20, factor_escala))
    mostrar_label(image_button)

    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala)))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(escalar_valor(150, factor_escala),escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    mostrar_label(image_button_1)
    dic_texto = {"Reportes Nuevo SUI":"Información original, certificada y archivos .SUI reportada a la SSPD","Seguimiento":"Información de consecutivos de años anteriores, evidencias SOX\nhallazgos y mesas de ayuda",
                "ANS":"Acuerdos de Nivel de Servicio (información enviada por la áreas)","Reportes CREG":"Reportes de activos (cumplimiento del Anexo 18 Resolución CREG 202 de 2013)",
                "Reportes DANE":"Información de consumo y facturación de usuarios R y NR por sector de consumo enviada al DANE",
                "Reportes SH":"Información presentada a la Secretaria de Hacienda de Bogotá D.C.", "Reportes Naturgas":"", "Validador y Lineamientos":"Versiones de los lineamientos y validador SUI",
                "Monitoreo y Control":"Diferentes formatos de control de calidad de la información", "Tableu":"Flujo de Tableau para ejecutar el GRC1-SAP, incluyendo campos adicionales", 
                "Tablas maestras":"Tablas referentes de mercados relevantes e información de Divipola (DANE)"}
    event_loop = QEventLoop()
    def cambiar_botones_reporte(valor):
        nonlocal dic_carpetas
        boton = dic_carpetas[valor][1]
        if boton.text() == "X":
            boton.setText("")
            dic_carpetas[valor][0] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_carpetas[valor][0] = True
        mostrar_label(boton)
    def comprobar_dic(dic, pos):
        for llave, valor in dic.items():
            if valor[pos]:
                    return True
        return False
    def comprobar_aceptar():
        return comprobar_dic(dic_carpetas, 0)
    def on_button_clicked(texto):
        nonlocal estado, info
        if (texto == "aceptar" and comprobar_aceptar()) or (texto == "volver"):
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(image_button)
            esconder_label(boton_1)
            esconder_label(image_button_1)
            for llave, valor in dic_carpetas.items():
                esconder_label(valor[1])
                esconder_label(valor[2])
            if texto == "volver":
                estado, info = menu_edicion_archivos(app, window, central_widget, dimensiones, estado=estado, info=info)
            elif texto == "aceptar":
                info["Carpetas"] = dic_carpetas
                if estado == "convertir_archivos":
                    if dic_carpetas ['Reportes Nuevo SUI'][0]:
                        estado, info = seleccionar_reporte_categoria(app, window, central_widget, dimensiones, estado=estado, info=info, estado_anterior="seleccionar_carpetas")
                    else:
                        info["Categoria"] = {"Comercial":[True, None, None],
                                            "Tarifario":[True, None, None],
                                            "Tecnico":[True, None, None]}
                        dic_reportes = {}
                        for i, (llave, valor) in enumerate(reportes_disponibles.items()):
                            for elemento in valor:
                                if llave not in dic_reportes:
                                    dic_reportes[llave] = {}
                                if elemento not in dic_reportes[llave]:
                                    dic_reportes[llave][elemento] = None
                                dic_reportes[llave][elemento] = [True, None, None]
                        info["Reporte"] = dic_reportes
                        estado, info = seleccionar_periodo(app, window, central_widget, dimensiones, estado, info, estado_anterior="seleccionar_carpetas", c_meses=12)
                else:
                    estado, info = seleccionar_reporte(app, window, central_widget, dimensiones, estado=estado, info=info)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    for llave, valor in dic_carpetas.items():
        valor[1].clicked.connect(lambda _, l=llave: cambiar_botones_reporte(l))
    event_loop.exec_()
    return estado,info

def confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op, estado_anterior):
    estado = op
    info = None
    screen_width, screen_height = dimensiones
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    cuadro = crear_cuadro(central_widget, dimensiones)
    mostrar_label(cuadro)
    titulo_espacios = crear_label(texto, central_widget, font="bold", font_size=40, color="#030918", background_color="white")
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(400, factor_escala))
    mostrar_label(titulo_espacios)
    texto_1 = crear_label("¿Desea continuar con la selección?", central_widget, font_size=30, color="#030918", background_color="white")
    x = round((screen_width-texto_1.sizeHint().width())*0.5)
    texto_1.move(x, escalar_valor(600, factor_escala))
    mostrar_label(texto_1)
    boton_1 = crear_boton("Aceptar", central_widget)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x, escalar_valor(1040, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(texto_1)
        esconder_label(image_button)
        esconder_label(cuadro)
        esconder_label(boton_1)
        if texto == "volver":
            if estado_anterior == "menu_config_inicial":
                estado, info = menu_config_inicial(app, window, central_widget, dimensiones)
            else:
                estado, info = menu_inicial(app, window, central_widget, dimensiones)
        else:
            estado = texto
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked(op))
    event_loop.exec_()
    return estado, info

def lista_codigo_DANE(texto):
    lista_texto = texto.split(",")
    valores_aceptados = []
    for elemento in lista_texto:
        elemento = elemento.strip()
        num = None
        if elemento in dic_DANE_nombres:
            num = int(elemento)
        elif elemento in dic_DANE_nombres_inicio:
            num = int(dic_DANE_nombres_inicio[elemento])
        if num:
            if num not in valores_aceptados:
                valores_aceptados.append(num)
    valores_aceptados.sort()
    lista_texto_dane = [str(i) for i in valores_aceptados]
    lista_texto_dane_c = [",".join(lista_texto_dane[i:i+3]) for i in range(0, len(lista_texto_dane), 3)]
    lista_texto_dane_c = "\n".join(lista_texto_dane_c)
    return valores_aceptados, lista_texto_dane_c

def num_aceptado(texto):
    try:
        num = int(texto)
        if num > 0:
            return str(num)
        else:
            return ""
    except BaseException:
        return ""

def opciones_adicionales(app, window, central_widget, dimensiones, opciones={}, estado=None, info=None, estado_anterior=None):
    dic_adicionales_texto = {"codigo_DANE":"Código DANE", "valor_facturado":"Valor total facturado", "cantidad_filas":"Cantidad de filas", "inventario":"Inventario de suscriptores", "regenerar":"Regenerar archivos necesarios (form_estandar, resumen)",
                        "reportes_mensuales":"Reportes mensuales", "texto_regenerar":"_form_estandar, _resumen",
                    "usuarios_activos":"Info. usuarios activos", "sumatoria":f"Sumatoria {grupo_vanti}","facturas":"Cantidad de facturas emitidas",
                    "conservar_archivos":"Conservar los archivos originales", "cantidad_filas":"Cantidad de filas mínimo"}
    dic_explicacion = {"codigo_DANE":"Código DANE de 8 dígitos relacionad con diversas entidades geográficas,\ncomo departamentos, municipios, y localidades.",
                        "valor_facturado":"Incluir el valor facturado por los usuarios.\nValor de facturación por consumo y valor de facturación total.",
                        "cantidad_filas":"Selección de cantidad de filas mínimo.",
                        "inventario":"Incluir la información correspondiente del inventario de suscriptores.",
                        "regenerar":"Regenerar archivos necesarios (form_estandar, resumen).",
                        "reportes_mensuales":"Información a generar para los reportes mensuales.",
                        "texto_regenerar":"_form_estandar, _resumen.",
                        "usuarios_activos":"Info. usuarios activos.",
                        "sumatoria":f"Sumatoria {grupo_vanti}.",
                        "facturas":"Cantidad de facturas emitidas.",
                        "conservar_archivos":"Conservar los archivos originales.",
                        "cantidad_filas":"Cantidad de filas mínimo para la creación de un archivo .xlsx (valor máximo de 65.000)."}
    if not len(opciones):
        return estado, info
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    lista_cod_DANE = [f"{l}, {v}" for l,v in dic_DANE_nombres.items()]
    largo_lista_cod_DANE = len(lista_cod_DANE)
    lista_cod_DANE_c = []
    ancho_texto = escalar_valor(80, factor_escala)
    for i in range(0,largo_lista_cod_DANE,2):
        t1 = str(lista_cod_DANE[i])
        if i+1 < largo_lista_cod_DANE:
            t2 = str(lista_cod_DANE[i+1])
            espacio = " "*(ancho_texto-len(t1))
            lista_cod_DANE_c.append(t1+espacio+t2)
        else:
            lista_cod_DANE_c.append(t1)
    dic_texto_2 = {f"Códigos DANE {grupo_vanti}": lista_cod_DANE_c}
    titulo = "Opciones adicionales"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=50)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, escalar_valor(10, factor_escala))
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)
    label_codigo_DANE = crear_label("", central_widget, font="bold", font_size=12)
    label_codigo_DANE.move(escalar_valor(50, factor_escala), escalar_valor(980, factor_escala))
    label_codigo_DANE.setParent(central_widget)
    esconder_label(label_codigo_DANE)
    label_cantidad_filas = crear_label("", central_widget, font="bold", font_size=12)
    label_cantidad_filas.move(escalar_valor(50, factor_escala), escalar_valor(980, factor_escala))
    label_cantidad_filas.setParent(central_widget)
    esconder_label(label_cantidad_filas)
    cambio = escalar_valor(120, factor_escala)
    codigo_DANE = False
    if "codigo_DANE" in opciones:
        if opciones["codigo_DANE"]:
            v_line_edit = crear_label("Código DANE: ", central_widget, font_size=15, line_edit=True)
            x = round((screen_width-v_line_edit.sizeHint().width())*0.5)
            v_line_edit.move(x,escalar_valor(1000, factor_escala))
            v_line_edit.setParent(central_widget)
            mostrar_label(v_line_edit)
            cambio = escalar_valor(150, factor_escala)
            codigo_DANE = True
    cantidad_filas = False
    if "cantidad_filas" in opciones:
        if opciones["cantidad_filas"]:
            cantidad_filas = True
            v_line_edit = crear_label("Cantidad de filas mínimo: ", central_widget, font_size=15, line_edit=True)
            x = round((screen_width-v_line_edit.sizeHint().width())*0.5)
            v_line_edit.move(x,escalar_valor(1000, factor_escala))
            v_line_edit.setParent(central_widget)
            mostrar_label(v_line_edit)
    label_check = QPushButton("", central_widget)
    pixmap_check = QPixmap(ruta_imagenes+"check.png")
    pixmap_check = pixmap_check.scaled(escalar_valor(320, factor_escala),escalar_valor(80, factor_escala), aspectRatioMode=1)
    icon_check = QIcon(pixmap_check)
    label_check.setIcon(icon_check)
    label_check.setIconSize(pixmap_check.size())
    label_check.move(escalar_valor(1660, factor_escala),escalar_valor(980, factor_escala))
    esconder_label(label_check)
    lista_x_pos = [escalar_valor(50, factor_escala), escalar_valor(780, factor_escala), escalar_valor(1400, factor_escala)]
    c_x = 0
    c_y = escalar_valor(200, factor_escala)
    c_c = 0
    dic_opciones_botones = {}
    dic_texto = {}
    for llave, valor in opciones.items():
        dic_texto[dic_adicionales_texto[llave]] = dic_explicacion[llave]
        if llave != "codigo_DANE" and llave != "cantidad_filas":
            if llave not in dic_opciones_botones:
                dic_opciones_botones[llave] = None
            boton_for = crear_boton("", central_widget, font_size=48, padding=10, radius=10)
            label_for = crear_label(dic_adicionales_texto[llave], central_widget, font_size=20)
            boton_for.setFixedSize(escalar_valor(80, factor_escala),escalar_valor(80, factor_escala))
            boton_for.setParent(central_widget)
            label_for.setParent(central_widget)
            boton_for.move(lista_x_pos[c_x] + escalar_valor(80, factor_escala), c_y)
            label_for.move(lista_x_pos[c_x] + escalar_valor(150, factor_escala), c_y - escalar_valor(25, factor_escala))
            dic_opciones_botones[llave] = [False, boton_for, label_for]
            mostrar_label(label_for)
            mostrar_label(boton_for)
            c_c += 1
            c_y += cambio
            if c_c > 5:
                c_x += 1
                c_c = 0
                c_y = escalar_valor(200, factor_escala)
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,escalar_valor(1100, factor_escala))
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    size = escalar_qsize(pixmap.size(), factor_escala)
    pixmap = pixmap.scaled(
        size,
        aspectRatioMode=Qt.KeepAspectRatio,
        transformMode=Qt.SmoothTransformation
    )
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(escalar_valor(20, factor_escala),escalar_valor(20, factor_escala))
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(escalar_valor(80, factor_escala), escalar_valor(80, factor_escala)))
    image_button_1.setFixedSize(escalar_valor(150, factor_escala), escalar_valor(150, factor_escala))
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,escalar_valor(5, factor_escala))
    image_button_2 = QPushButton("", central_widget)
    pixmap_2 = QPixmap(ruta_imagenes+"lupa.png")
    icon_2 = QIcon(pixmap_2)
    image_button_2.setIcon(icon_2)
    image_button_2.setIconSize(QSize(escalar_valor(45, factor_escala), escalar_valor(45, factor_escala)))
    image_button_2.setFixedSize(escalar_valor(45, factor_escala), escalar_valor(45, factor_escala))
    image_button_2.move(escalar_valor(740, factor_escala), escalar_valor(1000, factor_escala))
    mostrar_label(image_button_1)
    if codigo_DANE:
        mostrar_label(image_button_2)

    event_loop = QEventLoop()
    def cambiar_botones_reporte(llave):
        nonlocal dic_opciones_botones
        boton = dic_opciones_botones[llave][1]
        if boton.text() == "X":
            boton.setText("")
            dic_opciones_botones[llave][0] = False
        elif boton.text() == "":
            boton.setText("X")
            dic_opciones_botones[llave][0] = True
        mostrar_label(boton)
    def guardar_nombre(label_codigo_DANE):
        nonlocal dic_opciones_botones
        codigo = v_line_edit.text()
        if len(codigo):
            dane_num, dane_text = lista_codigo_DANE(codigo)
            dic_opciones_botones["codigo_DANE"] = dane_num
            mostrar_label(label_check)
            esconder_label(label_codigo_DANE)
            label_codigo_DANE.setText(dane_text)
            label_codigo_DANE.repaint()
            QApplication.processEvents()
            mostrar_label(label_codigo_DANE)
    def guardar_num(label_cantidad_filas):
        nonlocal dic_opciones_botones
        codigo = v_line_edit.text()
        if len(codigo):
            num = num_aceptado(codigo)
            dic_opciones_botones["cantidad_filas"] = num
            if len(num):
                mostrar_label(label_check)
                esconder_label(label_cantidad_filas)
                label_cantidad_filas.setText(num)
                label_cantidad_filas.repaint()
                QApplication.processEvents()
                mostrar_label(label_cantidad_filas)
    def on_button_clicked(texto):
        nonlocal estado, info
        if texto == "aceptar" or texto == "volver":
            event_loop.quit()
            esconder_label(titulo_espacios)
            if codigo_DANE or cantidad_filas:
                esconder_label(v_line_edit)
            esconder_label(label_check)
            esconder_label(image_button)
            esconder_label(boton_1)
            esconder_label(label_codigo_DANE)
            esconder_label(label_cantidad_filas)
            esconder_label(image_button_1)
            esconder_label(image_button_2)
            for llave, valor in dic_opciones_botones.items():
                if llave != "codigo_DANE" and llave != "cantidad_filas":
                    esconder_label(valor[1])
                    esconder_label(valor[2])
            if texto == "volver":
                if estado_anterior == "menu_seleccion":
                    estado,info = menu_seleccion(app, window, central_widget, dimensiones, estado=estado, info=info)
                elif estado_anterior == "seleccionar_periodo":
                    estado, info = seleccionar_periodo(app, window, central_widget, dimensiones, estado=estado, info=info)
                else:
                    estado, info = menu_inicial(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                info["Opciones_adicionales"] = dic_opciones_botones
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto,dimensiones=dimensiones))
    image_button_2.clicked.connect(lambda: ventana_secundaria(central_widget,"Códigos DANE disponibles",dic_texto_2, lista=False,dimensiones=dimensiones))
    if codigo_DANE:
        v_line_edit.returnPressed.connect(lambda: guardar_nombre(label_codigo_DANE))
    if cantidad_filas:
        v_line_edit.returnPressed.connect(lambda: guardar_num(label_cantidad_filas))
    for llave, valor in dic_opciones_botones.items():
        if llave != "codigo_DANE":
            valor[1].clicked.connect(lambda _, l=llave: cambiar_botones_reporte(l))
    event_loop.exec_()
    return estado, info

def ventana_secundaria(central_widget, titulo, dic_texto, lista=True, dimensiones=(1920, 1200)):
    ventana = QDialog(central_widget)
    ventana.setWindowTitle(titulo)
    ventana.setGeometry(central_widget.geometry().left(), central_widget.geometry().top(), int(central_widget.width()*0.9), int(central_widget.height()*0.9))
    ventana.setStyleSheet(f"""QWidget{{background-color: #030918; border: 5px solid #030918}}""")
    layout = QVBoxLayout()
    screen_width = dimensiones[0]
    screen_height = dimensiones[1]
    factor_escala = calcular_factor_escala(screen_width, screen_height)
    font_size = escalar_valor(24, factor_escala)
    font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    font_id_1 = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family_1 = QFontDatabase().applicationFontFamilies(font_id_1)[0]
    for llave, valor in dic_texto.items():
        label = QLabel(llave, ventana)
        label.setStyleSheet(f"color: white;font-size: {int(font_size*1.5)}px;font-family: '{font_family_1}'")
        layout.addWidget(label)
        if isinstance(valor, str):
            label_1 = QLabel(valor, ventana)
            label_1.setStyleSheet(f"color: white;font-size: {font_size}px;font-family: '{font_family}'")
            layout.addWidget(label_1)
        elif isinstance(valor, list):
            if lista:
                for elemento in valor:
                    label_2 = QLabel(elemento[0], ventana)
                    label_2.setStyleSheet(f"color: white;font-size: {int(font_size*1.65)}px;font-family: '{font_family_1}'")
                    layout.addWidget(label_2)
                    label_3 = QLabel(elemento[1], ventana)
                    label_3.setStyleSheet(f"color: white;font-size: {font_size}px;font-family: '{font_family}'")
                    layout.addWidget(label_3)
            else:
                for elemento in valor:
                    label_2 = QLabel(elemento, ventana)
                    label_2.setStyleSheet(f"color: white;font-size: {int(font_size*1.4)}px;font-family: '{font_family_1}'")
                    layout.addWidget(label_2)
    content_widget = QWidget()
    content_widget.setLayout(layout)
    scroll_area = QScrollArea()
    scroll_area.setWidget(content_widget)
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet(f"""
        QScrollArea {{border: 5px solid white;}}
        QScrollBar:vertical {{background-color: #030918;width: 25px;border-radius: 6px;}}
        QScrollBar:horizontal {{background-color: #030918;height: 12px;border-radius: 6px;}}
        QScrollBar::handle:vertical {{background-color: white;border-radius: 12px;}}
        QScrollBar::handle:horizontal {{background-color: white;border-radius: 6px;}}""")
    ventana_layout = QVBoxLayout(ventana)
    ventana_layout.addWidget(scroll_area)
    ventana.setLayout(ventana_layout)
    ventana.exec_()
