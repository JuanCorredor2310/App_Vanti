import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import Qt
import ruta_principal as mod_rp

global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos, ruta_fuentes, ruta_imagenes, fuente_texto, azul_vanti, dic_colores
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

def pantalla_inicio(titulo_espacios, app_vanti, titulo_1, titulo_2, button, image_button, screen_width, y=90):
    titulo_espacios.setText("INICIO")
    ajuatar_lugar(screen_width, titulo_espacios, y)
    mostrar_label(titulo_espacios)
    mostrar_label(image_button)
    esconder_label(app_vanti)
    esconder_label(titulo_1)
    esconder_label(titulo_2)
    esconder_label(button)

def create_main_window():
    #Configuración inicial
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = QWidget(window)
    central_widget.setStyleSheet("background-color: #030918;")
    window.setCentralWidget(central_widget)
    #Constantes pantalla
    screen = app.primaryScreen()
    screen_size = screen.size()
    screen_width = screen_size.width()
    screen_height = screen_size.height()
    logo_label = QLabel(central_widget)
    logo_label.setPixmap(QPixmap(ruta_imagenes+"vanti.png"))
    x = round((screen_width-(logo_label.sizeHint().width())*1.1))
    y = round((screen_height-(logo_label.sizeHint().height())*1.6))
    logo_label.move(x, y)
    #Creación labels
    app_vanti = QLabel("APP VANTI", central_widget)
    app_vanti.setStyleSheet("color: white;")
    font_id = QFontDatabase().addApplicationFont(ruta_fuente_negrilla)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    app_vanti.setFont(QFont(font_family, 80))
    x = round((screen_width-app_vanti.sizeHint().width())*0.5)
    app_vanti.move(x, 100)

    titulo_1 = QLabel("Vicepresidencia de Estrategia y Finanzas", central_widget)
    titulo_1.setStyleSheet("color: white;")
    font_id = QFontDatabase().addApplicationFont(ruta_fuente)
    font_family = QFontDatabase().applicationFontFamilies(font_id)[0]
    titulo_1.setFont(QFont(font_family,20))
    x = round((screen_width-titulo_1.sizeHint().width())*0.5)
    titulo_1.move(x, 550)

    titulo_2 = QLabel("Dirección Regulación, Márgenes y Tarifas", central_widget)
    titulo_2.setStyleSheet("color: white;")
    titulo_2.setFont(QFont(font_family, 30))
    x = round((screen_width-titulo_2.sizeHint().width())*0.5)
    titulo_2.move(x, 380)

    titulo_espacios = QLabel("", central_widget)
    titulo_espacios.setStyleSheet("color: white;")
    titulo_espacios.setFont(QFont(font_family, 80))
    x = round((screen_width-titulo_espacios.sizeHint().width())*0.5)
    titulo_espacios.move(x, 40)
    esconder_label(titulo_espacios)

    image_button = QPushButton("", central_widget)  # Texto vacío, solo imagen
    pixmap = QPixmap(ruta_imagenes+"flecha.png")  # Cambia a la ruta de tu imagen
    icon = QIcon(pixmap)
    image_button.setIcon(icon)
    image_button.setIconSize(pixmap.size())  # Tamaño de la imagen
    image_button.move(20,20)
    esconder_label(image_button)
    image_button.clicked.connect(lambda: pantalla_inicial(titulo_espacios, app_vanti, titulo_1, titulo_2, button, image_button))

    button = QPushButton("INICIAR")
    button.setStyleSheet("""QPushButton {color: #030918;padding: 20px;font-size: 40px;border: 2px solid white;
                            border-radius: 15px;font-family: '{font_family}';background-color: #ffffff;}""")
    button.clicked.connect(lambda: pantalla_inicio(titulo_espacios, app_vanti, titulo_1, titulo_2, button, image_button, screen_width))
    x = round((screen_width-button.sizeHint().width())*0.5)
    button.move(x,800)
    button.setParent(central_widget)  # Añadir button al central_widget
    window.setCentralWidget(central_widget)
    window.setWindowTitle("App Vanti")
    window.setGeometry(100, 100, 300, 200)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0x03, 0x09, 0x18))
    window.setPalette(palette)
    window.setStyleSheet("""QWidget {background-color: #030918;}
                        QLabel {margin: 20px;}""")
    window.showMaximized()
    return app, window

app, window = create_main_window()
window.show()
sys.exit(app.exec_())

