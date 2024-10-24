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
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos,ruta_fuentes,ruta_imagenes,fuente_texto,azul_vanti,dic_colores
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
dic_colores = mod_1.leer_archivos_json(ruta_constantes+"colores.json")["datos"]
azul_vanti = dic_colores["azul_v"]

def ubicacion_imagen(nueva_imagen, espacio):
    ancho, alto = nueva_imagen.size
    tamanio = (abs(espacio[0][0]-espacio[1][0]),abs(espacio[0][1]-espacio[3][1]))
    if alto > tamanio[1]:
        escalar = tamanio[1]/alto
    else:
        escalar = alto/tamanio[1]
    if int(ancho*escalar) <= tamanio[0]:
        nueva_imagen = nueva_imagen.resize((int(ancho*escalar), tamanio[1]))
    else:
        nueva_imagen = nueva_imagen.resize((tamanio[0],int(alto*escalar)))
    ancho, alto = nueva_imagen.size
    posicion = (espacio[0][0]+(abs(espacio[1][0]-espacio[0][0]-ancho)//2),abs(espacio[0][1]))
    return nueva_imagen,posicion

def slide_portada(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha, lista_metricas_portada):
    plantilla = ruta_imagenes+"plantilla_portada.png"
    imagen = Image.open(plantilla)
    dibujo = ImageDraw.Draw(imagen)
    ancho, alto = imagen.size
    fuente = ImageFont.truetype(ruta_fuente_negrilla, 60)
    bbox = dibujo.textbbox((0, 0), fecha, font=fuente)
    tamanio_texto_fecha = (bbox[2] - bbox[0], bbox[3] - bbox[1]) 
    dibujo.text((ancho-10-tamanio_texto_fecha[0],12), fecha, fill=azul_vanti, font=fuente)
    #442,1018
    dibujo.text((442,1018), f"Última actualización: {fecha_actual}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))

    #370,150
    texto = f"Total ventas m³\n{grupo_vanti}\n({fecha})"
    dibujo.text((370,150), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 22))
    #920,150
    texto = f"Cantidad de usuarios\nnuevos {grupo_vanti}\n({fecha})"
    dibujo.text((920,150), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 22))
    #1475,150
    texto = f"Cantidad de Eventos\nNo Controlados\n({fecha})"
    dibujo.text((1482,150), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 22))
    #920,690
    texto = f"Tiempo promedio de\nrespuesta a\nemergencias para\neventos No Controlados\n({fecha})"
    dibujo.text((920,690), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 22))
    #1475,690
    texto = f"Usuarios afectados\ncon las suspenciones\nde servicio\n({fecha})"
    dibujo.text((1482,690), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 22))
    #1475,385
    texto = f"Suspensiones\nrealizadas No\nEximentes de\nresponsabilidad\n({fecha})"
    dibujo.text((1482,385), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 22))

    ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
    esp = [(220,370),(630,370),(630,630),(220,630)]
    nueva_imagen = ubi_imagen+"porcentaje_cumplimientos_regulatorios_grupo_vanti.png"
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    esp = [(220,675),(630,675),(630,940),(220,940)]
    nueva_imagen = ubi_imagen+"porcentaje_matriz_requerimientos.png"
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
    esp = [(750,370),(1170,370),(1170,630),(750,630)]
    nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_grupo_vanti_pie_consumo_m3.png"
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    for i in range(len(lista_metricas_portada)):
        elemento = str(lista_metricas_portada[i])
        if elemento:
            if i == 0:
                dibujo.text((370,265), elemento, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            elif i == 1:
                dibujo.text((920,265), elemento, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            elif i == 2:
                dibujo.text((1482,565), elemento, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            elif i == 3:
                dibujo.text((1482,862), elemento, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            elif i == 4:
                dibujo.text((1482,265), elemento, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            elif i == 5:
                dibujo.text((920,862), elemento, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
    imagen.save(ubi+"slide_1.png")

def cargar_imagen(imagen, nombre_imagen, esp):
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
        imagen.save(nombre_imagen)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")

def slide_comercial(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha):
    ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
    esp = [(121,84),(1800,84),(1800,1012),(121,1012)]
    plantilla = ruta_imagenes+"plantilla_mag_com_1.png"
    imagen = Image.open(plantilla)
    dibujo = ImageDraw.Draw(imagen)
    ancho, alto = imagen.size
    #? Texto mes
    fuente = ImageFont.truetype(ruta_fuente_negrilla, 42)
    bbox = dibujo.textbbox((0, 0), fecha, font=fuente)
    tamanio_texto_fecha = (bbox[2] - bbox[0], bbox[3] - bbox[1]) 
    dibujo.text((ancho-10-tamanio_texto_fecha[0],16), fecha, fill=azul_vanti, font=fuente)
    #? Texto actualización
    dibujo.text((358,1030), f"Última actualización: {fecha_actual}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 20))
    nueva_imagen = ubi_imagen+texto_fecha+"_usuarios.png"
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    imagen.save(ubi+"slide_6.png")

    imagen = Image.open(plantilla)
    dibujo = ImageDraw.Draw(imagen)
    ancho, alto = imagen.size
    fuente = ImageFont.truetype(ruta_fuente_negrilla, 42)
    bbox = dibujo.textbbox((0, 0), fecha, font=fuente)
    tamanio_texto_fecha = (bbox[2] - bbox[0], bbox[3] - bbox[1]) 
    dibujo.text((ancho-10-tamanio_texto_fecha[0],16), fecha, fill=azul_vanti, font=fuente)
    dibujo.text((358,1030), f"Última actualización: {fecha_actual}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 20))
    nueva_imagen = ubi_imagen+texto_fecha+"_consumo.png"
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    imagen.save(ubi+"slide_7.png")

    plantilla = ruta_imagenes+"plantilla_mag_com_2.png"
    imagen = Image.open(plantilla)
    dibujo = ImageDraw.Draw(imagen)
    ancho, alto = imagen.size
    fuente = ImageFont.truetype(ruta_fuente_negrilla, 42)
    bbox = dibujo.textbbox((0, 0), fecha, font=fuente)
    tamanio_texto_fecha = (bbox[2] - bbox[0], bbox[3] - bbox[1]) 
    dibujo.text((ancho-10-tamanio_texto_fecha[0],16), fecha, fill=azul_vanti, font=fuente)
    dibujo.text((358,1030), f"Última actualización: {fecha_actual}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 20))
    esp = [(46,144),(916,144),(916,924),(46,924)]
    nueva_imagen = ubi_imagen+texto_fecha+"_pie_regulados.png"
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    esp = [(1010,144),(1878,144),(1878,924),(1010,924)]
    nueva_imagen = ubi_imagen+texto_fecha+"_pie_no_regulados.png"
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    imagen.save(ubi+"slide_8.png")
    """esp = [(121,82),(1800,82),(1800,1012),(121,1012)]
    plantilla = ruta_imagenes+"plantilla_mag_com_1.png"
    imagen = Image.open(plantilla)
    nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_tabla_consumo.png"
    nombre_slide = ubi+"slide_9.png"
    cargar_imagen(imagen, nueva_imagen, nombre_slide)
    imagen.save(ubi+"slide_9.png")"""

def slide_def_1(ubi,fecha,fecha_actual):
    lista_plantilla = ["equipo","def_1","def_2","def_3"]
    for i in range(len(lista_plantilla)):
        plantilla = ruta_imagenes+f"plantilla_{lista_plantilla[i]}.png"
        imagen = Image.open(plantilla)
        dibujo = ImageDraw.Draw(imagen)
        ancho, alto = imagen.size
        fuente = ImageFont.truetype(ruta_fuente_negrilla, 60)
        bbox = dibujo.textbbox((0, 0), fecha, font=fuente)
        tamanio_texto_fecha = (bbox[2] - bbox[0], bbox[3] - bbox[1]) 
        dibujo.text((ancho-10-tamanio_texto_fecha[0],12), fecha, fill=azul_vanti, font=fuente)
        dibujo.text((442,1018), f"Última actualización: {fecha_actual}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
        imagen.save(ubi+f"slide_{i+2}.png")

def crear_slides(ubi, fecha, fecha_completa, fecha_actual, texto_fecha, lista_metricas_portada):
    ubi_carpeta = ubi
    ubi += "\\04. Dashboard\\Imagenes\\"
    fecha = f"{fecha[1]}/{fecha[0]}"
    slide_portada(ubi, fecha, fecha_actual, ubi_carpeta, texto_fecha, lista_metricas_portada)
    slide_def_1(ubi, fecha, fecha_actual)
    slide_comercial(ubi, fecha, fecha_actual, ubi_carpeta, texto_fecha)

    ubi = ubi.replace("Imagenes\\", "Imagenes")
    print(f"\n\nEl Dashboard para el periodo: {fecha_completa} se ha creado en la carpeta {mod_1.acortar_nombre(ubi)}.\n")


# fecha
# 21

# texto actualización
# (358,1030)

# 1 cuadro
#esp = [(121,82),(1800,82),(1800,1012),(121,1012)]

# 2 cuadro
#esp = [(46,142),(916,142),(916,924),(46,924)]
#esp = [(1010,142),(1878,142),(1878,924),(1010,924)]

# 3 cuadro
#esp = [(121,82),(876,82),(876,526),(121,526)]
#esp = [(1036,82),(1800,82),(1800,526),(1036,526)]
#esp = [(121,565),(1800,565),(1800,1014),(121,1014)]

# 4 cuadro
#esp = [(121,82),(876,82),(876,526),(121,526)]
#esp = [(1036,82),(1800,82),(1800,526),(1036,526)]
#esp = [(121,566),(876,566),(876,1015),(121,1015)]
#esp = [(1036,566),(1800,566),(1800,1015),(1036,1015)]
