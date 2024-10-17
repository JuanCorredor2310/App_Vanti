import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import seaborn as sns
import pandas as pd
from pandas.plotting import table
import os
from PIL import Image,ImageDraw,ImageFont
from skimage.transform import resize

import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos,ruta_fuentes,ruta_imagenes,fuente_texto,azul_vanti
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
ruta_fuentes = mod_rp.v_fuentes()
ruta_imagenes = mod_rp.v_imagenes()
import modulo as mod_1
import archivo_creacion_json as mod_2
global ruta_fuente,grupo_vanti
grupo_vanti = "Grupo Vanti"
ruta_fuente = ruta_fuentes+"Muli.ttf"
ruta_fuente_negrilla = ruta_fuentes+"Muli-Bold.ttf"
fuente_texto = font_manager.FontProperties(fname=ruta_fuentes+"Muli.ttf")
azul_vanti = "#14314a"

def slide_portada(ubi,fecha):
    plantilla = ruta_imagenes+"plantilla_portada.png"
    imagen = Image.open(plantilla)
    dibujo = ImageDraw.Draw(imagen)
    ancho, alto = imagen.size
    print(f"Tamaño: {ancho},{alto}")
    #370,150
    texto = f"Total ventas m³\n{grupo_vanti}\n{fecha}"
    dibujo.text((370,150), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 25, index=1))
    #1588,12
    dibujo.text((1588,12), fecha, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 60, index=1))

    #442,1018
    imagen.save(ubi+"slide_1.png")


def crear_slides(ubi, fecha, fecha_completa, fecha_actual):
    ubi += "\\04. Dashboard\\Imagenes\\"
    fecha = f"{fecha[1]}/{fecha[0]}"
    slide_portada(ubi, fecha, fecha_actual)
    print(f"\n\nEl Dashboard para el periodo: {fecha_completa} se ha creado en la carpeta {mod_1.acortar_nombre(ubi)}.\n")