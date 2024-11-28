import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QPushButton, QScrollArea, QLineEdit
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import Qt, QEventLoop, QSize
import ruta_principal as mod_rp
import json
import time
from datetime import datetime, timedelta

global ruta_principal, ruta_codigo, ruta_constantes, rutanuevo_sui, ruta_archivos, ruta_fuentes, ruta_imagenes, fuente_texto, azul_vanti, dic_colores, nombre_aplicativo, lista_anios, dic_meses, lista_meses, lista_trimestres,reportes_disponibles,fecha_actual,lista_carpetas_extra,dic_DANE_nombres,dic_DANE_nombres_inicio
global ruta_fuente, grupo_vanti,ruta_fuente_negrilla
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
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"vanti.png")
    pixmap = pixmap.scaled(320,80, aspectRatioMode=1)
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(int(screen_width-image_button.sizeHint().width())-20,int(screen_height-image_button.sizeHint().height())-20)
    mostrar_label(image_button)
    window.setCentralWidget(central_widget)
    window.setWindowTitle(nombre_aplicativo)
    window.setGeometry(100, 100, 300, 200)
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
    app_vanti = crear_label("APP VANTI", central_widget, font="bold", font_size=80)
    x = round((screen_width-app_vanti.sizeHint().width())*0.5)
    app_vanti.move(x, 100)
    mostrar_label(app_vanti)
    titulo_1 = crear_label("Vicepresidencia de Estrategia y Finanzas", central_widget, font_size=20)
    x = round((screen_width-titulo_1.sizeHint().width())*0.5)
    titulo_1.move(x, 550)
    mostrar_label(titulo_1)
    titulo_2 = crear_label("Dirección Regulación, Márgenes y Tarifas", central_widget, font_size=30)
    x = round((screen_width-titulo_2.sizeHint().width())*0.5)
    titulo_2.move(x, 380)
    mostrar_label(titulo_2)
    button = crear_boton("INICIAR", central_widget, font_size=40, font="bold")
    x = round((screen_width-button.sizeHint().width())*0.5)
    button.move(x,800)
    button.setParent(central_widget)
    mostrar_label(button)
    event_loop = QEventLoop()
    def on_button_clicked():
        event_loop.quit()
        esconder_label(app_vanti)
        esconder_label(titulo_1)
        esconder_label(titulo_2)
        esconder_label(button)
    button.clicked.connect(on_button_clicked)
    event_loop.exec_()

def menu_inicial(app, window, central_widget, dimensiones, estado=None, info=None):
    screen_width = dimensiones[0]
    titulo = "INICIO"
    label_1 = crear_label(titulo, central_widget, font="bold", font_size=80)
    x = round((screen_width-label_1.sizeHint().width())*0.5)
    label_1.move(x, 50)
    mostrar_label(label_1)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)
    boton_1 = crear_boton("Configuración inicial", central_widget, font_size=35)
    boton_2 = crear_boton("Edición de archivos", central_widget, font_size=35)
    boton_3 = crear_boton("Reportes comerciales", central_widget, font_size=35)
    boton_4 = crear_boton("Reportes tarifarios", central_widget, font_size=35)
    boton_5 = crear_boton("Reportes técnicos", central_widget, font_size=35)
    boton_6 = crear_boton("Cumplimientos de reportes regulatorios", central_widget, font_size=35)
    boton_7 = crear_boton("Dashboard", central_widget, font_size=50)
    botones = [boton_1, boton_2, boton_3, boton_4, boton_5, boton_6, boton_7]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,400)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,600)
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_5.move(x,800)
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,400)
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,600)
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    boton_6.move(x,800)
    boton_6.setParent(central_widget)
    mostrar_label(boton_6)
    x = round((((screen_width)-max_width)*0.5))
    boton_7.move(x,1000)
    boton_7.setParent(central_widget)
    mostrar_label(boton_7)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    mostrar_label(image_button_1)
    dic_texto = {"Configuración inicial":"Configuración del aplicativo. Recomendado si no existen las carpetas o archivos necesarios en el dispositivo",
                "Edición de archivos":"Almacenamiento, manipulación o estandarización de archivos",
                "Reportes comerciales":"Actividades con reportes comerciales como información por sectores de consumo, información por sectores de consumo subsidiadios,\ncompensaciones, desviaciones significativas, reporte DANE, reporte Secretaria de Hacienda de Bogotá D.C.\nComprobación de la calidad de la información o comparación entre archivos de certificación, calidad (CLD) y/o producción (PRD)",
                "Reportes tarifarios":"Actividades con reportes tarifarios\n",
                "Reportes técnicos":"Actividades con reportes técnicos como indicadores técnicos (IPLI,IO,IRST-EG) o\nreporte de suspensiones",
                "Cumplimientos de reportes regulatorios":"Indicadores de cumplimientos de reportes regulatorios como porcentaje de atención a solicitudes,\nreportes trimestrales, matriz de requerimientos, gastos AOM, pagos contribuciones MME o\ntarifas distribuidoras de GN en Colombia",
                "Dashboard":"Creación y almacenamiento slides Dashboard "}
    event_loop = QEventLoop()
    def on_button_clicked(evento):
        nonlocal estado, info
        event_loop.quit()
        esconder_label(label_1)
        esconder_label(image_button)
        esconder_label(image_button_1)
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
        else:
            pantalla_inicio(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("config_inicial"))
    boton_2.clicked.connect(lambda:on_button_clicked("edicion_archivos"))
    boton_3.clicked.connect(lambda:on_button_clicked("reportes_comerciales"))
    boton_4.clicked.connect(lambda:on_button_clicked("reportes_tarifarios"))
    boton_5.clicked.connect(lambda:on_button_clicked("reportes_tecnicos"))
    boton_6.clicked.connect(lambda:on_button_clicked("cumplmiento_reportes"))
    boton_7.clicked.connect(lambda:on_button_clicked("dashboard"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado, info

def menu_config_inicial(app, window, central_widget, dimensiones):
    screen_width = dimensiones[0]
    estado = None
    info = None

    titulo = "Configuración inicial"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 40)
    mostrar_label(titulo_espacios)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)

    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    mostrar_label(image_button_1)
    dic_texto = {"Creación de espacio de trabajo":"Creación de las carpetas necesarias para el correcto funcionamiento del aplicativo.\nCreación y/o actualización de constantes como tablas, archivos o imágenes usados por el aplicativo.",
                "Agregar año actual":"Incluir el año actual a la información generada (archivos y carpetas) por el aplicativo.\nSe debe ejecutar está función al inicio de cada año",
                "Editar un reporte existente":"Edición de archvios de tipo .json\nEstos archivos representan las regalmentaciones utilizadas por cada reporte de la SSPD  según el lineamiento específico.",
                "Crear un nuevo reporte":"Creación de un nuevo tipo de reporte a utilizar (archivo .json)\n"}
    boton_1 = crear_boton("Creación de espacio de trabajo", central_widget)
    boton_2 = crear_boton("Agregar año actual", central_widget)
    boton_3 = crear_boton("Editar un reporte existente", central_widget)
    boton_4 = crear_boton("Crear un nuevo reporte", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,500)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,800)
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,500)
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,800)
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
        else:
            estado, info = menu_inicial(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("crear_carpetas"))
    boton_2.clicked.connect(lambda:on_button_clicked("agregar_anio"))
    boton_3.clicked.connect(lambda:on_button_clicked("editar_reporte"))
    boton_4.clicked.connect(lambda:on_button_clicked("agregar_reporte"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado, info

def menu_edicion_archivos(app, window, central_widget, dimensiones, estado=None, info={}):
    screen_width = dimensiones[0]
    titulo = "Edición de archivos"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 40)
    mostrar_label(titulo_espacios)
    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)
    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    mostrar_label(image_button_1)
    dic_texto = {"Conversión archivos .txt a .csv":"Convesión de archivos .txt a .csv en un ubicación seleccionada",
                "Almacenar archivos":"Almacenamiento de archivos en la carpeta \'Guardar_archivos\' en el formato del aplicativo\nEl formato necesario es \'Reporte_Filial_Año_Mes\'",
                "Estandarización de archivos":"Generación de archivos de tipo _form_estandar.csv\nEstos archivos contienen las columnas escritas según la información del lineamiento y los archivos .json",
                "Generar archivos resumen":"Generación de archivos de tipo _resumen.csv\nEstos archivos contienen las columnas escritas según la información del lineamiento y los archivos .json",
                "Revisión de archivos existentes":"Revisión de los archivos disponibles en las carpetas con el fin de conocer la información\nalmacenada y disponible para el procesamiento del aplicativo",
                "Revisión de reportes existentes":"Revisión de los reportes disponibles y aceptados por el aplicativo según los archivos .json\n"}
    boton_1 = crear_boton("Conversión archivos .txt a .csv", central_widget)
    boton_2 = crear_boton("Almacenar archivos", central_widget)
    boton_3 = crear_boton("Estandarización de archivos", central_widget)
    boton_4 = crear_boton("Generar archivos resumen", central_widget)
    boton_5 = crear_boton("Revisión de archivos existentes", central_widget)
    boton_6 = crear_boton("Revisión de reportes existentes", central_widget)
    botones = [boton_1, boton_2, boton_3, boton_4, boton_5, boton_6]
    max_width = max([boton.sizeHint().width() for boton in botones])
    for boton in botones:
        boton.setFixedWidth(max_width)
    x = round(((screen_width*0.5)-max_width)*0.5)
    boton_1.move(x,400)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,600)
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_5.move(x,800)
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,400)
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,600)
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    boton_6.move(x,800)
    boton_6.setParent(central_widget)
    mostrar_label(boton_6)

    event_loop = QEventLoop()
    def on_button_clicked(texto):
        nonlocal estado
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
        esconder_label(image_button_1)
        if texto == "volver":
            estado, info = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "almacenar_archivos":
            estado = texto
        else:
            #TODO: Llamar selección para cada carpeta
            estado, info = menu_inicial(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("convertir_archivos"))
    boton_2.clicked.connect(lambda:on_button_clicked("almacenar_archivos"))
    boton_3.clicked.connect(lambda:on_button_clicked("archivos_estandar"))
    boton_4.clicked.connect(lambda:on_button_clicked("archivos_resumen"))
    boton_5.clicked.connect(lambda:on_button_clicked("archivos_existentes"))
    boton_6.clicked.connect(lambda:on_button_clicked("reportes_existentes"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado, info

def menu_reportes_comerciales(app, window, central_widget, dimensiones, estado=None, info={}):
    screen_width = dimensiones[0]
    titulo = "Reportes comerciales"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 40)
    mostrar_label(titulo_espacios)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)

    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
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
    boton_1.move(x,400)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    boton_3.move(x,600)
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)
    boton_5.move(x,800)
    boton_5.setParent(central_widget)
    mostrar_label(boton_5)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,400)
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)
    boton_4.move(x,600)
    boton_4.setParent(central_widget)
    mostrar_label(boton_4)
    boton_6.move(x,800)
    boton_6.setParent(central_widget)
    mostrar_label(boton_6)
    x = round((((screen_width)-max_width)*0.5))
    boton_7.move(x,1000)
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
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado,info

def menu_reporte_comercial(app, window, central_widget, dimensiones, estado=None, info={}):
    screen_width = dimensiones[0]

    titulo = "Reportes comerciales\npor sector de consumo"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=75)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 40)
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)

    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
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
    boton_1.move(x,700)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    x = round((((screen_width*0.5)-max_width)*0.5)+(screen_width*0.5))
    boton_2.move(x,700)
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
        else:
            estado = texto
            estado,info = menu_seleccion(app, window, central_widget, dimensiones, "menu_reporte_comercial", estado, info)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("reporte_comercial_sector_consumo"))
    boton_2.clicked.connect(lambda:on_button_clicked("reporte_comercial_sector_consumo_subsidio"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado,info

def menu_seleccion(app, window, central_widget, dimensiones, estado_anterior=None, estado=None, info={}):
    screen_width = dimensiones[0]

    titulo = "Selección información"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 10)
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)

    t_filial = crear_label("Filiales", central_widget, font="bold", font_size=50)
    t_filial.move(50, 150)
    t_filial.setParent(central_widget)
    mostrar_label(t_filial)

    t_periodo = crear_label("Periodos", central_widget, font="bold", font_size=50)
    t_periodo.move(700, 150)
    t_periodo.setParent(central_widget)
    mostrar_label(t_periodo)

    boton_2 = crear_boton("", central_widget, font_size=60, padding=5)
    boton_2.setFixedSize(60,60)
    boton_2.move(1200,210)
    boton_2.setParent(central_widget)
    mostrar_label(boton_2)

    t_anual = crear_label("Anual", central_widget, font="bold", font_size=40)
    t_anual.move(1300, 170)
    t_anual.setParent(central_widget)
    mostrar_label(t_anual)
    anual = False

    f1 = crear_boton("", central_widget, font_size=60, padding=5)
    f1.setFixedSize(80,80)
    f1.move(50,350)
    f1.setParent(central_widget)
    mostrar_label(f1)

    t_f1 = crear_label("VANTI", central_widget, font="bold", font_size=40)
    t_f1.move(150, 310)
    t_f1.setParent(central_widget)
    mostrar_label(t_f1)

    f2 = crear_boton("", central_widget, font_size=60, padding=5)
    f2.setFixedSize(80,80)
    f2.move(50,500)
    f2.setParent(central_widget)
    mostrar_label(f2)

    t_f2 = crear_label("GNCB", central_widget, font="bold", font_size=40)
    t_f2.move(150, 460)
    t_f2.setParent(central_widget)
    mostrar_label(t_f2)

    f3 = crear_boton("", central_widget, font_size=60, padding=5)
    f3.setFixedSize(80,80)
    f3.move(50,650)
    f3.setParent(central_widget)
    mostrar_label(f3)

    t_f3 = crear_label("GNCR", central_widget, font="bold", font_size=40)
    t_f3.move(150, 610)
    t_f3.setParent(central_widget)
    mostrar_label(t_f3)

    f4 = crear_boton("", central_widget, font_size=60, padding=5)
    f4.setFixedSize(80,80)
    f4.move(50,800)
    f4.setParent(central_widget)
    mostrar_label(f4)

    t_f4 = crear_label("GOR", central_widget, font="bold", font_size=40)
    t_f4.move(150, 760)
    t_f4.setParent(central_widget)
    mostrar_label(t_f4)

    f5 = crear_boton("", central_widget, font_size=60, padding=5)
    f5.setFixedSize(80,80)
    f5.move(50,950)
    f5.setParent(central_widget)
    mostrar_label(f5)

    t_f5 = crear_label("Todas", central_widget, font="bold", font_size=40)
    t_f5.move(150, 910)
    t_f5.setParent(central_widget)
    mostrar_label(t_f5)

    dic_botones_filiales = {"VANTI":[f1,t_f1,False], "GNCB":[f2,t_f2,False], "GNCR":[f3,t_f3,False], "GOR":[f4,t_f4,False], "Todas":[f5,t_f5,False]}

    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,1100)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)

    boton_3 = crear_boton("Limpiar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_3.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_3.move(1700,150)
    boton_3.setParent(central_widget)
    mostrar_label(boton_3)

    if len(lista_anios) >=3 :
        lista_anios_sel = lista_anios[-3:]
    else:
        lista_anios_sel = lista_anios.copy()
    lista_fechas_sel = []
    dic_fechas = {}
    x_fecha = 620
    for anio in lista_anios_sel:
        y_fecha = 300
        for mes in lista_meses:
            llave = anio+" / "+mes[:3]
            lista_fechas_sel.append(llave)
            dic_fechas[llave] = [(anio, mes), False, crear_boton("", central_widget, font_size=42, padding=1, radius=5), crear_label(llave, central_widget, font_size=15)]
            dic_fechas[llave][2].setFixedSize(48,48)
            dic_fechas[llave][2].setParent(central_widget)
            dic_fechas[llave][3].setParent(central_widget)
            dic_fechas[llave][2].move(x_fecha,y_fecha)
            dic_fechas[llave][3].move(x_fecha + 100, y_fecha-10)
            y_fecha += 65
            mostrar_label(dic_fechas[llave][2])
            mostrar_label(dic_fechas[llave][3])
        x_fecha += 450

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
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
            for key, value in dic_botones_filiales.items():
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
            print(llave_activa)
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
                    if contador > 12:
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
            #llave_activa = boton_fecha_selected()
            #if llave_activa:

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
            

    def limpiar_botones(boton):
        nonlocal dic_fechas, dic_botones_filiales, anual, boton_2
        boton_2.setText("")
        anual = False
        for llave, value in dic_fechas.items():
            value[2].setText("")
            value[1] = False
        for llave, value in dic_botones_filiales.items():
            value[0].setText("")
            value[2] = False

    def on_button_clicked(texto):
        nonlocal estado, info
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
            esconder_label(t_anual)
            esconder_label(boton_2)
            esconder_label(boton_3)
            for llave, value in dic_fechas.items():
                esconder_label(value[3])
                esconder_label(value[2])
            if texto == "volver":
                if estado_anterior == "menu_reporte_comercial":
                    estado,info = menu_reporte_comercial(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                info["Fecha"] = dic_fechas
                info["Filial"] = dic_botones_filiales
                estado,info = seleccionar_reporte(app, window, central_widget, dimensiones, estado, info)

    f1.clicked.connect(lambda: cambiar_botones("VANTI"))
    f2.clicked.connect(lambda: cambiar_botones("GNCB"))
    f3.clicked.connect(lambda: cambiar_botones("GNCR"))
    f4.clicked.connect(lambda: cambiar_botones("GOR"))
    f5.clicked.connect(lambda: cambiar_botones("Todas"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    boton_2.clicked.connect(lambda:cambiar_botones_x(boton_2))
    boton_3.clicked.connect(lambda:limpiar_botones(boton_3))
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    for llave, value in dic_fechas.items():
        value[2].clicked.connect(lambda _, l=llave: cambiar_botones_fecha(l))
    event_loop.exec_()
    return estado,info

def seleccionar_reporte(app, window, central_widget, dimensiones, estado=None, info={}):
    screen_width = dimensiones[0]

    titulo = "Selección de reportes"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 10)
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)

    t_comercial = crear_label("Reportes comerciales", central_widget, font="bold", font_size=32)
    t_comercial.move(50, 150)
    t_comercial.setParent(central_widget)
    mostrar_label(t_comercial)

    t_tarifario = crear_label("Reportes tarifarios", central_widget, font="bold", font_size=32)
    t_tarifario.move(780, 150)
    t_tarifario.setParent(central_widget)
    mostrar_label(t_tarifario)

    t_tecnico = crear_label("Reportes técnicos", central_widget, font="bold", font_size=32)
    t_tecnico.move(1400, 150)
    t_tecnico.setParent(central_widget)
    mostrar_label(t_tecnico)

    #reportes_disponibles
    dic_reportes = {}
    lista_x_reportes = [50, 780, 1400]
    for i, (llave, valor) in enumerate(reportes_disponibles.items()):
        y_reporte = 300
        for elemento in valor:
            if elemento != "GRTT2SAP":
                if llave not in dic_reportes:
                    dic_reportes[llave] = {}
                if elemento not in dic_reportes[llave]:
                    dic_reportes[llave][elemento] = None
                boton_for = crear_boton("", central_widget, font_size=42, padding=10, radius=10)
                label_for = crear_label(elemento, central_widget, font_size=20)
                boton_for.setFixedSize(56,56)
                boton_for.setParent(central_widget)
                label_for.setParent(central_widget)
                boton_for.move(lista_x_reportes[i] + 80,y_reporte)
                label_for.move(lista_x_reportes[i] + 180, y_reporte - 15)
                dic_reportes[llave][elemento] = [False, boton_for, label_for]
                mostrar_label(label_for)
                mostrar_label(boton_for)
                y_reporte += 80
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,1100)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)

    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    mostrar_label(image_button_1)
    dic_texto = {"Reportes comerciales":[("GRC1","Información comercial de usuarios regulados"),("GRC2","Información comercial de suministro, transporte, distribución y comercialización"),("GRC3","Información de compensación sector residencial y\nno residencial usuarios regulados"),("GRTT2","Inventario de suscriptores"),("DS56","Usuarios con consumos estacionales"),("DS57","Investigaciones por Desviaciones Significativas"),("DS58"," Resultados Investigaciones por Desviaciones Significativas")],
                "Reportes tarifarios":[("GRT1","Estructura tarifaria de gas combustible por redes"),("GRT3","Opción tarifaria")],
                "Reportes técnicos":[("GRS1","Información de suspensiones"),("GRCS1","Información de Respuesta a Servicio Técnico"),("GRCS2","Consolidación de indicadores"),("GRCS3","Información de Presión en Líneas Individuales y Nivel de Odorización"),("GRCS7","Revisiones previas y Revisiones Periódicas Obligatorias - RPO"),("GRCS9","Revisiones Periódicas Obligatorias y revisiones previas\n - cuentas no normalizadas")]}

    event_loop = QEventLoop()

    def cambiar_botones_reporte(llave, valor):
        nonlocal dic_reportes
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
                estado, info = menu_seleccion(app, window, central_widget, dimensiones)
            elif texto == "aceptar":
                info["Reporte"] = dic_reportes
                estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado, info)

    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    for llave, dic_llave in dic_reportes.items():
        for reporte, lista_reporte in dic_llave.items():
            lista_reporte[1].clicked.connect(lambda _, l=llave, v=reporte: cambiar_botones_reporte(l, v))
    event_loop.exec_()
    return estado,info

def seleccionar_carpetas(app, window, central_widget, dimensiones, estado=None, info={}):
    screen_width = dimensiones[0]

    titulo = "Selección de carpetas"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=60)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 10)
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)

    #reportes_disponibles
    dic_carpetas = {}
    lista_x_reportes = [50, 900]
    c_x = 0
    c_y = 300
    c_c = 0
    for valor in lista_carpetas_extra:
        if valor not in dic_carpetas:
            dic_carpetas[valor] = None
        boton_for = crear_boton("", central_widget, font_size=48, padding=10, radius=10)
        label_for = crear_label(valor, central_widget, font_size=30)
        boton_for.setFixedSize(80,80)
        boton_for.setParent(central_widget)
        label_for.setParent(central_widget)
        boton_for.move(lista_x_reportes[c_x] + 80, c_y)
        label_for.move(lista_x_reportes[c_x] + 180, c_y - 25)
        dic_carpetas[valor] = [False, boton_for, label_for]
        mostrar_label(label_for)
        mostrar_label(boton_for)
        c_c += 1
        c_y += 120
        if c_c > 5:
            c_x += 1
            c_c = 0
            c_y = 300
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,1100)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)

    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))  # Ajusta el tamaño del ícono
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    mostrar_label(image_button_1)
    dic_texto = {"Carpeta 1":"info","Carpeta 2":"info","Carpeta 3":"info","Carpeta 4":"info","Carpeta 5":"info"}
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
                estado, info = seleccionar_reporte(app, window, central_widget, dimensiones, estado, info)
            elif texto == "aceptar":
                info["Carpetas"] = dic_carpetas
                estado, info = opciones_adicionales(app, window, central_widget, dimensiones, estado=estado, info=info)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    for llave, valor in dic_carpetas.items():
        valor[1].clicked.connect(lambda _, l=llave: cambiar_botones_reporte(l))
    event_loop.exec_()
    return estado,info

def confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op, estado_anterior):
    estado = op
    info = None
    screen_width, screen_height = dimensiones

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)

    cuadro = crear_cuadro(central_widget, dimensiones)
    mostrar_label(cuadro)

    titulo_espacios = crear_label(texto, central_widget, font="bold", font_size=40, color="#030918", background_color="white")
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 400)
    mostrar_label(titulo_espacios)

    texto_1 = crear_label("¿Desea continuar con la selección?", central_widget, font_size=30, color="#030918", background_color="white")
    x = round((screen_width-texto_1.sizeHint().width())*0.5)
    texto_1.move(x, 600)
    mostrar_label(texto_1)

    boton_1 = crear_boton("Aceptar", central_widget)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,1040)
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
    lista_texto_dane = [str(i) for i in valores_aceptados]
    return valores_aceptados, ", ".join(lista_texto_dane)

def opciones_adicionales(app, window, central_widget, dimensiones, opciones=[], estado=None, info=None, estado_anterior=None):
    opciones = {"regenerar":True, "codigo_DANE":True, "sumatoria":True, "valor_facturado":True, "facturas":True}
    dic_adicionales = {"codigo_DANE":False, "valor_facturado":False, "cantidad_filas":False, "inventario":False, "regenerar":False,
                        "reportes_mensuales":False, "texto_regenerar":"_form_estandar, _resumen",
                    "usuarios_activos":False, "sumatoria":False, "reporte_consumo_anual":False, "facturas":False}
    dic_adicionales_texto = {"codigo_DANE":"Código DANE", "valor_facturado":"Valor total facturado", "cantidad_filas":"Cantidad de filas", "inventario":"Inventario de suscriptores", "regenerar":"Regenerar archivos necesarios",
                        "reportes_mensuales":"Reportes mensuales", "texto_regenerar":"_form_estandar, _resumen",
                    "usuarios_activos":"Info. usuarios activos", "sumatoria":f"Sumatoria {grupo_vanti}","facturas":"Cantidad de facturas emitidas"}
    if not len(opciones):
        return dic_adicionales
    screen_width = dimensiones[0]

    #ventana_secundaria
    lista_cod_DANE = [f"{l}, {v}" for l,v in dic_DANE_nombres.items()]
    dic_texto_2 = {f"Códigos DANE {grupo_vanti}": lista_cod_DANE}
    titulo = "Opciones adicionales"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=50)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 10)
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)

    label_codigo_DANE = crear_label("", central_widget, font="bold", font_size=12)
    label_codigo_DANE.move(50, 980)
    label_codigo_DANE.setParent(central_widget)
    esconder_label(label_codigo_DANE)

    cambio = 120
    if "codigo_DANE" in opciones:
        if opciones["codigo_DANE"]:
            v_line_edit = crear_label("Código DANE: ", central_widget, font_size=15, line_edit=True)
            x = round((screen_width-v_line_edit.sizeHint().width())*0.5)
            v_line_edit.move(x,1000)
            v_line_edit.setParent(central_widget)
            mostrar_label(v_line_edit)
            codigo_DANE = True
            cambio = 150
    label_check = QPushButton("", central_widget)
    pixmap_check = QPixmap(ruta_imagenes+"check.png")
    pixmap_check = pixmap_check.scaled(320,80, aspectRatioMode=1)
    icon_check = QIcon(pixmap_check)
    label_check.setIcon(icon_check)
    label_check.setIconSize(pixmap_check.size())
    label_check.move(1660,980)
    esconder_label(label_check)
    lista_x_pos = [50, 780, 1400]
    c_x = 0
    c_y = 200
    c_c = 0
    dic_opciones_botones = {}
    for llave, valor in opciones.items():
        if llave != "codigo_DANE":
            if llave not in dic_opciones_botones:
                dic_opciones_botones[llave] = None
            boton_for = crear_boton("", central_widget, font_size=48, padding=10, radius=10)
            label_for = crear_label(dic_adicionales_texto[llave], central_widget, font_size=20)
            boton_for.setFixedSize(80,80)
            boton_for.setParent(central_widget)
            label_for.setParent(central_widget)
            boton_for.move(lista_x_pos[c_x] + 80, c_y)
            label_for.move(lista_x_pos[c_x] + 150, c_y - 25)
            dic_opciones_botones[llave] = [False, boton_for, label_for]
            mostrar_label(label_for)
            mostrar_label(boton_for)
            c_c += 1
            c_y += cambio
            if c_c > 5:
                c_x += 1
                c_c = 0
                c_y = 200
    boton_1 = crear_boton("Aceptar", central_widget, font_size=25)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,1100)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)

    image_button = QPushButton("", central_widget)
    pixmap = QPixmap(ruta_imagenes+"flecha.png")
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())
    image_button.move(20,20)
    mostrar_label(image_button)

    image_button_1 = QPushButton("", central_widget)
    pixmap_1 = QPixmap(ruta_imagenes+"lupa.png")
    icon_1 = QIcon(pixmap_1)
    image_button_1.setIcon(icon_1)
    image_button_1.setIconSize(QSize(80, 80))
    image_button_1.setFixedSize(150, 150)
    x = round((screen_width-(image_button_1.sizeHint().width()))*0.95)
    image_button_1.move(x,5)
    image_button_2 = QPushButton("", central_widget)
    pixmap_2 = QPixmap(ruta_imagenes+"lupa.png")
    icon_2 = QIcon(pixmap_2)
    image_button_2.setIcon(icon_2)
    image_button_2.setIconSize(QSize(45, 45))
    image_button_2.setFixedSize(45, 45)
    image_button_2.move(740,1000)
    mostrar_label(image_button_1)
    mostrar_label(image_button_2)
    dic_texto = {"Opción 1":"info","Opción 2":"info","Opción 3":"info","Opción 4":"info","Opción 5":"info"}

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
            QApplication.processEvents()
            label_codigo_DANE.setText(dane_text)
            mostrar_label(label_codigo_DANE)
            QApplication.processEvents()
            mostrar_label(label_check)
    def on_button_clicked(texto):
        nonlocal estado, info
        if texto == "aceptar" or texto == "volver":
            event_loop.quit()
            esconder_label(titulo_espacios)
            esconder_label(v_line_edit)
            esconder_label(label_check)
            esconder_label(image_button)
            esconder_label(boton_1)
            esconder_label(label_codigo_DANE)
            esconder_label(image_button_1)
            esconder_label(image_button_2)
            for llave, valor in dic_opciones_botones.items():
                if llave != "codigo_DANE":
                    esconder_label(valor[1])
                    esconder_label(valor[2])
            if texto == "volver":
                estado, info = seleccionar_carpetas(app, window, central_widget, dimensiones, estado, info)
            elif texto == "aceptar":
                info["Opciones_adicionales"] = dic_opciones_botones
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("aceptar"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    image_button_2.clicked.connect(lambda: ventana_secundaria(central_widget,"Códigos DANE disponibles",dic_texto_2, lista=False))
    v_line_edit.returnPressed.connect(lambda: guardar_nombre(label_codigo_DANE))
    for llave, valor in dic_opciones_botones.items():
        if llave != "codigo_DANE":
            valor[1].clicked.connect(lambda _, l=llave: cambiar_botones_reporte(l))
    event_loop.exec_()
    return estado, info

def ventana_secundaria(central_widget, titulo, dic_texto, lista=True):
    ventana = QDialog(central_widget)
    ventana.setWindowTitle(titulo)
    ventana.setGeometry(central_widget.geometry().left(), central_widget.geometry().top(), int(central_widget.width()*0.9), int(central_widget.height()*0.9))
    ventana.setStyleSheet(f"""QWidget{{background-color: #030918; border: 5px solid #030918}}""")
    layout = QVBoxLayout()
    font_size = 20
    font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    font_id_1 = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family_1 = QFontDatabase().applicationFontFamilies(font_id_1)[0]
    for llave, valor in dic_texto.items():
        label = QLabel(llave, ventana)
        label.setStyleSheet(f"color: white;font-size: {int(font_size*1.8)}px;font-family: '{font_family_1}'")
        layout.addWidget(label)
        if isinstance(valor, str):
            label_1 = QLabel(valor, ventana)
            label_1.setStyleSheet(f"color: white;font-size: {font_size}px;font-family: '{font_family}'")
            layout.addWidget(label_1)
        elif isinstance(valor, list):
            if lista:
                for elemento in valor:
                    label_2 = QLabel(elemento[0], ventana)
                    label_2.setStyleSheet(f"color: white;font-size: {int(font_size*1.4)}px;font-family: '{font_family_1}'")
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

"""
def reset_reporte():
    seleccionar_reportes = {"ubicacion":None,
                        "anios":None,
                        "filial":None,
                        "meses":None,
                        "tipo":None,
                        "clasificacion":None,
                        "fecha_personalizada":None}
    return seleccionar_reportes
"""


"""
regenerar=False, codigo_DANE=False, valor_facturado=False, cantidad_filas=False, mostrar_archivos=False, inventario=False,
                    calcular_tiempo=True, reportes_mensuales=False, texto_regenerar = "_form_estandar, _resumen", texto_regenerar_mensuales="",
                    usuarios_activos=False, sumatoria=False, reporte_consumo_anual=False, facturas=False
"""
