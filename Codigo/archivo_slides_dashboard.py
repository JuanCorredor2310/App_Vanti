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
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos,ruta_fuentes,ruta_imagenes,fuente_texto,azul_vanti,dic_colores,meta_kpi_sub
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
meta_kpi_sub = "1,4"

def conversion_decimales(texto):
    return str(texto).replace(".",",")

def conversion_miles(num):
    try:
        valor = int(num)
        if valor >= 1000:
            return f"{(valor/1e3):.3f}"
        else:
            return str(valor)
    except BaseException:
        return num

def ubicacion_imagen(nueva_imagen, espacio):
    ancho, alto = nueva_imagen.size
    tamanio = (abs(espacio[0][0]-espacio[1][0]),abs(espacio[0][1]-espacio[3][1]))
    if alto > tamanio[1]:
        escalar = tamanio[1]/alto
    else:
        escalar = alto/tamanio[1]
    if int(ancho*escalar) > tamanio[0]:
        nueva_imagen = nueva_imagen.resize((tamanio[0],int(alto*escalar)))
    else:
        nueva_imagen = nueva_imagen.resize((int(ancho*escalar), tamanio[1]))
    ancho, alto = nueva_imagen.size
    posicion = (espacio[0][0]+(abs(espacio[1][0]-espacio[0][0]-ancho)//2),abs(espacio[0][1]))
    return nueva_imagen,posicion

def slide_portada(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p1.png"
        imagen = Image.open(plantilla)
        dibujo = ImageDraw.Draw(imagen)
        dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
        dibujo.text((360,230), conversion_decimales(dic_metricas["total_ventas"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((920,230), str(dic_metricas["nuevos_usuarios"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1500,260), str(dic_metricas["cantidad_emergencias"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1500,560), str(dic_metricas["tiempo_emergencias"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1380,790), str(dic_metricas["usuarios_eventos"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1440,890), str(dic_metricas["cantidad_eventos"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((850,790), str(dic_metricas["usuarios_compensados"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((810,890), "$ "+str(dic_metricas["valor_compensado"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))

        ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
        esp = [(170,440),(620,440),(620,670),(170,670)]
        nueva_imagen = ubi_imagen+"porcentaje_cumplimientos_regulatorios_grupo_vanti.png"
        if  os.path.exists(nueva_imagen):
            nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
            nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
            imagen.paste(nueva_imagen, pos, nueva_imagen)
        else:
            print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
        esp = [(170,770),(620,770),(620,995),(170,995)]
        nueva_imagen = ubi_imagen+"porcentaje_matriz_requerimientos.png"
        if  os.path.exists(nueva_imagen):
            nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
            nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
            imagen.paste(nueva_imagen, pos, nueva_imagen)
        else:
            print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
        ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
        esp = [(730,440),(1180,440),(1180,670),(730,670)]
        nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_grupo_vanti_pie_consumo_m3.png"
        if  os.path.exists(nueva_imagen):
            nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
            nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
            imagen.paste(nueva_imagen, pos, nueva_imagen)
        else:
            print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
        imagen.save(ubi+f"slide_{c_slide}.png")
        c_slide += 1
        return c_slide
    except BaseException:
        pass

def cargar_imagen(imagen, nombre_imagen, esp):
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
        imagen.save(nombre_imagen)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")

def slide_def_1(ubi,fecha,fecha_actual, dic_metricas,mes_corte,fecha_anio_anterior,c_slide):
    try:
        lista_plantilla = ["p2","p3","p4","p5","p6"]
        for i in lista_plantilla:
            plantilla = ruta_imagenes+f"{i}.png"
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            color = azul_vanti
            if i == "p2":
                color = "white"
            if i == "p6":
                dibujo.text((1440,525), str(dic_metricas["usuarios"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente_negrilla, 60))
                dibujo.text((1522,990), "* Cifras a "+mes_corte, fill=dic_colores["azul_v"], font=ImageFont.truetype(ruta_fuente, 20))
                dibujo.text((760,1025), f"Último corte: {fecha_anio_anterior}", fill=color, font=ImageFont.truetype(ruta_fuente, 30))
            else:
                dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=color, font=ImageFont.truetype(ruta_fuente, 30))
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def slide_usuarios(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p7.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill="white", font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((1480,240), str(dic_metricas["nuevos_usuarios"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1480,450), str(dic_metricas["porcentaje_crecimiento"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1480,660), str(dic_metricas["usuarios_regulados"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1480,870), str(dic_metricas["usuarios_no_regulados"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(22,320),(1230,320),(1230,900),(22,900)]
            nueva_imagen = ubi_imagen+texto_fecha+"_usuarios.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def slide_pie_usuarios(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p8.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((395,920), str(dic_metricas["usarios_residenciales"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1370,920), str(dic_metricas["usarios_no_residenciales"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(120,190),(900,190),(900,820),(120,820)]
            nueva_imagen = ubi_imagen+texto_fecha+"_pie_regulados.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
            esp = [(990,190),(1890,190),(1890,820),(990,820)]
            nueva_imagen = ubi_imagen+texto_fecha+"_pie_no_regulados.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide +=1
        return c_slide
    except BaseException:
        pass

def dibujar_texto_derecha(posicion_final, texto, fill, font, dibujo):
    bbox = dibujo.textbbox((0, 0), texto, font=font)
    ancho_texto = bbox[2] - bbox[0]
    x_inicial = posicion_final[0] - ancho_texto
    y_inicial = posicion_final[1]
    dibujo.text((x_inicial, y_inicial), texto, fill=fill, font=font)

def slide_consumo(ubi,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p9.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujar_texto_derecha((1815,200), str(dic_metricas["Demanda"]["Regulados"]["Residencial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,287), str(dic_metricas["Demanda"]["Regulados"]["Comercial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,375), str(dic_metricas["Demanda"]["Regulados"]["Industrial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,498), str(dic_metricas["Demanda"]["No regulados"]["Industrial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,587), str(dic_metricas["Demanda"]["No regulados"]["GNCV"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,669), str(dic_metricas["Demanda"]["No regulados"]["Comercial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,750), str(dic_metricas["Demanda"]["No regulados"]["Comercializadoras /\nTransportadores"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,838), str(dic_metricas["Demanda"]["No regulados"]["Termoeléctrico"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(25,270),(1330,270),(1330,920),(25,920)]
            nueva_imagen = ubi_imagen+texto_fecha+"_consumo.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def pegar_imagen(nueva_imagen, imagen, esp):
    if os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
        nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos, nueva_imagen)
    else:
        print(f"No existe la imagen ...{mod_1.acortar_nombre(nueva_imagen)}")
    return imagen

def slide_pie_consumo(ubi, fecha_actual, ubi_carpeta, texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p10.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((850,520), str(dic_metricas["consumo_mes"])+" M", fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(120,90),(725,90),(725,520),(120,520)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_VANTI_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = [(120,590),(725,590),(725,1020),(120,1020)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_GNCR_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = [(1150,90),(1720,90),(1720,520),(1150,520)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_GNCB_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = [(1150,590),(1720,590),(1720,1020),(1150,1020)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_GOR_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def slide_sub_con(ubi, fecha_actual, ubi_carpeta, texto_fecha, c_slide):
    try:
        plantilla = ruta_imagenes+"p11.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            texto = "El valor de las contribuciones para los Transportadores de gas natural en VANTI S.A. ESP. (Diciembre/2023) fue de 50.2 m M"
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            if "2024" in fecha_actual:
                dibujo.text((75,960), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 20))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(22,150),(1895,150),(1895,895),(22,895)]
            nueva_imagen = ubi_imagen+texto_fecha+"_subsidios_estratos.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def ajustar_coordenadas(coor):
    lista = [(coor[0][0],coor[0][1]),(coor[1][0],coor[0][1]),(coor[1][0],coor[1][1]),(coor[0][0],coor[1][1])]
    return lista

def slide_kpi_sub(ubi, fecha_actual, ubi_carpeta, dic_metricas, c_slide, anio):
    try:
        plantilla = ruta_imagenes+"p12.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((215,295), f"Meta {anio}", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((200,332), grupo_vanti, fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((165,535), "Comportamiento", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((265,575), "MME", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((152,778), "Dueda MME - TAM", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((255,383), str(meta_kpi_sub), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 55))
            dibujo.text((212,630), str(dic_metricas["kpi_subsidios"][0]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 55))
            dibujo.text((182,824), str(dic_metricas["deuda_subsidios"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 55))
            dibujo.ellipse((335,638,400,708), fill=dic_metricas["kpi_subsidios"][1])
            ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
            esp = ajustar_coordenadas([(525,190),(1900,990)])
            nueva_imagen = ubi_imagen+"KPI_subsidios.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def slide_recla_fact(ubi, fecha_actual, ubi_carpeta, c_slide):
    try:
        plantilla = ruta_imagenes+"p13.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
            esp = ajustar_coordenadas([(35,110),(1010,550)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_VANTI.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = ajustar_coordenadas([(985,110),(1860,550)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_GNCB.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = ajustar_coordenadas([(35,625),(1010,1015)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_GNCR.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = ajustar_coordenadas([(985,625),(1860,1015)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_GOR.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def slide_compensaciones(ubi, fecha_actual, ubi_carpeta, c_slide, texto_fecha):
    try:
        plantilla = ruta_imagenes+"p14.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill="white", font=ImageFont.truetype(ruta_fuente, 30))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = ajustar_coordenadas([(32,150),(1885,950)])
            nueva_imagen = ubi_imagen+texto_fecha+"_compilado_compensacion.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        pass

def crear_slides(ubi, fecha, fecha_completa, fecha_corte, texto_fecha, dic_metricas,mes_corte, fecha_anio_anterior):
    ubi_carpeta = ubi
    ubi += "\\04. Dashboard\\Imagenes\\"
    anio = fecha[0]
    fecha = f"{fecha[1]}/{fecha[0]}"
    c_slide = 1
    c_slide = slide_portada(ubi, fecha, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_def_1(ubi, fecha, fecha_corte, dic_metricas,mes_corte,fecha_anio_anterior, c_slide)
    c_slide = slide_usuarios(ubi, fecha, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_pie_usuarios(ubi, fecha, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_consumo(ubi, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_pie_consumo(ubi, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_sub_con(ubi, fecha_corte, ubi_carpeta, texto_fecha, c_slide)
    c_slide = slide_kpi_sub(ubi, fecha_corte, ubi_carpeta, dic_metricas, c_slide, anio)
    c_slide = slide_recla_fact(ubi, fecha_corte, ubi_carpeta, c_slide)
    c_slide = slide_compensaciones(ubi, fecha_corte, ubi_carpeta, c_slide, texto_fecha)
    ubi = ubi.replace("Imagenes\\", "Imagenes")
    print(f"\n\nEl Dashboard para el periodo: {fecha_completa} se ha creado en la carpeta {mod_1.acortar_nombre(ubi)}\n")
    os.startfile(ubi)