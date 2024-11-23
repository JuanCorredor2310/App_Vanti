import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QPushButton, QScrollArea
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import Qt, QEventLoop, QSize
import ruta_principal as mod_rp
import json
import time

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

def crear_boton(texto, central_widget, font="normal", color=dic_colores["azul_v"], font_size=32, padding=20):
    boton = QPushButton(texto, central_widget)
    if font == "normal":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    elif font == "bold":
        font_id = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    boton.setStyleSheet(f"""QPushButton {{color: {color};padding: {padding}px;font-size: {font_size}px;
                            border: 0.5px solid white;border-radius: 15px;font-family: '{font_family}';background-color: #ffffff;}}""")
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
        elif evento == "edicion_archivos":
            estado = menu_edicion_archivos(app, window, central_widget, dimensiones)
        elif evento == "reportes_comerciales":
            estado = menu_reportes_comerciales(app, window, central_widget, dimensiones)
        else:
            estado = pantalla_inicio(app, window, central_widget, dimensiones)
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
        estado_anterior = "menu_config_inicial"
        if texto == "volver":
            estado = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "crear_carpetas":
            op = texto
            texto = "Creación de carpetas y constantes"
            estado = confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op, estado_anterior)
        elif texto == "agregar_anio":
            op = texto
            texto = "Agregar año actual"
            estado = confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op, estado_anterior)
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

def menu_edicion_archivos(app, window, central_widget, dimensiones):
    screen_width = dimensiones[0]
    estado = None

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
            estado = menu_inicial(app, window, central_widget, dimensiones)
        else:
            print(texto)
            estado = menu_inicial(app, window, central_widget, dimensiones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("convertir_archivos"))
    boton_2.clicked.connect(lambda:on_button_clicked("almacenar_archivos"))
    boton_3.clicked.connect(lambda:on_button_clicked("archivos_estandar"))
    boton_4.clicked.connect(lambda:on_button_clicked("archivos_resumen"))
    boton_5.clicked.connect(lambda:on_button_clicked("archivos_existentes"))
    boton_6.clicked.connect(lambda:on_button_clicked("reportes_existentes"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado

def menu_reportes_comerciales(app, window, central_widget, dimensiones):
    screen_width = dimensiones[0]
    estado = None

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
        esconder_label(boton_7)
        esconder_label(image_button_1)
        if texto == "volver":
            estado = menu_inicial(app, window, central_widget, dimensiones)
        elif texto == "reporte_comercial":
            estado = menu_reporte_comercial(app, window, central_widget, dimensiones)
        else:
            print(texto)
            estado = menu_inicial(app, window, central_widget, dimensiones)
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
    return estado

def menu_reporte_comercial(app, window, central_widget, dimensiones):
    screen_width = dimensiones[0]
    estado = None

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
        estado = texto
        event_loop.quit()
        esconder_label(titulo_espacios)
        esconder_label(image_button)
        esconder_label(boton_1)
        esconder_label(boton_2)
        esconder_label(image_button_1)
        if texto == "volver":
            estado = menu_reportes_comerciales(app, window, central_widget, dimensiones)
        else:
            botones = menu_seleccion(app, window, central_widget, dimensiones)
            print(botones)
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked("reporte_comercial_sector_consumo"))
    boton_2.clicked.connect(lambda:on_button_clicked("reporte_comercial_sector_consumo_subsidio"))
    image_button_1.clicked.connect(lambda: ventana_secundaria(central_widget,titulo,dic_texto))
    event_loop.exec_()
    return estado

def menu_seleccion(app, window, central_widget, dimensiones):
    screen_width = dimensiones[0]

    titulo = "Selección información"
    titulo_espacios = crear_label(titulo, central_widget, font="bold", font_size=65)
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 30)
    titulo_espacios.setParent(central_widget)
    mostrar_label(titulo_espacios)

    t_filial = crear_label("Filiales", central_widget, font="bold", font_size=65)
    t_filial.move(50, 150)
    t_filial.setParent(central_widget)
    mostrar_label(t_filial)

    f1 = crear_boton("", central_widget, font_size=60, padding=5)
    f1.setFixedSize(80,300)
    f1.move(50,200)
    f1.setParent(central_widget)
    mostrar_label(f1)

    t_f1 = crear_label("VANTI", central_widget, font="bold", font_size=40)
    t_f1.move(150, 200)
    t_f1.setParent(central_widget)
    mostrar_label(t_f1)

    f2 = crear_boton("", central_widget, font_size=60, padding=5)
    f2.setFixedSize(80,80)
    f2.move(50,300)
    f2.setParent(central_widget)
    mostrar_label(f2)

    t_f2 = crear_label("GNCB", central_widget, font="bold", font_size=40)
    t_f2.move(150, 300)
    t_f2.setParent(central_widget)
    mostrar_label(t_f2)

    f3 = crear_boton("", central_widget, font_size=60, padding=5)
    f3.setFixedSize(80,80)
    f3.move(50,400)
    f3.setParent(central_widget)
    mostrar_label(f3)

    t_f3 = crear_label("GNCR", central_widget, font="bold", font_size=40)
    t_f3.move(150, 400)
    t_f3.setParent(central_widget)
    mostrar_label(t_f3)

    f4 = crear_boton("", central_widget, font_size=60, padding=5)
    f4.setFixedSize(80,80)
    f4.move(50,500)
    f4.setParent(central_widget)
    mostrar_label(f4)

    t_f4 = crear_label("GOR", central_widget, font="bold", font_size=40)
    t_f4.move(150, 500)
    t_f4.setParent(central_widget)
    mostrar_label(t_f4)

    f5 = crear_boton("", central_widget, font_size=60, padding=5)
    f5.setFixedSize(80,80)
    f5.move(50,600)
    f5.setParent(central_widget)
    mostrar_label(f5)

    t_f5 = crear_label("Todas", central_widget, font="bold", font_size=40)
    t_f5.move(150, 600)
    t_f5.setParent(central_widget)
    mostrar_label(t_f5)

    boton_1 = crear_boton("Aceptar", central_widget)
    x = round((((screen_width*0.5)-boton_1.sizeHint().width())*0.5)+(screen_width*0.53))
    boton_1.move(x,1040)
    boton_1.setParent(central_widget)
    mostrar_label(boton_1)
    dic_botones_filiales = {"VANTI":[f1,False], "GNCB":[f2,False], "GNCR":[f3,False], "GOR":[f4,False], "Todas":[f5,False]}
    event_loop = QEventLoop()

    def cambiar_botones(boton):
        if boton.text() == "X":
            boton.setText("")
        elif boton.text() == "":
            boton.setText("X")
        boton.setParent(central_widget)
        mostrar_label(boton)

    def on_button_clicked(texto):
        if texto == "volver":
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
            estado = menu_reporte_comercial(app, window, central_widget, dimensiones)
    f1.clicked.connect(lambda: cambiar_botones(f1))
    f2.clicked.connect(lambda: cambiar_botones(f2))
    f3.clicked.connect(lambda: cambiar_botones(f3))
    f4.clicked.connect(lambda: cambiar_botones(f4))

    boton_1.clicked.connect(lambda:on_button_clicked("volver"))
    event_loop.exec_()
    #esconder_label(box)
    return True


def manejar_clic_boton(boton_actual, lista_botones):
    """
    Maneja el clic en los botones
    - Si se selecciona el último botón, selecciona todos
    - Actualiza el diccionario de botones seleccionados
    """
    global selected_buttons

    # Limpiar el diccionario de selección
    selected_buttons.clear()

    # Si el último botón (índice 4) está seleccionado, seleccionar todos
    if lista_botones[4].isChecked():
        for btn in lista_botones:
            btn.setChecked(True)

    # Actualizar el diccionario de botones seleccionados
    for btn in lista_botones:
        selected_buttons[btn.text()] = btn.isChecked()

    # Imprimir los botones seleccionados
    print("Botones seleccionados:", selected_buttons)


def confirmacion_seleccion(app, window, central_widget, dimensiones, texto, op, estado_anterior):
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
                estado = menu_config_inicial(app, window, central_widget, dimensiones)
            else:
                estado = menu_inicial(app, window, central_widget, dimensiones)
        else:
            estado = texto
    image_button.clicked.connect(lambda:on_button_clicked("volver"))
    boton_1.clicked.connect(lambda:on_button_clicked(op))
    event_loop.exec_()
    return estado

def ventana_secundaria(central_widget, titulo, dic_texto):
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