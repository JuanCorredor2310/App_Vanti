import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QDialog, QPushButton, QScrollArea
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import Qt, QEventLoop, QSize
import ruta_principal as mod_rp
import json

global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos, ruta_fuentes, ruta_imagenes, fuente_texto, azul_vanti, dic_colores, nombre_aplicativo
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

def crear_label(texto, central_widget, font="normal", color="white", font_size=30, background_color="#030918"):
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

def crear_boton(texto, central_widget, font="normal", color=dic_colores["azul_v"], font_size=32):
    boton = QPushButton(texto, central_widget)
    if font == "normal":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    elif font == "bold":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    boton.setStyleSheet(f"""QPushButton {{color: {color};padding: 20px;font-size: {font_size}px;
                            border: 2px solid white;border-radius: 15px;font-family: '{font_family}';background-color: #ffffff;}}""")
    return boton

def crear_label_imagen(ruta, central_widget):
    logo_label = QLabel(central_widget)
    logo_label.setPixmap(QPixmap(ruta))
    return logo_label

def mostrar_label(label):
    label.show()

def esconder_label(label):
    label.hide()

def pantalla_inicial(titulo_espacios, app_vanti, titulo_1, titulo_2, button, image_button):
    esconder_label(titulo_espacios)
    esconder_label(image_button)
    mostrar_label(app_vanti)
    mostrar_label(titulo_1)
    mostrar_label(titulo_2)
    mostrar_label(button)

def ajuatar_lugar(screen_width, label, y=40):
    x = round((screen_width-label.sizeHint().width())*0.5)
    label.move(x, y)

def pantalla_inicio_1(titulo_espacios, app_vanti, titulo_1, titulo_2, button, image_button, screen_width, y=90):
    titulo_espacios.setText("INICIO")
    ajuatar_lugar(screen_width, titulo_espacios, y)
    mostrar_label(titulo_espacios)
    mostrar_label(image_button)
    esconder_label(app_vanti)
    esconder_label(titulo_1)
    esconder_label(titulo_2)
    esconder_label(button)

def crear_pantalla_incial(mostrar=True):
    #Configuración inicial
    app = QApplication([])
    app.setWindowIcon(QIcon(ruta_imagenes+"vanti_logo.ico"))
    window = QMainWindow()
    window.setWindowIcon(QIcon(ruta_imagenes+"vanti_logo.ico"))
    central_widget = QWidget(window)
    central_widget.setStyleSheet("background-color: #030918;")
    window.setCentralWidget(central_widget)
    #Constantes pantalla
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
    if mostrar:
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

    button = QPushButton("INICIAR")
    button.setStyleSheet("""QPushButton {color: #030918;padding: 20px;font-size: 40px;border: 2px solid white;
                            border-radius: 15px;font-family: '{font_family}';background-color: #ffffff;}""")
    x = round((screen_width-button.sizeHint().width())*0.5)
    button.move(x,800)
    button.setParent(central_widget)
    mostrar_label(button)

    estado = None
    event_loop = QEventLoop()
    # Manejador del botón
    def on_button_clicked():
        nonlocal estado
        event_loop.quit()
        esconder_label(app_vanti)
        esconder_label(titulo_1)
        esconder_label(titulo_2)
        esconder_label(button)
        estado = menu_inicial(app, window, central_widget, dimensiones)
    button.clicked.connect(on_button_clicked)
    event_loop.exec_()
    # Esperar hasta que el botón sea oprimido
    return estado

def menu_inicial(app, window, central_widget, dimensiones):
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

    estado = None
    event_loop = QEventLoop()
    def on_button_clicked(evento):
        nonlocal estado
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
            estado = pantalla_inicio(app, window, central_widget, dimensiones)
        elif evento == "config_inicial":
            estado = menu_config_inicial(app, window, central_widget, dimensiones)
        else:
            estado = pantalla_inicio(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("config_inicial"))
    boton_2.clicked.connect(lambda:on_button_clicked(True))
    boton_3.clicked.connect(lambda:on_button_clicked(True))
    boton_4.clicked.connect(lambda:on_button_clicked(True))
    boton_5.clicked.connect(lambda:on_button_clicked(True))
    boton_6.clicked.connect(lambda:on_button_clicked(True))
    boton_7.clicked.connect(lambda:on_button_clicked(True))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado

def menu_config_inicial(app, window, central_widget, dimensiones):
    screen_width = dimensiones[0]
    estado = None

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
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(boton_3)
        esconder_label(boton_4)
        esconder_label(image_button_1)
        if texto == "volver":
            estado = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "crear_carpetas":
            op = texto
            texto = "Creación de carpetas y constantes"
            estado = confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op)
        else:
            print(texto)
            estado = menu_inicial(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("crear_carpetas"))
    boton_2.clicked.connect(lambda:on_button_clicked("agregar_anio"))
    boton_3.clicked.connect(lambda:on_button_clicked("editar_reporte"))
    boton_4.clicked.connect(lambda:on_button_clicked("agregar_reporte"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado

def confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op):
    estado = op
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

    texto_1 = crear_label("¿Desea continar con la seleción?", central_widget, font_size=30, color="#030918", background_color="white")
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
            estado = menu_config_inicial(app, window, central_widget, dimensiones)
        else:
            estado = texto
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked(op))
    event_loop.exec_()
    return estado

def ventana_secundaria(central_widget, titulo, dic_texto):
    ventana = QDialog(central_widget)
    ventana.setWindowTitle(titulo)
    ventana.setGeometry(central_widget.geometry().left(), central_widget.geometry().top(), int(central_widget.width()*0.82), int(central_widget.height()*0.82))
    ventana.setStyleSheet(f"""QWidget{{background-color: #030918; border: 5px solid #030918}}""")
    layout = QVBoxLayout()
    font_size = 24
    font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    font_id_1 = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family_1 = QFontDatabase().applicationFontFamilies(font_id_1)[0]
    for llave, valor in dic_texto.items():
        label = QLabel(llave, ventana)
        label.setStyleSheet(f"color: white;font-size: {int(font_size*1.8)}px;font-family: '{font_family_1}'")
        layout.addWidget(label)
        label_1 = QLabel(valor, ventana)
        label_1.setStyleSheet(f"color: white;font-size: {font_size}px;font-family: '{font_family}'")
        layout.addWidget(label_1)
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