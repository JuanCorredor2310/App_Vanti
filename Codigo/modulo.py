# ---------------------------------------------------------------------------------------------------------
# Python: 3.10.11 64-bit
# & Código Versión 1 - VANTI
import os
import sys
import time
import json
import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
sys.path.append(os.path.abspath(ruta_codigo))
import archivo_csv_a_excel as mod_5

# * -------------------------------------------------------------------------------------------------------
# *                                             Archivos json
# * -------------------------------------------------------------------------------------------------------
def almacenar_json(diccionario, nombre_archivo):
    with open(nombre_archivo, 'w') as file:
        json.dump(diccionario, file, indent=4)

def leer_archivos_json(archivo):
    with open(archivo) as file:
            data = json.load(file)
    return data

# * -------------------------------------------------------------------------------------------------------
# *                                             Constantes globales
# * -------------------------------------------------------------------------------------------------------

global lista_meses, lista_empresas, lista_anios, dic_reportes, lista_reportes_generales, reportes_generados, lista_reportes_totales,chunksize,llaves_dic_reporte, dic_carpetas, dic_filiales,antidad_datos_excel, dic_nit, cantidad_datos_estilo_excel,grupo_vanti,mercado_relevante,mercado_relevante_resumen,tabla_3
grupo_vanti = "Grupo Vanti"
dic_carpetas = leer_archivos_json(ruta_constantes+"carpetas.json")
lista_anios = list(leer_archivos_json(ruta_constantes+"anios.json")["datos"].values())
lista_meses = list(leer_archivos_json(ruta_constantes+"tabla_18.json")["datos"].values())
dic_filiales = leer_archivos_json(ruta_constantes+"tabla_empresa.json")["datos"]
dic_nit = leer_archivos_json(ruta_constantes+"tabla_nit.json")["datos"]
lista_filiales = list(dic_filiales.keys())
dic_reportes = dic_carpetas["carpeta_6"]
lista_reportes_generales = leer_archivos_json(ruta_constantes+"carpetas_extra.json")["carpeta_2"]
reportes_generados = leer_archivos_json(ruta_constantes+"carpetas_extra.json")["carpeta_4"]
mercado_relevante = leer_archivos_json(ruta_constantes+"mercado_relevante.json")
mercado_relevante_resumen = leer_archivos_json(ruta_constantes+"mercado_relevante_resumen.json")
chunksize = 60000
cantidad_datos_excel = chunksize
cantidad_datos_estilo_excel = 120000
llaves_dic_reporte = ["generales_no_float","generales_float","generales_fecha","generales_hora"]
tabla_3 = leer_archivos_json(ruta_constantes+"tabla_3.json")
def crear_lista_reportes_totales():
    dic = leer_archivos_json(ruta_constantes+"reportes_disponibles.json")["datos"]
    lista = []
    for i in dic:
        lista.extend(dic[i])
    return lista
lista_reportes_totales = crear_lista_reportes_totales()

# * Importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import chardet
import math
import csv
import dataframe_image as dfi
import pathlib
from datetime import datetime
from playwright.sync_api import sync_playwright
import googlemaps
import shutil


# * -------------------------------------------------------------------------------------------------------
# *                                             Uso de librería Geopy
# * -------------------------------------------------------------------------------------------------------
def encontrar_coordenadas(municipio):
    gmaps = googlemaps.Client(key="AIzaSyARSFO5ues9twiOidNkaH6ML3MCjfRLXtg")
    geocode_result = gmaps.geocode(municipio)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location
        #print(f"Latitud: {location['lat']}, Longitud: {location['lng']}")
    else:
        return None

# * -------------------------------------------------------------------------------------------------------
# *                                             Uso de años y meses
# * -------------------------------------------------------------------------------------------------------
def encontrar_anio(archivo):
    for anio in lista_anios:
        if str(anio) in archivo:
            return anio
    return None

def encontrar_mes(archivo):
    for mes in lista_meses:
        mes_1 = mes.upper()
        if mes_1 in archivo:
            return mes_1
    return None

def cambiar_formato_fecha(ruta):
    lista_ruta = ruta.split("\\")
    anio_archivo = encontrar_anio(lista_ruta[-1])
    mes_archivo = encontrar_mes(lista_ruta[-1])
    if anio_archivo and mes_archivo:
        index_mes = lista_meses.index(mes_archivo.lower().capitalize())-1
        if index_mes == -1:
            anio_archivo = str(int(anio_archivo)-1)
            mes_archivo = lista_meses[-1]
        return anio_archivo, lista_meses[index_mes]
    else:
        return None, None

# * -------------------------------------------------------------------------------------------------------
# *                                             Definir variables globales
# * -------------------------------------------------------------------------------------------------------
# ? Ubicación de imagen Vanti
global imagen_vanti
imagen_vanti = 'vanti.png'

# ? Medición de la información horaria actual
global fecha_actual
fecha_actual = datetime.now()

# * -------------------------------------------------------------------------------------------------------
# *                                             Lectura DataFrames
# * -------------------------------------------------------------------------------------------------------
"""
    función: leer_dataframe
    Función para lectura de archivo (csv) en un dataframe

    # ? @param archivo: Archivo a utilizar
"""
def leer_dataframe(archivo):
    encoding_1 = elegir_codificacion(archivo)
    df = pd.read_csv(archivo, encoding=encoding_1)
    return df

def leer_dataframe_utf_8(archivo):
    df = pd.read_csv(archivo, encoding="utf-8-sig")
    return df

def elegir_codificacion(archivo):
    with open(archivo, 'rb') as file:
        raw_data = file.read(400000)
        result = chardet.detect(raw_data)
        encoding_1 = result['encoding']
    return encoding_1

def lectura_dataframe_chunk(archivo, valor_chunksize=chunksize,separador=","):
    lista_codificaciones = []
    lista_codificaciones.append(elegir_codificacion(archivo))
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','utf-16','utf-16-be','utf-32','ascii','windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
                                    'shift-jis','euc-jp','mac_roman','utf-7','cp437','cp850','ibm866','tis-620'])
    for elemento in lista_codificaciones:
        try:
            lista_df = []
            for i, chunk in enumerate(pd.read_csv(archivo, chunksize=valor_chunksize, encoding=elemento, sep=separador,low_memory=False)):
                lista_df.append(chunk.reset_index(drop=True).copy())
            return lista_df
        except pd.errors.ParserError:
            pass
        except UnicodeDecodeError:
            pass
        except UnicodeError:
            pass
    return None

# * -------------------------------------------------------------------------------------------------------
# *                                             Información horaria
# * -------------------------------------------------------------------------------------------------------
"""
    función: determinar_mes_actual
    Función Determina el mes actual de fecha_actual

    # ? @param fecha_actual: Fecha actual en formato datetime
"""
def determinar_mes_actual(fecha_actual):
    mes = fecha_actual.month
    return lista_meses[:mes]

# * -------------------------------------------------------------------------------------------------------
# *                                             Tiempo de procesamiento
# * -------------------------------------------------------------------------------------------------------
def mostrar_tiempo(t_f, t_i):
    tiempo = t_f-t_i
    if tiempo > 60:
        minutos = round(tiempo//60)
        segundos = round(tiempo%60,4)
        if minutos == 1:
            print(f"\nTiempo de procesamiento: {minutos} minuto y {segundos} segundos")
        else:
            print(f"\nTiempo de procesamiento: {minutos} minutos y {segundos} segundos")
    else:
        print(f"\nTiempo de procesamiento: {tiempo:.4f} segundos")

# * -------------------------------------------------------------------------------------------------------
# *                                             Edición de textos
# * -------------------------------------------------------------------------------------------------------
"""
    función: lista_a_texto
    Función Función para convertir una lista a texto con un seperador seleccionado

    # ? @param lista: Lista a recibir
    # ? @param seperador: Seperador seleccionado
    # ? @param salto: Generar un salto de línea en el texto
"""
def lista_a_texto(lista, separador, salto):
    texto = separador.join(lista)
    if salto:
        texto += "\n"
    return texto

def cambio_separador_texto(texto):
    if texto.count(';') > 3:
        lista_texto = texto.split(";")
        largo = len(lista_texto)
        for i in range(largo):
            lista_texto[i] = lista_texto[i].replace(",",".")
        texto = lista_a_texto(lista_texto, ",", False)
    return texto

def cambio_caracteres_texto(texto):
    dic = {"Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U",
            "á":"a","é":"e","í":"i","ó":"o","ú":"u",
            "Ñ":"N","ñ":"n","<":" ",">":" "}
    ele = '[¿?!¡]()"\"#\\$%&\'´+*\{}…=€£¥÷×@^|~§©®™°•¶'
    for i in ele:
        texto = texto.replace(i,"")
    for i, j in dic.items():
        texto = texto.replace(i,j)
    return texto

# * -------------------------------------------------------------------------------------------------------
# *                                             Creación de carpetas
# * -------------------------------------------------------------------------------------------------------
"""
    función: buscar_carpetas
    Función para encontrar las carpetas en una ubicación específica

    # ? @param ruta: Ubicación seleccionada
"""
def buscar_carpetas(ruta):
    carpetas = []
    for elemento in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, elemento)
        if os.path.isdir(ruta_completa):
            carpetas.append(ruta_completa)
    return carpetas

def buscar_carpetas_lista_carpetas(lista_carpetas):
    lista_final = []
    for elemento in lista_carpetas:
        lista_final.extend(list(buscar_carpetas(elemento)))
    return lista_final

"""
    función: ciclo_creacion_carpetas
    Función Creación de carpetas (almacenadas en carpeta) en ubicación

    # ? @param ubicacion: Ubicación seleccionada
    # ? @param carpeta: Carpetas a guardar
"""
def ciclo_creacion_carpetas(ubicacion, carpeta):
    for i in range(len(carpeta)):
        numeros_c = listado_numeros_lista(carpeta)
        ubi = ubicacion+"/"+numeros_c[i]+carpeta[i]
        os.makedirs(ubi, exist_ok=True)

"""
    función: crear_carpeta
    Función para crear carpeta con el nombre de elemento

    # ? @param elemento: Creación de una carpeta con el nombre de elemento
"""
def crear_carpeta(elemento):
    os.makedirs(elemento, exist_ok=True)

"""
    función: creación_carpeta
    Función Creación de carpetas almacenadas en lista

    # ? @param lista: Lista de carpetas
"""
def creacion_carpeta(lista):
    for elemento in lista:
        crear_carpeta(elemento)

def filtrar_carpetas(lista_carpetas, filtro):
    lista = []
    for elemento in filtro:
        for carpeta in lista_carpetas:
            if elemento in carpeta:
                lista.append(carpeta)
    return lista

def filtrar_carpetas_mes_anio(lista_carpetas, filtro):
    lista = []
    for elemento in filtro:
        for carpeta in lista_carpetas:
            if elemento[0] in carpeta and elemento[1] in carpeta:
                lista.append(carpeta)
    return lista


# * -------------------------------------------------------------------------------------------------------
# *                                             Edición de archivos
# * -------------------------------------------------------------------------------------------------------
def lectura_archivo_readline(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo_txt:
            lineas = archivo_txt.readlines()
            archivo_txt.close()
    except UnicodeDecodeError:
        try:
            archivo_txt.close()
            with open(ruta, 'r', encoding='utf-8-sig') as archivo_txt:
                lineas = archivo_txt.readlines()
                archivo_txt.close()
        except UnicodeDecodeError:
            try:
                archivo_txt.close()
                with open(ruta, 'r', encoding='iso-8859-1') as archivo_txt:
                    lineas = archivo_txt.readlines()
                    archivo_txt.close()
            except UnicodeDecodeError:
                try:
                    archivo_txt.close()
                    with open(ruta, 'r', encoding='utf-16') as archivo_txt:
                        lineas = archivo_txt.readlines()
                        archivo_txt.close()
                except UnicodeDecodeError:
                    try:
                        archivo_txt.close()
                        with open(ruta, 'r', encoding='utf-32') as archivo_txt:
                            lineas = archivo_txt.readlines()
                            archivo_txt.close()
                    except UnicodeDecodeError:
                        try:
                            archivo_txt.close()
                            encoding_1 = elegir_codificacion(ruta)
                            with open(ruta, 'r', encoding=encoding_1) as archivo_txt:
                                lineas = archivo_txt.readlines()
                                archivo_txt.close()
                        except UnicodeDecodeError:
                            lineas = []
    return lineas

def encontrar_codificacion(archivo):
    lista_codificaciones = []
    lista_codificaciones.append(elegir_codificacion(archivo))
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','utf-16','utf-16-be','utf-32','ascii','windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
                                    'shift-jis','euc-jp','mac_roman','utf-7','cp437','cp850','ibm866','tis-620'])
    for elemento in lista_codificaciones:
        try:
            with open(archivo, 'r', encoding=elemento) as file:
                sample = file.read(10000)
                dialect = csv.Sniffer().sniff(sample)
                return dialect
        except UnicodeDecodeError:
            pass
        except UnicodeError:
            pass
    return None

def cambio_archivo(ruta, ext_original, ext_final):
    dialect = encontrar_codificacion(ruta)
    if dialect:
        lista_df = lectura_dataframe_chunk(ruta, separador=dialect.delimiter)
        if lista_df:
            df = pd.concat(lista_df, ignore_index=True)
            df.to_csv(ruta.replace(ext_original,ext_final), index=False, sep=',', encoding="utf-8-sig")
            return ruta.replace(ext_original,ext_final)
        return None
    else:
        return None

"""
    función: eliminar_archivos
    Función lista

    # ? @param lista: Lista de archivos a eliminar
"""
def eliminar_archivos(lista):
    for elemento in lista:
        if os.path.exists(elemento):
            os.remove(elemento)

def buscar_archivos_no_repetidos(archivo):
    lista_archivo = archivo.split("\\")
    if "_form_estandar" not in lista_archivo[-1] and "_resumen" not in lista_archivo[-1]:
        return True
    else:
        return False

def buscar_formato(archivo):
    lista_archivo = archivo.split("\\")
    if "_form_estandar" in lista_archivo[-1]:
        return True
    else:
        return False

"""
    función: conversion_archivos
    Función para la conversión de archivos en un nuevo formato

    # ? @param lista: Lista de archivos a convertir
    # ? @param ext_original: Extensión original
    # ? @param ext_final: Extensión nueva
    # ? @param separador: Separador seleccionado para el nuevo archivo
"""

def conversion_archivos_lista(lista_archivos, ext_original, ext_final, separador,informar=False):
    for archivo in lista_archivos:
        op = conversion_archivos(archivo, ext_original, ext_final, separador)
        if op and informar:
            informar_archivo_creado(archivo, informar)

def conversion_archivos(archivo, ext_original, ext_final, separador):
    if ext_original in archivo:
        archivo = cambio_archivo(archivo, ext_original, ext_final)
        return True
    return False

def cambiar_formato_dataframe(df, dic_reporte):
    df.columns = list(dic_reporte["generales"].keys())
    return df

def acortar_nombre(nombre):
    lista_nombre = nombre.split("\\")
    largo = len(lista_nombre)
    if largo > 6:
        texto = "...\\"+lista_a_texto(lista_nombre[largo-6:], "\\", False)
    return texto

def informar_archivo_creado(nombre,valor):
    texto = acortar_nombre(nombre)
    if valor:
        print(f"\nArchivo {texto} creado\n")

def estandarizacion_archivos(lista_archivos, informar):
    dic_reporte = None
    for archivo in lista_archivos:
        conversion_archivos(archivo, ".csv", ".csv", ",")
        dic_reporte = buscar_reporte(archivo)
        if dic_reporte:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:

                for i in range(len(lista_df)):
                    df = lista_df[i].copy()
                    if len(df.columns) == dic_reporte["cantidad_columnas"]:
                        df = cambiar_formato_dataframe(df, dic_reporte)
                        lista_df[i] = df
                df = pd.concat(lista_df, ignore_index=True)
                nuevo_nombre = archivo.replace(".csv", "_form_estandar.csv")
                df.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(nuevo_nombre, informar)

def cambiar_formato_dataframe_resumen(df, dic_reporte):
    df = df[dic_reporte["seleccionados"]]
    return df

def buscar_reporte(archivo):
    lista_archivo = archivo.split("\\")
    for reporte in lista_reportes_totales:
        if reporte in lista_archivo[-1]:
            dic_reporte = leer_archivos_json(ruta_constantes+f"/{reporte.upper()}.json")
            return dic_reporte
    return None

def archivos_resumen(lista_archivos, informar):
    dic_reporte = None
    for archivo in lista_archivos:
        if buscar_formato(archivo):
            dic_reporte = buscar_reporte(archivo)
            if dic_reporte:
                lista_df = lectura_dataframe_chunk(archivo)
                if lista_df:
                    for i in range(len(lista_df)):
                        df = lista_df[i].copy()
                        if len(df.columns) == dic_reporte["cantidad_columnas"]:
                            df = cambiar_formato_dataframe_resumen(df, dic_reporte)
                            anio_archivo, mes_archivo = cambiar_formato_fecha(archivo)
                            if anio_archivo and mes_archivo:
                                df["Anio_reportado"] = anio_archivo
                                df["Mes_reportado"] = mes_archivo
                            lista_df[i] = df
                    df = pd.concat(lista_df, ignore_index=True)
                    nuevo_nombre = archivo.replace("_form_estandar.csv", "_resumen.csv")
                    df.to_csv(nuevo_nombre, index=False,encoding="utf-8-sig")
                    if informar:
                        informar_archivo_creado(nuevo_nombre, True)

def encontrar_categoria_reporte(reporte):
    for categoria, lista in dic_reportes.items():
        for elemento in lista:
            if elemento == reporte:
                return categoria

def encontrar_nueva_ubi_archivo(ubi, ext_archivo):
    orden = [2, 1, 3, -1, 0]
    for i in orden:
        lista_carpetas = buscar_carpetas(ubi)
        elemento = ext_archivo[i]
        for carpeta in lista_carpetas:
            if elemento in carpeta:
                ubi = carpeta
        lista_carpetas.clear()
    return ubi


def almacenar_archivos(ruta, tipo, informar):
    try:
        lista_carpetas = buscar_carpetas(ruta_nuevo_sui)
        for i in lista_carpetas:
            if dic_carpetas["carpeta_2"][0] in i:
                ubi = i
        lista_archivos = busqueda_archivos_tipo(ruta+"\\*",tipo)
        for archivo in lista_archivos:
            nombre_archivo = archivo.split("\\")[-1]
            ext_archivo = nombre_archivo.split("_")
            ext_archivo[-1] = ext_archivo[-1].split(".")[0]
            categoria = encontrar_categoria_reporte(ext_archivo[0])
            ext_archivo[3] = ext_archivo[3].lower().capitalize()
            ext_archivo.append(categoria)
            if None not in ext_archivo:
                ubi_1 = encontrar_nueva_ubi_archivo(ubi, ext_archivo)
                nueva_ubi = ubi_1+"\\"+nombre_archivo
                shutil.move(archivo, nueva_ubi)
                if informar:
                    informar_archivo_creado(nueva_ubi, informar)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass

def conversion_archivos_CSV(lista_archivos):
    for archivo in lista_archivos:
        os.rename(archivo, archivo.replace(".CSV",".csv"))

def regenerar_archivos_necesarios(lista_archivos, evitar):
    lista_regenerar = []
    for i in range(len(lista_archivos)):
        if evitar == "_resumen":
            nombre = lista_archivos[i].replace(evitar,"_form_estandar")
        elif evitar == "_form_estandar":
            nombre = lista_archivos[i].replace(evitar,"")
        if os.path.exists(nombre):
            lista_regenerar.append(nombre)
    if evitar == "_resumen":
        archivos_resumen(lista_regenerar,True)
    elif evitar == "_form_estandar":
        estandarizacion_archivos(lista_regenerar,True)

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Comerciales
# * -------------------------------------------------------------------------------------------------------
def apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos, codigo_DANE, reporte, informar, valor_facturado,filial):
    tabla_11 = leer_archivos_json(ruta_constantes+"/tabla_11.json")
    for archivo in lista_archivos:
        if reporte in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                df2 = lista_df[0][["Anio_reportado","Mes_reportado"]].reset_index(drop=True)
                anio_reportado = df2["Anio_reportado"][0]
                mes_reportado = df2["Mes_reportado"][0]
                dic_dataframe = {}
                for i in range(len(lista_df)):
                    df = lista_df[i].copy()
                    if codigo_DANE:
                        df = df[df["Codigo_DANE"] == codigo_DANE]
                    lista_sectores = list(df["Sector_consumo"].unique())
                    for sector in lista_sectores:
                        try:
                            s1 = int(sector)
                            df_sector = df[df["Sector_consumo"] == s1]
                            if s1 not in dic_dataframe:
                                dic_dataframe[s1] = [0,0,0]
                            cantidad_usuarios = len(list(df_sector["ID_Factura"].unique()))
                            volumen = df_sector["Volumen"].sum()
                            valor_total = df_sector["Valor_total_facturado"].sum()
                            dic_dataframe[s1][0] += cantidad_usuarios
                            dic_dataframe[s1][1] += volumen
                            dic_dataframe[s1][2] += valor_total
                        except ValueError:
                            pass
                        except TypeError:
                            pass
                dic_dataframe = dict(sorted(dic_dataframe.items()))
                dic_dataframe_2 = {"Tipo de usuario":[],
                                    "Sector de consumo":[],
                                    "Cantidad de usuarios":[],
                                    "Consumo m3":[]}
                if codigo_DANE:
                    dic_dataframe_2["Codigo DANE"] = []
                if valor_facturado:
                    dic_dataframe_2["Valor total facturado"] = []
                for llave, valor in dic_dataframe.items():
                    try:
                        valor_1 = tabla_11["datos"][str(llave)]
                        dic_dataframe_2["Tipo de usuario"].append("No regulados")
                        dic_dataframe_2["Sector de consumo"].append(valor_1)
                        dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                        dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                        if codigo_DANE:
                            dic_dataframe_2["Codigo DANE"].append(codigo_DANE)
                        if valor_facturado:
                            dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                    except KeyError:
                        pass
                df1 = pd.DataFrame(dic_dataframe_2)
                df1["Filial"] = dic_filiales[filial]
                df1["NIT"] = dic_nit[dic_filiales[filial]]
                df1["Anio reportado"] = anio_reportado
                df1["Mes reportado"] = mes_reportado
                lista_nombre = archivo.split("\\")
                if codigo_DANE:
                    lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_consumo_{str(codigo_DANE)}.csv")
                else:
                    lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo.csv")
                nombre = lista_a_texto(lista_nombre, "\\", False)
                if len(df1) > 0:
                    lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3"]
                    if valor_facturado:
                        lista_columnas.append("Valor total facturado")
                    if codigo_DANE:
                        lista_columnas.append("Codigo DANE")
                    df1 = df1[lista_columnas]
                    df1.to_csv(nombre, index=False, encoding="utf-8-sig")
                    if informar:
                        informar_archivo_creado(nombre, True)
                    return nombre
                else:
                    return None
            else:
                return None
    else:
        return None

def buscar_NIU(lista_NIU, dic_NIU, subsidio=False, rango=20):
    dic_2 = dic_NIU.copy()
    cantidad_usuario = 0
    volumen = 0
    valor_total_facturado = 0
    for elemento in lista_NIU:
        try:
            valor = dic_2[elemento]
            if subsidio:
                if valor[0] > 0:
                    cantidad_usuario += 1
                if valor[0] > rango:
                    volumen += rango
                elif valor[0] <= rango:
                    volumen += valor[0]
                valor_total_facturado += valor[1]
                del dic_2[elemento]
            else:
                volumen += valor[0]
                valor_total_facturado += valor[1]
                cantidad_usuario += 1
        except KeyError:
            pass
    return cantidad_usuario, volumen, valor_total_facturado, dic_2

def busqueda_sector_GRTT2(lista_archivos, dic_NIU, codigo_DANE, reporte, valor_facturado, filial, subsidio=False,rango=20):
    for archivo in lista_archivos:
        if reporte in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                df2 = lista_df[0][["Anio_reportado","Mes_reportado"]].reset_index(drop=True)
                anio_reportado = df2["Anio_reportado"][0]
                mes_reportado = df2["Mes_reportado"][0]
                dic_dataframe = {}
                lista_NIU_codigo_DANE = []
                for i in range(len(lista_df)):
                    df = lista_df[i].copy()
                    if codigo_DANE:
                        df = df[df["Codigo_DANE"] == codigo_DANE]
                    lista_NIU_codigo_DANE.extend(list(df["NIU"]))
                    lista_sectores = list(df["Estrato"].unique())
                    for sector in lista_sectores:
                        if subsidio:
                            if str(sector) in ["1","2"]:
                                try:
                                    s1 = int(sector)
                                    df_sector = df[df["Estrato"] == s1]
                                    lista_NIU_sector = list(df_sector["NIU"])
                                    if s1 not in dic_dataframe:
                                        dic_dataframe[s1] = [0,0,0]
                                    cantidad_usuario, volumen, valor_total_facturado, dic_NIU = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                    dic_dataframe[s1][0] += cantidad_usuario
                                    dic_dataframe[s1][1] += volumen
                                    dic_dataframe[s1][2] += valor_total_facturado
                                except TypeError:
                                    pass
                                except ValueError:
                                    pass
                        else:
                            try:
                                s1 = int(sector)
                                df_sector = df[df["Estrato"] == s1]
                                lista_NIU_sector = list(df_sector["NIU"])
                                if s1 not in dic_dataframe:
                                    dic_dataframe[s1] = [0,0,0]
                                cantidad_usuario, volumen, valor_total_facturado, dic_NIU = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                dic_dataframe[s1][0] += cantidad_usuario
                                dic_dataframe[s1][1] += volumen
                                dic_dataframe[s1][2] += valor_total_facturado
                            except TypeError:
                                pass
                            except ValueError:
                                pass
                dic_dataframe = dict(sorted(dic_dataframe.items()))
                dic_dataframe_2 = {"Tipo de usuario":[],
                                    "Sector de consumo":[],
                                    "Cantidad de usuarios":[],
                                    "Consumo m3":[]}
                if codigo_DANE:
                    dic_dataframe_2["Codigo DANE"] = []
                if valor_facturado:
                    dic_dataframe_2["Valor total facturado"] = []
                for llave, valor in dic_dataframe.items():
                    try:
                        valor_1 = tabla_3["datos"][str(llave)]
                        dic_dataframe_2["Tipo de usuario"].append("Regulados")
                        dic_dataframe_2["Sector de consumo"].append(valor_1)
                        dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                        dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                        if codigo_DANE:
                            dic_dataframe_2["Codigo DANE"].append(codigo_DANE)
                        if valor_facturado:
                            dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                    except KeyError:
                        pass
                lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3"]
                if valor_facturado:
                    lista_columnas.append("Valor total facturado")
                if codigo_DANE:
                    lista_columnas.append("Codigo DANE")
                df1 = pd.DataFrame(dic_dataframe_2)
                df1["Anio reportado"] = anio_reportado
                df1["Mes reportado"] = mes_reportado
                df1["Filial"] = dic_filiales[filial]
                df1["NIT"] = dic_nit[dic_filiales[filial]]
                df1 = df1[lista_columnas]
                return df1

def apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos, codigo_DANE, reporte, informar, valor_facturado,filial,subsidio=False):
    for archivo in lista_archivos:
        if reporte in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                dic_1 = {}
                for i in range(len(lista_df)):
                    df = lista_df[i].copy().reset_index()
                    for pos in range(len(df)):
                        elemento = df["NIU"][pos]
                        consumo = df["Consumo"][pos]
                        valor_total_facturado = df["Valor_total_facturado"][pos]
                        if elemento not in dic_1:
                            dic_1[elemento] = [0,0]
                        dic_1[elemento][0] += consumo
                        dic_1[elemento][1] += valor_total_facturado
                df1 = busqueda_sector_GRTT2(lista_archivos, dic_1, codigo_DANE, "GRTT2", valor_facturado, filial,subsidio)
                lista_nombre = archivo.split("\\")
                if codigo_DANE:
                    if subsidio:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_consumo_{str(codigo_DANE)}_subsidio.csv")
                    else:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_consumo_{str(codigo_DANE)}.csv")
                else:
                    if subsidio:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo_subsidio.csv")
                    else:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo.csv")
                nombre = lista_a_texto(lista_nombre, "\\", False)
                if len(df1) > 0:
                    df1.to_csv(nombre, index=False, encoding="utf-8-sig")
                    if informar:
                        informar_archivo_creado(nombre, True)
                    return nombre
                else:
                    return None
            else:
                return None
    else:
        return None

def reporte_comercial_sector_consumo(lista_archivos, codigo_DANE, informar, seleccionar_reporte, valor_facturado,subsidio=False, almacenar_excel=True):
    lista_df_filiales = []
    lista_df_filial = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        proceso = None
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            n2 = apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos_filial, codigo_DANE, "GRC2", informar, valor_facturado, filial)
            n1 = apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos_filial, codigo_DANE, "GRC1", informar, valor_facturado, filial, subsidio)
            if n1 and n2:
                df1 = leer_dataframe(n1)
                lista_n1 = n1.split("\\")
                nombre_1 = lista_n1[-1].split("_")
                nombre_1 = nombre_1[1:]
                lista_n1[-1] = lista_a_texto(nombre_1, "_", False)
                n1 = lista_a_texto(lista_n1, "\\", False)
                df2 = leer_dataframe(n2)
                lista_n2 = n2.split("\\")
                nombre_2 = lista_n2[-1].split("_")
                nombre_2 = nombre_2[1:]
                lista_n2[-1] = lista_a_texto(nombre_2, "_", False)
                n2 = lista_a_texto(lista_n2, "\\", False)
                df3 = pd.concat([df1, df2])
                df3.to_csv(n1, index=False, encoding="utf-8-sig")
                df3.to_csv(n2, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(n1, True)
                df3 = leer_dataframe_utf_8(n1)
                n3 = n1.replace(".csv",".xlsx")
                almacenar = mod_5.almacenar_csv_en_excel(df3, n3,"Datos")
                if informar and almacenar:
                    informar_archivo_creado(n3, True)
                n3 = n2.replace(".csv",".xlsx")
                mod_5.almacenar_csv_en_excel(df3, n3,"Datos")
                proceso = True
            elif n1:
                df1 = leer_dataframe(n1)
                lista_n1 = n1.split("\\")
                nombre_1 = lista_n1[-1].split("_")
                nombre_1 = nombre_1[1:]
                lista_n1[-1] = lista_a_texto(nombre_1, "_", False)
                n1 = lista_a_texto(lista_n1, "\\", False)
                df1.to_csv(n1, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(n1, True)
                df1 = leer_dataframe_utf_8(n1)
                n1 = n1.replace(".csv",".xlsx")
                almacenar = mod_5.almacenar_csv_en_excel(df1, n1,"Datos")
                if informar and almacenar:
                    informar_archivo_creado(n1, True)
                proceso = True
                df3 = df1.copy()
            elif n2:
                df2 = leer_dataframe(n2)
                lista_n2 = n2.split("\\")
                nombre_2 = lista_n2[-1].split("_")
                nombre_2 = nombre_2[1:]
                lista_n2[-1] = lista_a_texto(nombre_2, "_", False)
                n2 = lista_a_texto(lista_n2, "\\", False)
                df2.to_csv(n2, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(n2, True)
                df2 = leer_dataframe_utf_8(n2)
                n2 = n2.replace(".csv",".xlsx")
                almacenar = mod_5.almacenar_csv_en_excel(df2, n2,"Datos")
                if informar and almacenar:
                    informar_archivo_creado(n2, True)
                proceso = True
                df3 = df2.copy()
        if proceso:
            if len(lista_filiales_archivo) == 4:
                lista_df_filiales.append(df3)
            elif len(lista_filiales_archivo) == 1:
                lista_df_filial.append(df3)
    if len(lista_df_filiales) > 0:
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        if not codigo_DANE:
            if n1:
                n1 = n1.replace(".xlsx",".csv")
                lista_nombre = n1.split("\\")
            elif n2:
                n2 = n2.replace(".xlsx",".csv")
                lista_nombre = n2.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_",False)
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
            df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
            if informar:
                informar_archivo_creado(nuevo_nombre, True)
            df_total = leer_dataframe_utf_8(nuevo_nombre)
            if almacenar_excel:
                nuevo_nombre = nuevo_nombre.replace(".csv",".xlsx")
                almacenar = mod_5.almacenar_csv_en_excel(df_total, nuevo_nombre,"Datos")
                if informar and almacenar:
                    informar_archivo_creado(nuevo_nombre, True)
            return df_total, nuevo_nombre.replace(".xlsx",".csv")
    elif len(lista_df_filial) > 0:
        df_total = pd.concat(lista_df_filial, ignore_index=True)
        return df_total, n1.replace(".xlsx",".csv")
    else:
        return None, None

def reporte_comercial_sector_consumo_subsidio(lista_archivos, codigo_DANE, informar, seleccionar_reporte, valor_facturado):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        proceso = None
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            n1 = apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos_filial, codigo_DANE, "GRC1", informar, valor_facturado, filial,True)
            if n1:
                df1 = leer_dataframe(n1)
                lista_n1 = n1.split("\\")
                nombre_1 = lista_n1[-1].split("_")
                nombre_1 = nombre_1[1:]
                lista_n1[-1] = lista_a_texto(nombre_1, "_", False)
                n1 = lista_a_texto(lista_n1, "\\", False)
                df1.to_csv(n1, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(n1, True)
                df1 = leer_dataframe_utf_8(n1)
                n1 = n1.replace(".csv",".xlsx")
                almacenar = mod_5.almacenar_csv_en_excel(df1, n1,"Datos")
                if informar and almacenar:
                    informar_archivo_creado(n1, True)
                proceso = True
                df3 = df1.copy()
        if proceso and len(lista_filiales_archivo) == 4:
            lista_df_filiales.append(df3)
    if len(lista_filiales) > 0 and not codigo_DANE and len(lista_df_filiales) > 0:
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        if n1:
            n1 = n1.replace(".xlsx",".csv")
            lista_nombre = n1.split("\\")
        elif n2:
            n2 = n2.replace(".xlsx",".csv")
            lista_nombre = n2.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_",False)
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
        df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nuevo_nombre, True)
        df_total = leer_dataframe_utf_8(nuevo_nombre)
        nuevo_nombre = nuevo_nombre.replace(".csv",".xlsx")
        almacenar = mod_5.almacenar_csv_en_excel(df_total, nuevo_nombre,"Datos")
        if informar and almacenar:
            informar_archivo_creado(nuevo_nombre, True)

def apoyo_reporte_comparacion_prd_cld_cer(lista_archivos, informar, filial):
    lista_GRTT2 = []
    dic_SAP_CLD = {}
    dic_SAP_PRD = {}
    dic_GRC1 = {}
    lista_df_porcentaje = []
    for archivo in lista_archivos:
        if "SAP" not in archivo and "GRC1" in archivo:
            nombre_final = archivo
        dic_conteo = {"Lectura_real":0,
                    "Lectura_estimada":0,
                    "Consumo":0,
                    "Valor total facturado":0}
        lista_df = lectura_dataframe_chunk(archivo)
        if lista_df:
            df1 = lista_df[0][["Anio_reportado","Mes_reportado"]]
            for df in lista_df:
                if "GRTT2" not in archivo:
                    df_R = df[df["Tipo_lectura"]=="R"]
                    df_E = df[df["Tipo_lectura"]=="E"]
                    dic_conteo["Consumo"] += df["Consumo"].sum()
                    dic_conteo["Valor total facturado"] += df["Valor_total_facturado"].sum()
                    dic_conteo["Lectura_real"] += len(df_R)
                    dic_conteo["Lectura_estimada"] += len(df_E)
                    df_R = df[df["Tipo_lectura"]==1]
                    df_E = df[df["Tipo_lectura"]==2]
                    dic_conteo["Lectura_real"] += len(df_R)
                    dic_conteo["Lectura_estimada"] += len(df_E)
                    if "SAP_CLD" in archivo:
                        for pos in range(len(df)):
                            elemento = df["NIU"][pos]
                            factura = df["ID_factura"][pos]
                            lectura = df["Tipo_lectura"][pos]
                            if elemento not in dic_SAP_CLD:
                                dic_SAP_CLD[elemento] = [factura, lectura]
                    elif "SAP_PRD" in archivo:
                        for pos in range(len(df)):
                            elemento = df["NIU"][pos]
                            factura = df["ID_factura"][pos]
                            lectura = df["Tipo_lectura"][pos]
                            if elemento not in dic_SAP_PRD:
                                dic_SAP_PRD[elemento] = [factura, lectura]
                    elif "SAP_PRD" not in archivo and "SAP_CLD" not in archivo:
                        for pos in range(len(df)):
                            elemento = df["NIU"][pos]
                            factura = df["ID_factura"][pos]
                            lectura = df["Tipo_lectura"][pos]
                            if elemento not in dic_GRC1:
                                dic_GRC1[elemento] = [factura, lectura]
                else:
                    lista_GRTT2.extend(list(df["NIU"].unique()))
            if "GRTT2" not in archivo:
                if dic_conteo["Lectura_real"]+dic_conteo["Lectura_estimada"] == 0:
                    porcentaje_1 = "0 %"
                    porcentaje_2 = "0 %"
                else:
                    porcentaje_1 = str(round((dic_conteo["Lectura_real"]/(dic_conteo["Lectura_real"]+dic_conteo["Lectura_estimada"]))*100,2))+"%"
                    porcentaje_2 = str(round((dic_conteo["Lectura_estimada"]/(dic_conteo["Lectura_real"]+dic_conteo["Lectura_estimada"]))*100,2))+"%"
                dic_df = {"Tipo de Lectura":["R","E"],
                            "Totales":[dic_conteo["Lectura_real"], dic_conteo["Lectura_estimada"]],
                            "Porcentaje de Lectura":[porcentaje_1, porcentaje_2],
                            "Consumo m3":[dic_conteo["Consumo"], dic_conteo["Consumo"]],
                            "Valor total facturado":[dic_conteo["Valor total facturado"], dic_conteo["Valor total facturado"]]}
                df_conteo = pd.DataFrame(dic_df)
                df_conteo["Anio_reportado"] = df1["Anio_reportado"][0]
                df_conteo["Mes_reportado"] = df1["Mes_reportado"][0]
                df_conteo["Filial"] = dic_filiales[filial]
                if "SAP_CLD" in archivo:
                    df_conteo["Archivo"] = "GRC1_SAP_CLD"
                elif "SAP_PRD" in archivo:
                    df_conteo["Archivo"] = "GRC1_SAP_PRD"
                else:
                    df_conteo["Archivo"] = "GRC1"
                lista_df_porcentaje.append(df_conteo)
        else:
            return None
    df_porcentaje = pd.concat(lista_df_porcentaje, ignore_index=True)
    df_GRC1 = df_porcentaje[df_porcentaje["Archivo"] == "GRC1"].reset_index(drop=True)
    if len(df_GRC1) > 0:
        valor_consumo_GRC1 = df_GRC1["Consumo m3"][0]
        valor_facturado_GRC1 = df_GRC1["Valor total facturado"][0]
    else:
        valor_consumo_GRC1 = 0
        valor_facturado_GRC1 = 0
    df_GRC1_CLD = df_porcentaje[df_porcentaje["Archivo"] == "GRC1_SAP_CLD"].reset_index(drop=True)
    if len(df_GRC1_CLD) > 0:
        valor_consumo_GRC1_CLD = df_GRC1_CLD["Consumo m3"][0]
        valor_facturado_GRC1_CLD = df_GRC1_CLD["Valor total facturado"][0]
    else:
        valor_consumo_GRC1_CLD = 0
        valor_facturado_GRC1_CLD = 0
    df_GRC1_PRD = df_porcentaje[df_porcentaje["Archivo"] == "GRC1_SAP_PRD"].reset_index(drop=True)
    if len(df_GRC1_PRD) > 0:
        valor_consumo_GRC1_PRD = df_GRC1_PRD["Consumo m3"][0]
        valor_facturado_GRC1_PRD = df_GRC1_PRD["Valor total facturado"][0]
    else:
        valor_consumo_GRC1_PRD = 0
        valor_facturado_GRC1_PRD = 0
    if valor_consumo_GRC1 == 0:
        porcentaje_consumo_GRC1_CLD = "0 %"
        porcentaje_consumo_GRC1_PRD = "0 %"
    else:

        porcentaje_consumo_GRC1_CLD = str(round((abs(valor_consumo_GRC1_CLD-valor_consumo_GRC1)/valor_consumo_GRC1)*100,2))+" %"
        porcentaje_consumo_GRC1_PRD = str(round((abs(valor_consumo_GRC1_PRD-valor_consumo_GRC1)/valor_consumo_GRC1)*100,2))+" %"
    if valor_facturado_GRC1 == 0:
        porcentaje_facturado_GRC1_CLD = "0 %"
        porcentaje_facturado_GRC1_PRD = "0 %"
    else:
        porcentaje_facturado_GRC1_CLD = str(round((abs(valor_facturado_GRC1_CLD-valor_facturado_GRC1)/valor_facturado_GRC1)*100,2))+" %"
        porcentaje_facturado_GRC1_PRD = str(round((abs(valor_facturado_GRC1_PRD-valor_facturado_GRC1)/valor_facturado_GRC1)*100,2))+" %"
    df_porcentaje["Diff. Porcentual Consumo m3"] = "0 %"
    df_porcentaje["Diff. Porcentual Valor total facturado"] = "0 %"
    df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_CLD', 'Diff. Porcentual Consumo m3'] = porcentaje_consumo_GRC1_CLD
    df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_PRD', 'Diff. Porcentual Consumo m3'] = porcentaje_consumo_GRC1_PRD
    df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_CLD', "Diff. Porcentual Valor total facturado"] = porcentaje_facturado_GRC1_CLD
    df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_PRD', "Diff. Porcentual Valor total facturado"] = porcentaje_facturado_GRC1_PRD
    df_porcentaje = df_porcentaje[["Archivo","Filial","Anio_reportado","Mes_reportado","Tipo de Lectura","Totales","Porcentaje de Lectura","Consumo m3",
                                    "Valor total facturado",'Diff. Porcentual Consumo m3','Diff. Porcentual Valor total facturado']]
    nombre = nombre_final.replace("_resumen", "_porcentaje")
    df_porcentaje.to_csv(nombre, index=False)
    if informar:
        informar_archivo_creado(nombre, True)
    nombre = nombre.replace(".csv",".xlsx")
    almacenar = mod_5.almacenar_csv_en_excel(df_porcentaje, nombre,"Datos")
    if almacenar and informar:
        informar_archivo_creado(nombre, True)
    dic_total = {"NIU":[],
                "Tipo de lectura GRC1 CLD":[],
                "Tipo de lectura GRC1 PRD":[],
                "Tipo de lectura GRC1":[],
                "Factura GRC1":[],
                "Factura GRC1 CLD":[],
                "Factura GRC1 PRD":[],
                "Existe GRTT2":[]}
    if len(dic_SAP_CLD) > cantidad_datos_excel:
        lista_llaves = list(dic_SAP_CLD.keys())[:cantidad_datos_excel]
        lista_valores = list(dic_SAP_CLD.values())[:cantidad_datos_excel]
    else:
        lista_llaves = list(dic_SAP_CLD.keys())
        lista_valores = list(dic_SAP_CLD.values())
    for i in range(len(lista_llaves)):
        llave = lista_llaves[i]
        valor = lista_valores[i]
        valor_1 = None
        valor_2 = None
        try:
            valor_1 = dic_GRC1[llave]
            valor_2 = dic_SAP_PRD[llave]
            if valor_1 and valor_2:
                dic_total["Tipo de lectura GRC1"].append(valor_1[1])
                dic_total["Factura GRC1"].append(valor_1[0])
                dic_total["Tipo de lectura GRC1 PRD"].append(valor_2[1])
                dic_total["Factura GRC1 PRD"].append(valor_2[0])
                dic_total["NIU"].append(llave)
                dic_total["Tipo de lectura GRC1 CLD"].append(valor[1])
                dic_total["Factura GRC1 CLD"].append(valor[0])
                if llave in lista_GRTT2:
                    dic_total["Existe GRTT2"].append(1)
                else:
                    dic_total["Existe GRTT2"].append(2)
        except KeyError:
            pass
    df_total = pd.DataFrame(dic_total)
    nombre_final = nombre_final.replace("_resumen", "_total")
    df_total["Anio_reportado"] = df1["Anio_reportado"][0]
    df_total["Mes_reportado"] = df1["Mes_reportado"][0]
    df_total["Filial"] = dic_filiales[filial]
    df_total.to_csv(nombre_final, index=False)
    if informar:
        informar_archivo_creado(nombre_final, True)
    nombre_final = nombre_final.replace(".csv",".xlsx")
    almacenar = mod_5.almacenar_csv_en_excel(df_total, nombre_final,"Datos")
    if informar and almacenar:
        informar_archivo_creado(nombre_final, True)

def reporte_comparacion_prd_cld_cer(lista_archivos, seleccionar_reporte, informar):
    for filial in seleccionar_reporte["filial"]:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            apoyo_reporte_comparacion_prd_cld_cer(lista_archivos_filial, informar, filial)

def configurar_cantidad_filas_dataframe(lista_df, cantidad_filas):
    nueva_lista_df = []
    conteo = 0
    for i in lista_df:
        if conteo < cantidad_filas:
            nueva_lista_df.append(i)
            conteo += len(i)
        if conteo >= cantidad_filas:
            return nueva_lista_df
    return nueva_lista_df

def listas_diferentes(lista_1, lista_2, llave):
    largo_1 = len(lista_1)
    largo_2 = len(lista_2)
    if largo_1 != largo_2:
        return False,False
    else:
        conteo = 0
        dic_diferencias = {llave:[]}
        for i in range(largo_1):
            try:
                if pd.isna(lista_1[i]):
                    lista_1[i] = 0
                if pd.isna(lista_2[i]):
                    lista_2[i] = 0
                if lista_1[i] == 1 and lista_2[i] == "R":
                    dic_diferencias[llave].append((lista_1[i],lista_2[i],True))
                elif lista_1[i] == 2 and lista_2[i] == "E":
                    dic_diferencias[llave].append((lista_1[i],lista_2[i],True))
                elif lista_1[i] == lista_2[i]:
                    dic_diferencias[llave].append((lista_1[i],lista_2[i],True))
                else:
                    dic_diferencias[llave].append((lista_1[i],lista_2[i],False))
                    conteo += 1
            except ValueError:
                pass
            except TypeError:
                pass
        if conteo < 1:
            return False, dic_diferencias, conteo
        else:
            return True, dic_diferencias, conteo

def apoyo_reporte_comparacion_cld(lista_archivos, informar, filial,cantidad_filas):
    lista_1 = ["NIU",
        "ID_factura",
        "Tipo_factura",
        "Tipo_lectura",
        "Factor_poder_calorfico_fpc",
        "Lectura_anterior",
        "Lectura_actual",
        "Factor_correccion_utilizado",
        "Consumo",
        "Cuv_cargo_aplicado_consumo",
        "Facturacion_consumo",
        "Facturacion_cargo_fijo",
        "Valor_subsidio_contribucion",
        "Porcentaje_subsidio_contribucion_aplicado",
        "Valor_cuota_conexion",
        "Suspension_reconexion",
        "Corte_reinstalacion",
        "Valor_otros_conceptos",
        "Refacturacion_consumos",
        "Valor_refacturacion",
        "Valor_refacturacion_subsidio_contribucion",
        "Valor_total_facturado"]
    for archivo in lista_archivos:
        if "_CLD" not in archivo:
            nombre_archivo = archivo
            dic_dataframe = {}
            lista_archivo = archivo.split("\\")
            for reporte in lista_reportes_totales:
                if reporte in lista_archivo[-1]:
                    dic_reporte = leer_archivos_json(ruta_constantes+f"/{reporte.upper()}.json")
            if dic_reporte:
                lista_df = lectura_dataframe_chunk(archivo,15000)
                if lista_df:
                    nueva_lista_df = configurar_cantidad_filas_dataframe(lista_df, cantidad_filas)
                    if len(nueva_lista_df) == 1 and len(nueva_lista_df[0]) > cantidad_filas:
                        nueva_lista_df[0] = nueva_lista_df[0].iloc[:cantidad_filas]
                    for df in nueva_lista_df:
                        df1 = df.copy().reset_index(drop=True)
                        df1 = df1[lista_1]
                        for i in range(len(df1)):
                            dic_dataframe[df1["ID_factura"][i]] = df1.iloc[i].tolist()
        else:
            lista_df = lectura_dataframe_chunk(archivo)
            dic_dataframe_CLD = {}
            if lista_df:
                for df in lista_df:
                    df1 = df[lista_1]
                    for i in range(len(df1)):
                        dic_dataframe_CLD[df1["ID_factura"][i]] = df1.iloc[i].tolist()
    lista_iguales = []
    lista_diferentes = []
    for llave in dic_dataframe:
        try:
            diferentes,valor,conteo = listas_diferentes(dic_dataframe[llave], dic_dataframe_CLD[llave],llave)
            if diferentes:
                lista_diferentes.append(valor)
            else:
                lista_iguales.append(valor)
        except KeyError:
            pass
    largo = len(lista_1)
    print(f"Para {len(lista_iguales)+len(lista_diferentes)} filas evaluadas: {len(lista_iguales)} filas iguales, {len(lista_diferentes)} filas diferentes")
    lista_df_iguales = [[] for _ in range(largo)]
    lista_df_diferentes = [[] for _ in range(largo)]
    lista_df_diferentes_excel = [[] for _ in range(largo)]
    for dic in lista_iguales:
        for lista in dic.values():
            for i in range(len(lista)):
                lista_df_iguales[i].append(lista[i][0])
    dic_df_iguales = {}
    for i in range(largo):
        dic_df_iguales[lista_1[i]] = lista_df_iguales[i]
    df_iguales = pd.DataFrame(dic_df_iguales)
    df_iguales.to_csv(nombre_archivo.replace("_resumen", "_comparacion_iguales"), index=False, encoding="utf-8-sig")
    if informar:
        informar_archivo_creado(nombre_archivo.replace("_resumen", "_comparacion_iguales"),True)
    nombre_final = nombre_archivo.replace("_resumen", "_comparacion_iguales").replace(".csv",".xlsx")
    almacenar = mod_5.almacenar_csv_en_excel(df_iguales, nombre_final,"Datos")
    if informar and almacenar:
        informar_archivo_creado(nombre_final, True)
    for dic in lista_diferentes:
        for lista in dic.values():
            for i in range(len(lista)):
                lista_df_diferentes[i].append((lista[i][0],lista[i][1]))
    dic_df_diferentes = {}
    for i in range(largo):
        dic_df_diferentes[lista_1[i]] = lista_df_diferentes[i]
    df_diferentes = pd.DataFrame(dic_df_diferentes)
    df_diferentes.to_csv(nombre_archivo.replace("_resumen", "_comparacion_diferentes"), index=False, encoding="utf-8-sig")
    if informar:
        informar_archivo_creado(nombre_archivo.replace("_resumen", "_comparacion_diferentes"),True)
    for dic in lista_diferentes:
        for lista in dic.values():
            for i in range(len(lista)):
                lista_df_diferentes_excel[i].append(lista[i])
    dic_df_diferentes_excel = {}
    for i in range(largo):
        dic_df_diferentes_excel[lista_1[i]] = lista_df_diferentes_excel[i]
    df_diferentes_excel = pd.DataFrame(dic_df_diferentes_excel)
    nombre_final = nombre_archivo.replace("_resumen", "_comparacion_diferentes").replace(".csv",".xlsx")
    almacenar = mod_5.almacenar_csv_en_excel_patrones(df_diferentes_excel, nombre_final,"Datos")
    if informar and almacenar:
        informar_archivo_creado(nombre_final, True)

def reporte_comparacion_cld(lista_archivos, seleccionar_reporte, informar, cantidad_filas):
    for filial in seleccionar_reporte["filial"]:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            apoyo_reporte_comparacion_cld(lista_archivos_filial, informar, filial,cantidad_filas)


def apoyo_reporte_comparacion_prd_cld(lista_archivos, informar, filial,cantidad_filas):
    lista_1 = ["NIU",
        "ID_factura",
        "Tipo_factura",
        "Tipo_lectura",
        "Factor_poder_calorfico_fpc",
        "Lectura_anterior",
        "Lectura_actual",
        "Factor_correccion_utilizado",
        "Consumo",
        "Cuv_cargo_aplicado_consumo",
        "Facturacion_consumo",
        "Facturacion_cargo_fijo",
        "Valor_subsidio_contribucion",
        "Porcentaje_subsidio_contribucion_aplicado",
        "Valor_cuota_conexion",
        "Suspension_reconexion",
        "Corte_reinstalacion",
        "Valor_otros_conceptos",
        "Refacturacion_consumos",
        "Valor_refacturacion",
        "Valor_refacturacion_subsidio_contribucion",
        "Valor_total_facturado"]
    for archivo in lista_archivos:
        if "_CLD" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            dic_dataframe_CLD = {}
            if lista_df:
                for df in lista_df:
                    df1 = df[lista_1]
                    for i in range(len(df1)):
                        dic_dataframe_CLD[df1["ID_factura"][i]] = df1.iloc[i].tolist()
        elif "_PRD" in archivo:
            nombre_archivo = archivo
            dic_dataframe_PRD = {}
            lista_archivo = archivo.split("\\")
            for reporte in lista_reportes_totales:
                if reporte in lista_archivo[-1]:
                    dic_reporte = leer_archivos_json(ruta_constantes+f"/{reporte.upper()}.json")
            if dic_reporte:
                lista_df = lectura_dataframe_chunk(archivo,15000)
                if lista_df:
                    nueva_lista_df = configurar_cantidad_filas_dataframe(lista_df, cantidad_filas)
                    if len(nueva_lista_df) == 1 and len(nueva_lista_df[0]) > cantidad_filas:
                        nueva_lista_df[0] = nueva_lista_df[0].iloc[:cantidad_filas]
                    for df in nueva_lista_df:
                        df1 = df.copy().reset_index(drop=True)
                        df1 = df1[lista_1]
                        for i in range(len(df1)):
                            dic_dataframe_PRD[df1["ID_factura"][i]] = df1.iloc[i].tolist()
    lista_iguales = []
    lista_diferentes = []
    for llave in dic_dataframe_CLD:
        try:
            diferentes,valor,conteo = listas_diferentes(dic_dataframe_PRD[llave], dic_dataframe_CLD[llave],llave)
            if diferentes:
                lista_diferentes.append(valor)
            else:
                lista_iguales.append(valor)
        except KeyError:
            pass
    largo = len(lista_1)
    print(f"Para {len(lista_iguales)+len(lista_diferentes)} filas evaluadas: {len(lista_iguales)} filas iguales, {len(lista_diferentes)} filas diferentes")
    lista_df_iguales = [[] for _ in range(largo)]
    lista_df_diferentes = [[] for _ in range(largo)]
    lista_df_diferentes_excel = [[] for _ in range(largo)]
    for dic in lista_iguales:
        for lista in dic.values():
            for i in range(len(lista)):
                lista_df_iguales[i].append(lista[i][0])
    dic_df_iguales = {}
    for i in range(largo):
        dic_df_iguales[lista_1[i]] = lista_df_iguales[i]
    df_iguales = pd.DataFrame(dic_df_iguales)
    df_iguales.to_csv(nombre_archivo.replace("_resumen", "_comparacion_iguales_prd_cld"), index=False, encoding="utf-8-sig")
    if informar:
        informar_archivo_creado(nombre_archivo.replace("_resumen", "_comparacion_iguales_prd_cld"),True)
    nombre_final = nombre_archivo.replace("_resumen", "_comparacion_iguales_prd_cld").replace(".csv",".xlsx")
    almacenar = mod_5.almacenar_csv_en_excel(df_iguales, nombre_final,"Datos")
    if informar and almacenar:
        informar_archivo_creado(nombre_final, True)
    for dic in lista_diferentes:
        for lista in dic.values():
            for i in range(len(lista)):
                lista_df_diferentes[i].append((lista[i][0],lista[i][1]))
    dic_df_diferentes = {}
    for i in range(largo):
        dic_df_diferentes[lista_1[i]] = lista_df_diferentes[i]
    df_diferentes = pd.DataFrame(dic_df_diferentes)
    df_diferentes.to_csv(nombre_archivo.replace("_resumen", "_comparacion_diferentes_prd_cld"), index=False, encoding="utf-8-sig")
    if informar:
        informar_archivo_creado(nombre_archivo.replace("_resumen", "_comparacion_diferentes_prd_cld"),True)
    for dic in lista_diferentes:
        for lista in dic.values():
            for i in range(len(lista)):
                lista_df_diferentes_excel[i].append(lista[i])
    dic_df_diferentes_excel = {}
    for i in range(largo):
        dic_df_diferentes_excel[lista_1[i]] = lista_df_diferentes_excel[i]
    df_diferentes_excel = pd.DataFrame(dic_df_diferentes_excel)
    nombre_final = nombre_archivo.replace("_resumen", "_comparacion_diferentes_prd_cld").replace(".csv",".xlsx")
    almacenar = mod_5.almacenar_csv_en_excel_patrones(df_diferentes_excel, nombre_final,"Datos")
    if informar and almacenar:
        informar_archivo_creado(nombre_final, True)

def reporte_comparacion_prd_cld(lista_archivos, seleccionar_reporte, informar, cantidad_filas):
    for filial in seleccionar_reporte["filial"]:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            apoyo_reporte_comparacion_prd_cld(lista_archivos_filial, informar, filial,cantidad_filas)

def reporte_info_comercial_mensual(lista_archivos, informar, seleccionar_reporte, valor_facturado=True, almacenar_excel=True):
    df, archivo = reporte_comercial_sector_consumo(lista_archivos, False, False, seleccionar_reporte, valor_facturado)
    if archivo != None:
        columnas = df.columns
        lista_df = []
        lista_filiales = list(df["Filial"].unique())
        lista_tipo_usuarios = list(df["Tipo de usuario"].unique())
        for filial in lista_filiales:
            df_filial = df[df["Filial"] == filial].reset_index(drop=True)
            nueva_fila_final = []
            for columna in columnas:
                if columna in ["Cantidad de usuarios","Consumo m3","Valor total facturado"]:
                    nueva_fila_final.append(df_filial[columna].sum())
                elif columna in ["NIT","Filial","Anio reportado","Mes reportado"]:
                    nueva_fila_final.append(df_filial[columna][0])
                else:
                    nueva_fila_final.append("Total")
            for usuario in lista_tipo_usuarios:
                df_usuario = df_filial[df_filial["Tipo de usuario"] == usuario].reset_index(drop=True)
                nueva_fila = []
                for columna in columnas:
                    if columna in ["Cantidad de usuarios","Consumo m3","Valor total facturado"]:
                        nueva_fila.append(df_usuario[columna].sum())
                    elif columna in ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario"]:
                        nueva_fila.append(df_usuario[columna][0])
                    else:
                        nueva_fila.append("Total")
                df_filial.loc[len(df_filial)] = nueva_fila
            df_filial.loc[len(df_filial)] = nueva_fila_final
            lista_df.append(df_filial)
        if len(lista_df) > 0:
            df_total = pd.concat(lista_df, ignore_index=True)
            df_final = df_total[df_total["Sector de consumo"] == "Total"].reset_index(drop=True)
            nueva_fila_final = []
            for columna in columnas:
                if columna in ["Cantidad de usuarios","Consumo m3","Valor total facturado"]:
                    nueva_fila_final.append(df_final[columna].sum())
                elif columna in ["Anio reportado","Mes reportado"]:
                    nueva_fila_final.append(df_final[columna][0])
                elif columna in ["NIT","Filial"]:
                    nueva_fila_final.append(grupo_vanti)
                else:
                    nueva_fila_final.append("Total")
            df_total.loc[len(df_total)] = nueva_fila_final
            if len(seleccionar_reporte["filial"]) > 0:
                n_nombre = archivo.replace("_reporte_consumo","_info_comercial")
            else:
                filial = seleccionar_reporte["filial"][0]
                n_nombre = archivo.replace("_reporte_consumo",f"_{filial}_info_comercial")
            df_total = lista_porcentaje_dataframe(df_total)
            df_total.to_csv(n_nombre, index=False, encoding="utf-8-sig")
            if informar:
                informar_archivo_creado(n_nombre, True)
            df_total = leer_dataframe_utf_8(n_nombre)
            if almacenar_excel:
                n_nombre = n_nombre.replace(".csv",".xlsx")
                almacenar = mod_5.almacenar_csv_en_excel(df_total, n_nombre,"Datos")
                if informar and almacenar:
                    informar_archivo_creado(n_nombre, True)
            return df_total, n_nombre.replace(".xlsx",".csv")
        else:
            return None, None
    else:
        return None, None

def aux_lista_porcentaje_dataframe(df_filial, columna):
    dic = {}
    lista_porcentaje = []
    lista_tipo_usuario = list(df_filial["Tipo de usuario"].unique())
    for tipo_usuario in lista_tipo_usuario:
        df_total = df_filial[(df_filial["Tipo de usuario"] == tipo_usuario) & (df_filial["Sector de consumo"]=="Total")].reset_index(drop=True)
        dic[tipo_usuario] = df_total[columna][0]
    lista_tipo_usuario.remove("Total")
    for tipo_usuario in lista_tipo_usuario:
        df_usuario = df_filial[(df_filial["Tipo de usuario"] == tipo_usuario) & (df_filial["Sector de consumo"] != "Total")].reset_index(drop=True)
        lista_sector_consumo = list(df_usuario["Sector de consumo"].unique())
        for sector_consumo in lista_sector_consumo:
            df_sector_consumo = df_usuario[df_usuario["Sector de consumo"] == sector_consumo].reset_index(drop=True)
            porcentaje = round((df_sector_consumo[columna][0]/dic[tipo_usuario])*100,2)
            lista_porcentaje.append(str(porcentaje)+" %")
    for tipo_usuario in lista_tipo_usuario:
        df_usuario = df_filial[(df_filial["Tipo de usuario"] == tipo_usuario) & (df_filial["Sector de consumo"] == "Total")].reset_index(drop=True)
        porcentaje = round((df_usuario[columna][0]/dic["Total"])*100,2)
        lista_porcentaje.append(str(porcentaje)+" %")
    lista_porcentaje.append("100 %")
    return lista_porcentaje

def lista_porcentaje_dataframe(df):
    lista_df = []
    lista_columnas_num = ["Cantidad de usuarios","Consumo m3","Valor total facturado"]
    for filial in list(df["Filial"].unique()):
        lista_por_usuarios = []
        lista_por_consumo = []
        lista_por_valor_facturado = []
        df_filial =  df[df["Filial"] == filial].reset_index(drop=True)
        for columna in lista_columnas_num:
            if columna == "Cantidad de usuarios":
                lista_por_usuarios.extend(aux_lista_porcentaje_dataframe(df_filial, columna))
            elif columna =="Consumo m3":
                lista_por_consumo.extend(aux_lista_porcentaje_dataframe(df_filial, columna))
            elif columna == "Valor total facturado":
                lista_por_valor_facturado.extend(aux_lista_porcentaje_dataframe(df_filial, columna))
        df_filial["Porcentaje Cantidad de usuarios"] = lista_por_usuarios
        df_filial["Porcentaje Consumo m3"] = lista_por_consumo
        df_filial["Porcentaje Valor total facturado"] = lista_por_valor_facturado
        lista_df.append(df_filial)
    df = pd.concat(lista_df, ignore_index=True)
    return df

def dif_numerica_listas(lista_actual, lista_anterior):
    lista_diferencia = []
    if len(lista_actual) == len(lista_anterior):
        for i in range(len(lista_actual)):
            diferencia = lista_actual[i] - lista_anterior[i]
            lista_diferencia.append(diferencia)
        return lista_diferencia
    else:
        return lista_diferencia

def diferencia_columnas_dataframe(df_actual, df_anterior):
    df_actual = df_actual.copy().reset_index(drop=True)
    df_anterior = df_anterior.copy().reset_index(drop=True)
    lista_columnas_num = ["Cantidad de usuarios","Consumo m3","Valor total facturado"]
    for columna in lista_columnas_num:
        df_actual["Diferencia "+columna] = None
    for i in range(len(df_actual)):
        df_filtro_anterior = df_anterior[(df_anterior["Tipo de usuario"] == df_actual["Tipo de usuario"][i]) &
                                            (df_anterior["Sector de consumo"] == df_actual["Sector de consumo"][i]) &
                                            (df_anterior["Filial"] == df_actual["Filial"][i])].reset_index(drop=True)
        df_filtro_actual = df_actual[(df_actual["Tipo de usuario"] == df_actual["Tipo de usuario"][i]) &
                                            (df_actual["Sector de consumo"] == df_actual["Sector de consumo"][i]) &
                                            (df_actual["Filial"] == df_actual["Filial"][i])].reset_index(drop=True)
        if len(df_filtro_anterior) > 0 and len(df_filtro_actual):
            for columna in lista_columnas_num:
                valor_actual = df_filtro_actual[columna][0]
                valor_anterior = df_filtro_anterior[columna][0]
                df_actual.iloc[i, df_actual.columns.get_loc("Diferencia "+columna)] = valor_actual - valor_anterior
    return df_actual

def reporte_info_comercial_anual(lista_archivos, lista_archivos_aux, informar, seleccionar_reporte, lista_fechas):
    lista_df_anual = []
    lista_df_anual_dif = []
    df, nombre = reporte_info_comercial_mensual(lista_archivos_aux, informar, seleccionar_reporte,almacenar_excel=False)
    if nombre != None:
        lista_df_anual.append(df)
    for fecha in lista_fechas:
        print(fecha)
        lista_archivos_fecha = []
        for archivo in lista_archivos:
            if fecha[0] in archivo and fecha[1].upper() in archivo:
                lista_archivos_fecha.append(archivo)
        df, nombre = reporte_info_comercial_mensual(lista_archivos_fecha, informar, seleccionar_reporte,almacenar_excel=False)
        if nombre != None:
            lista_df_anual.append(df)
    for i in range(1,len(lista_df_anual)):
        df_actual = diferencia_columnas_dataframe(lista_df_anual[i], lista_df_anual[i-1])
        lista_df_anual_dif.append(df_actual)
    if len(lista_df_anual) > 0:
        lista_nombre = nombre.split("\\")
        lista_nombre[-6] = "02. Compilado"
        lista_nombre[-4] = "00. Compilado"
        n1 = lista_nombre[-1].split("_")
        n1[0] = lista_a_texto([lista_fechas[0][0],lista_fechas[0][1]],"_",False)
        n1[1] = lista_a_texto([lista_fechas[-1][0],lista_fechas[-1][1]],"_",False)
        lista_nombre[-1] = lista_a_texto(n1,"_",False)
        nombre = lista_a_texto(lista_nombre,"\\",False)
        df_total = pd.concat(lista_df_anual_dif, ignore_index=True)
        df_total.to_csv(nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nombre, True)
        df_total = leer_dataframe_utf_8(nombre)
        nombre = nombre.replace(".csv",".xlsx")
        almacenar = mod_5.almacenar_csv_en_excel(df_total, nombre,"Datos")
        if informar and almacenar:
            informar_archivo_creado(nombre, True)

def apoyo_reporte_usuarios_filial(lista_archivos,informar,filial,almacenar_excel=True):
    for archivo in lista_archivos:
        lista_df = lectura_dataframe_chunk(archivo)
        dic_dataframe = {}
        if lista_df:
            for i in range(len(lista_df)):
                df = lista_df[i]
                df = df[df["Estado"] == 1].reset_index(drop=True)
                df = df[["NIU","Codigo_DANE","Direccion","Cedula_Catastral","Estrato","Longitud","Latitud"]]
                df = df[df['Estrato'].apply(lambda x: isinstance(x, int))].reset_index(drop=True)
                lista_estrato_texto = []
                for j in range(len(df)):
                    try:
                        estrato_texto = tabla_3["datos"][str(df["Estrato"][j])]
                        lista_estrato_texto.append(estrato_texto)
                        if int(df["Estrato"][j]) not in dic_dataframe:
                            dic_dataframe[int(df["Estrato"][j])] = 0
                        dic_dataframe[int(df["Estrato"][j])] += 1
                    except KeyError:
                        lista_estrato_texto.append("")
                df["Estrato"] = lista_estrato_texto
                lista_df[i] = df
    dic_dataframe = dict(sorted(dic_dataframe.items()))
    dic_dataframe_texto = {}
    for i,j in dic_dataframe.items():
        dic_dataframe_texto[tabla_3["datos"][str(i)]] = j
    dic_dataframe_texto = {"Estrato":list(dic_dataframe_texto.keys()),
                            "Cantidad de usuarios":list(dic_dataframe_texto.values())}
    df_filial_resumen = pd.DataFrame(dic_dataframe_texto)
    df_filial_resumen["Filial"] = dic_filiales[filial]
    df_filial_resumen.to_csv(archivo.replace("_resumen","_inventario_suscriptores_compendio"), index=False, encoding="utf-8-sig")
    if informar:
        informar_archivo_creado(archivo.replace("_resumen","_inventario_suscriptores_compendio"), True)
    df_filial_resumen = leer_dataframe_utf_8(archivo.replace("_resumen","_inventario_suscriptores_compendio"))
    almacenar = mod_5.almacenar_csv_en_excel(df_filial_resumen, archivo.replace("_resumen","_inventario_suscriptores_compendio").replace(".csv",".xlsx"),"Datos")
    if informar and almacenar and almacenar_excel:
        informar_archivo_creado(archivo.replace("_resumen","_inventario_suscriptores_compendio").replace(".csv",".xlsx"), True)
    df_filial = pd.concat(lista_df, ignore_index=True)
    return df_filial, archivo

def reporte_usuarios_filial(lista_archivos, informar, seleccionar_reporte):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df,nombre = apoyo_reporte_usuarios_filial(lista_archivos_filial,informar,filial)
            if nombre:
                nombre = nombre.replace("_resumen","_inventario_suscriptores")
                df.to_csv(nombre, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(nombre, True)

def apoyo_generar_reporte_compensacion_mensual(lista_archivos,informar,filial,almacenar_excel=True):
    proceso1 = False
    df1 = pd.DataFrame()
    for archivo in lista_archivos:
        if "GRC3" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                nombre = archivo
                dic_df = {"Mes_compensado":[],"Anio_compensado":[],"CI":[],"Usuarios_compensados":[],"Valor_compensado":[]}
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                for i in range(len(lista_df)):
                    df = lista_df[i]
                    df_compensacion = df.copy().reset_index(drop=True)
                    lista_meses_compen = list(df["Periodo_compensado"].unique())
                    lista_anios_compen = list(df["Anio"].unique())
                    for mes in lista_meses_compen:
                        for anio in lista_anios_compen:
                            df_filtrado = df[(df["Periodo_compensado"] == mes) & (df["Anio"] == anio)].reset_index(drop=True)
                            if len(df_filtrado) > 0:
                                dic_df["Mes_compensado"].append(mes)
                                dic_df["Anio_compensado"].append(anio)
                                dic_df["CI"].append(df_filtrado["CI"][0])
                                dic_df["Usuarios_compensados"].append(len(df_filtrado))
                                dic_df["Valor_compensado"].append(df_filtrado["Valor_compensado"].sum())
                df1 = pd.DataFrame(dic_df)
                lista_fila = ["Total","Total",df1["CI"][0],df1["Usuarios_compensados"].sum(),df1["Valor_compensado"].sum()]
                df1.loc[len(df1)] = lista_fila
                df1["Filial"] = dic_filiales[filial]
                df1["Mes_reportado"] = mes_reportado
                df1["Anio_reportado"] = anio_reportado
                df1.to_csv(archivo.replace("_resumen","_reporte_compensacion"), index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(archivo.replace("_resumen","_reporte_compensacion"), True)
                df1 = leer_dataframe_utf_8(archivo.replace("_resumen","_reporte_compensacion"))
                if almacenar_excel:
                    almacenar = mod_5.almacenar_csv_en_excel(df1,archivo.replace("_resumen","_reporte_compensacion").replace(".csv",".xlsx"),"Datos")
                    if informar and almacenar:
                        informar_archivo_creado(archivo.replace("_resumen","_reporte_compensacion").replace(".csv",".xlsx"), True)
                proceso1=True
            else:
                return None,None
    if proceso1:
        for archivo in lista_archivos:
            if "GRTT2" in archivo:
                lista_df = lectura_dataframe_chunk(archivo)
                dic_dataframe = {}
                if lista_df:
                    columnas = ["NIU","Codigo_DANE","Estrato","Longitud","Latitud","ID_Mercado"]
                    for i in range(len(lista_df)):
                        df = lista_df[i]
                        df = df[columnas]
                        df = df[df['Estrato'].apply(lambda x: isinstance(x, int))].reset_index(drop=True)
                        for j in range(len(df)):
                            valor_NIU = df["NIU"][j]
                            try:
                                valor_dic = dic_dataframe[valor_NIU]
                            except KeyError:
                                dic_dataframe[valor_NIU] = df.iloc[j].tolist()
                            try:
                                estrato_texto = tabla_3["datos"][str(df["Estrato"][j])]
                                dic_dataframe[valor_NIU][2] = estrato_texto
                            except KeyError:
                                dic_dataframe[valor_NIU][2] = ""
                            try:
                                dic_dataframe[valor_NIU][-1] = int(dic_dataframe[valor_NIU][-1])
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                            try:
                                dic_dataframe[valor_NIU][1] = int(dic_dataframe[valor_NIU][1])
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                    lista_nueva = [[] for _ in range(5)]
                    for i in range(len(df_compensacion)):
                        valor_NIU = df_compensacion["NIU"][i]
                        try:
                            lista_valor_NIU = dic_dataframe[valor_NIU]
                            for j in range(1,len(lista_valor_NIU)):
                                lista_nueva[j-1].append(lista_valor_NIU[j])
                        except KeyError:
                            for j in range(1,len(columnas)):
                                lista_nueva[j-1].append("")
                    for i in range(1,len(lista_valor_NIU)):
                        columna = columnas[i]
                        df_compensacion[columna] = lista_nueva[i-1]
                    df_compensacion.to_csv(nombre.replace("_resumen","_reporte_compensacion"), index=False, encoding="utf-8-sig")
                    if informar:
                        informar_archivo_creado(nombre.replace("_resumen","_reporte_compensacion"), True)
                    df_compensacion = leer_dataframe_utf_8(nombre.replace("_resumen","_reporte_compensacion"))
                    almacenar = mod_5.almacenar_csv_en_excel(df_compensacion, nombre.replace("_resumen","_reporte_compensacion").replace(".csv",".xlsx"),"Datos")
                    if informar and almacenar and almacenar_excel:
                        informar_archivo_creado(nombre.replace("_resumen","_reporte_compensacion").replace(".csv",".xlsx"), True)
        return df1, nombre
    return None,None

def generar_reporte_compensacion_mensual(lista_archivos, seleccionar_reporte, informar, almacenar_excel=True):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df1,nombre = apoyo_generar_reporte_compensacion_mensual(lista_archivos_filial,informar,filial)
            if nombre:
                lista_df_filiales.append(df1)
    if len(lista_df_filiales) > 0 and len(lista_filiales_archivo) == 4:
        df_total_compilado = pd.concat(lista_df_filiales, ignore_index=True)
        lista_fila = []
        df_filtro = df_total_compilado[df_total_compilado["Anio_compensado"]=="Total"].reset_index(drop=True)
        lista_fila.append("Total")
        lista_fila.append("Total")
        lista_fila.append(df_filtro["CI"][0])
        lista_fila.append(df_filtro["Usuarios_compensados"].sum())
        lista_fila.append(df_filtro["Valor_compensado"].sum())
        lista_fila.append(grupo_vanti)
        lista_fila.append(df_filtro["Mes_reportado"][0])
        lista_fila.append(df_filtro["Anio_reportado"][0])
        df_total_compilado.loc[len(df_total_compilado)] = lista_fila
        df_total_compilado = df_total_compilado[["Filial","Mes_reportado","Anio_reportado","Usuarios_compensados","Valor_compensado","CI","Mes_compensado","Anio_compensado"]]
        lista_nombre = nombre.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
        nuevo_nombre = nuevo_nombre.replace("_resumen","_reporte_compensacion")
        df_total_compilado.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nuevo_nombre, True)
        df1 = leer_dataframe_utf_8(nuevo_nombre)
        if almacenar_excel:
            almacenar = mod_5.almacenar_csv_en_excel(df1,nuevo_nombre.replace(".csv",".xlsx"),"Datos")
            if informar and almacenar:
                informar_archivo_creado(nuevo_nombre.replace(".csv",".xlsx"), True)
        return df1, nuevo_nombre

def apoyo_reporte_usuarios_unicos_mensual(lista_archivos, informar, filial):
    for archivo in lista_archivos:
        if "GRC1" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                dic_reg = {}
                for df in lista_df:
                    for i in range(len(df)):
                        factura = str(df["ID_factura"][i]).upper()
                        if factura[0] == "F":
                            try:
                                valor = dic_reg[df["NIU"][i]]
                            except KeyError:
                                dic_reg[df["NIU"][i]] = True
        elif "GRC2" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                dic_no_reg = {}
                for df in lista_df:
                    for i in range(len(df)):
                        factura = str(df["ID_Factura"][i]).upper()
                        if factura[0] == "F":
                            try:
                                valor = dic_no_reg[df["NIU"][i]]
                            except KeyError:
                                dic_no_reg[df["NIU"][i]] = True
    dic_df = {"Clasificacion_usuarios":["Regulados","No Regulados"],
                "Cantidad_usuarios_unicos":[len(dic_reg), len(dic_no_reg)]}
    df = pd.DataFrame(dic_df)
    df["Filial"] = dic_filiales[filial]
    df["NIT"] = dic_nit[dic_filiales[filial]]
    df["Mes_reportado"] = mes_reportado
    df["Anio_reportado"] = anio_reportado
    return df, archivo

def reporte_usuarios_unicos_mensual(lista_archivos, informar, seleccionar_reporte, almacenar_excel=True):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df,nombre = apoyo_reporte_usuarios_unicos_mensual(lista_archivos_filial,informar,filial)
            if nombre:
                lista_df_filiales.append(df)
    df_total = pd.concat(lista_df_filiales, ignore_index=True)
    lista_nombre = nombre.split("\\")
    lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
    lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
    nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
    nuevo_nombre = nuevo_nombre.replace("_resumen","_usuarios_unicos")
    df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
    if informar:
        informar_archivo_creado(nuevo_nombre, True)
    df1 = leer_dataframe_utf_8(nuevo_nombre)
    if almacenar_excel:
        almacenar = mod_5.almacenar_csv_en_excel(df1,nuevo_nombre.replace(".csv",".xlsx"),"Datos")
        if informar and almacenar:
            informar_archivo_creado(nuevo_nombre.replace(".csv",".xlsx"), True)
    return df1, nuevo_nombre

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Tarifarios
# * -------------------------------------------------------------------------------------------------------


def lista_porcentaje_df_tarifas(df):
    lista_latitud = []
    lista_longitud = []
    lista_por_perdidas = []
    lista_por_G = []
    lista_por_T = []
    lista_por_D = []
    for fila in range(len(df)):
        try:
            por_perdidas = float(df["P_perdidas"][fila])
            Cuv = float(df["Cuv"][fila])
            G = float(df["G"][fila])
            T = float(df["T"][fila])
            D = float(df["D"][fila])
            latitud = mercado_relevante_resumen[str(df["ID_Mercado"][fila])]["Latitud"]
            longitud = mercado_relevante_resumen[str(df["ID_Mercado"][fila])]["Longitud"]
            if por_perdidas < 0:
                lista_por_perdidas.append("0 %")
            else:
                por_perdidas = ((G+T)/(1-por_perdidas)-G-T)
                lista_por_perdidas.append(str(round((por_perdidas*100)/Cuv,2))+" %")
            lista_por_G.append(str(round((G*100)/Cuv,2))+" %")
            lista_por_T.append(str(round((T*100)/Cuv,2))+" %")
            lista_por_D.append(str(round((D*100)/Cuv,2))+" %")
            lista_latitud.append(latitud)
            lista_longitud.append(longitud)
        except ValueError:
            pass
        except TypeError:
            pass
        except KeyError:
            pass
    if len(df) == len(lista_por_perdidas) == len(lista_por_D) == len(lista_por_G) == len(lista_por_T):
        df["Latitud"] = lista_latitud
        df["Longitud"] = lista_longitud
        df["Porcentaje G"] = lista_por_G
        df["Porcentaje T"] = lista_por_T
        df["Porcentaje D"] = lista_por_D
        df["Porcentaje P_perdidas"] = lista_por_perdidas
    return df

def apoyo_reporte_tarifas_mensual(lista_archivos,informar,filial):
    for archivo in lista_archivos:
        lista_df = lectura_dataframe_chunk(archivo)
        if lista_df:
            for df in lista_df:
                df_filtro = df[(df["Tarifa_1"]>0)|(df["Tarifa_2"]>0)].reset_index(drop=True).copy()
                df_filtro["Filial"] = dic_filiales[filial]
                df_filtro = lista_porcentaje_df_tarifas(df_filtro)
    return df_filtro, archivo

def reporte_tarifas_mensual(lista_archivos, informar, seleccionar_reporte, almacenar_excel=True):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df,nombre = apoyo_reporte_tarifas_mensual(lista_archivos_filial,informar,filial)
            if nombre:
                nombre = nombre.replace("_resumen.csv","_reporte_tarifario.csv")
                df.to_csv(nombre, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(nombre, True)
                df_total = leer_dataframe_utf_8(nombre)
                if almacenar_excel:
                    almacenar = mod_5.almacenar_csv_en_excel(df_total, nombre.replace(".csv",".xlsx"),"Datos")
                    if informar and almacenar:
                        informar_archivo_creado(nombre.replace(".csv",".xlsx"), True)
                lista_df_filiales.append(df)
    if len(lista_df_filiales) and len(lista_filiales_archivo)==4:
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        lista_nombre = nombre.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
        df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nuevo_nombre, True)
        df_total = leer_dataframe_utf_8(nuevo_nombre)
        if almacenar_excel:
            almacenar = mod_5.almacenar_csv_en_excel(df_total, nuevo_nombre.replace(".csv",".xlsx"),"Datos")
            if informar and almacenar:
                informar_archivo_creado(nuevo_nombre.replace(".csv",".xlsx"), True)
        return df_total,nuevo_nombre

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Técnicos
# * -------------------------------------------------------------------------------------------------------

def apoyo_generar_reporte_indicadores_tecnicos_mensual(lista_archivos, informar, filial):
    for archivo in lista_archivos:
        df = leer_dataframe_utf_8(archivo)
        df["Filial"] = dic_filiales[filial]
        df["NIT"] = dic_nit[dic_filiales[filial]]
        df = df[["NIT","Filial","Anio_reportado","Mes_reportado","IPLI","IO","IRST_EG","DES_NER","Suscriptores_DES_NER","Cantidad_eventos_DES_NER"]]
        df["IPLI"] = (df["IPLI"] * 100).round(2)
        df["IO"] = (df["IO"] * 100).round(2)
        df["IRST_EG"] = (df["IRST_EG"] * 100).round(2)
        nuevo_nombre = archivo.replace("_resumen.csv", "_indicador_tecnico.csv")
        return df, nuevo_nombre

def generar_reporte_indicadores_tecnicos_mensual(lista_archivos, seleccionar_reporte, informar,almacenar_excel=True):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df,nombre = apoyo_generar_reporte_indicadores_tecnicos_mensual(lista_archivos_filial,informar,filial)
            if nombre:
                nombre = nombre.replace("_resumen.csv","_reporte_tarifario.csv")
                df.to_csv(nombre, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(nombre, True)
                df_total = leer_dataframe_utf_8(nombre)
                if almacenar_excel:
                    almacenar = mod_5.almacenar_csv_en_excel(df_total, nombre.replace(".csv",".xlsx"),"Datos")
                    if informar and almacenar:
                        informar_archivo_creado(nombre.replace(".csv",".xlsx"), True)
                lista_df_filiales.append(df)
    if len(lista_df_filiales):
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        lista_nombre = nombre.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
        df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nuevo_nombre, True)
        df_total = leer_dataframe_utf_8(nuevo_nombre)
        if almacenar_excel:
            almacenar = mod_5.almacenar_csv_en_excel(df_total, nuevo_nombre.replace(".csv",".xlsx"),"Datos")
            if informar and almacenar:
                informar_archivo_creado(nuevo_nombre.replace(".csv",".xlsx"), True)
        return df_total,nuevo_nombre

def generar_reporte_indicadores_tecnicos_anual(lista_archivos, informar, filial, seleccionar_reporte):
    fecha = seleccionar_reporte["fecha_personalizada"]
    lista_df = []
    df_anual = pd.DataFrame()
    for archivo in lista_archivos:
        if filial in lista_archivos:
            df = leer_dataframe(archivo)
            lista_df.append(df)
            df_anual = pd.concat([df_anual, df], axis=0)
    df_anual["Filial"] = filial
    nombre = lista_archivos[0]
    lista_nombre = nombre.split("\\")
    lista_nombre[-6] = "02. Compilado"
    lista_nombre[-4] = "00. Compilado"
    ext_archivo = lista_nombre[-1].split("_")
    nombre_1 = ext_archivo[:2]
    nombre_1.append(fecha[0][0])
    nombre_1.append(fecha[0][1].upper())
    nombre_1.append(fecha[1][0])
    nombre_1.append(fecha[1][1].upper())
    nombre_1.append("indicador_tecnico.csv")
    lista_nombre[-1] = lista_a_texto(nombre_1,"_",False)
    nombre = lista_a_texto(lista_nombre,"\\",False)
    df_anual.to_csv(nombre, index=False)
    if informar:
        informar_archivo_creado(nombre, True)
    return df_anual, nombre

def generar_reporte_indicadores_tecnicos_anual_total(lista_archivos, informar, seleccionar_reporte):
    df_total = pd.DataFrame()
    for filial in seleccionar_reporte["filial"]:
        df = generar_reporte_indicadores_tecnicos_anual(lista_archivos, False, filial, seleccionar_reporte)
        df_total, nombre = pd.concat([df_total, df], axis=0)
    lista_nombre = nombre.split("\\")
    lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
    nombre_1 = lista_nombre[-1].split("_")
    del nombre_1[1]
    lista_nombre[-1] = lista_a_texto(nombre_1, "_", False)
    nombre = lista_a_texto(lista_nombre,"\\",False)
    df_total.to_csv(nombre, index=False)
    if informar:
        informar_archivo_creado(nombre, True)

def apoyo_generar_reporte_suspension_mensual(lista_archivos,informar,filial):
    for archivo in lista_archivos:
        lista_df = lectura_dataframe_chunk(archivo)
        if lista_df:
            dic_filas = {'ID_Mercado':[], 'Codigo_DANE':[], 'Tipo_gas':[],
                        'Tipo_suspension':[], 'Origen_suspension':[], 'Genero_compensacion':[],
                        'Numero_suscriptores_afectados':[],"Nombre_municipio":[]}
            for df in lista_df:
                filial = dic_filiales[filial]
                anio = df["Anio_reportado"][0]
                mes = df["Mes_reportado"][0]
                df_filtro = df[(df["Tipo_suspension"]==3) & (df["Genero_compensacion"]==1)].reset_index(drop=True).copy()
                lista_codigo_DANE = list(df_filtro["Codigo_DANE"].unique())
                for codigo_DANE in lista_codigo_DANE:
                    df_codigo_DANE = df_filtro[df_filtro["Codigo_DANE"]==codigo_DANE].reset_index(drop=True).copy()
                    for llave in dic_filas:
                        if llave == "Numero_suscriptores_afectados":
                            dic_filas[llave].append(df_codigo_DANE[llave].sum())
                        elif llave == "Nombre_municipio":
                            dic_filas[llave].append(mercado_relevante[str(codigo_DANE)]["Nombre_municipio"])
                        else:
                            dic_filas[llave].append(df_codigo_DANE[llave][0])
                df1 = pd.DataFrame(dic_filas)
                df1["Filial"] = filial
                df1["Anio_reportado"] = anio
                df1["Mes_reportado"] = mes
            return df1, archivo
        else:
            return None, None
    return None, None

def generar_reporte_suspension_mensual(lista_archivos, seleccionar_reporte, informar, almacenar_excel=True):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df,nombre = apoyo_generar_reporte_suspension_mensual(lista_archivos_filial,informar,filial)
            if nombre:
                nombre = nombre.replace("_resumen.csv","_reporte_suspension.csv")
                df.to_csv(nombre, index=False, encoding="utf-8-sig")
                if informar:
                    informar_archivo_creado(nombre, True)
                df_total = leer_dataframe_utf_8(nombre)
                if almacenar_excel:
                    almacenar = mod_5.almacenar_csv_en_excel(df_total, nombre.replace(".csv",".xlsx"),"Datos")
                    if informar and almacenar:
                        informar_archivo_creado(nombre.replace(".csv",".xlsx"), True)
                lista_df_filiales.append(df)
    if len(lista_df_filiales):
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        lista_nombre = nombre.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
        df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nuevo_nombre, True)
        df_total = leer_dataframe_utf_8(nuevo_nombre)
        if almacenar_excel:
            almacenar = mod_5.almacenar_csv_en_excel(df_total, nuevo_nombre.replace(".csv",".xlsx"),"Datos")
            if informar and almacenar:
                informar_archivo_creado(nuevo_nombre.replace(".csv",".xlsx"), True)
        return df_total,nuevo_nombre

# * -------------------------------------------------------------------------------------------------------
# *                                             Uso de listas (arreglos)
# * -------------------------------------------------------------------------------------------------------
def enumerar_lista(lista, cero_incial):
    lista_final = []
    for pos in range(len(lista)):
        if not cero_incial:
            lista_final.append(str(pos)+". "+lista[pos])
        else:
            if pos < 10:
                lista_final.append("0"+str(pos)+". "+lista[pos])
            else:
                lista_final.append(str(pos)+". "+lista[pos])
    return lista_final

def listado_numeros_lista(lista):
    lista_numeros = []
    for pos in range(len(lista)):
        if pos < 10:
            lista_numeros.append("0"+str(pos)+". ")
        else:
            lista_numeros.append(str(pos)+". ")
    return lista_numeros

def union_listas(lista_1, lista_2):
    if len(lista_1) == len(lista_2):
        lista_nueva = []
        for i in range(len(lista_1)):
            lista_nueva.append(lista_1[i]+lista_2[i])
        return lista_nueva
    else:
        return []

def union_listas_numeros(lista):
    lista_numeros = listado_numeros_lista(lista)
    lista_nueva = union_listas(lista_numeros, lista)
    return lista_nueva

def lista_con_elementos_nan(lista):
    for i in lista:
        if math.isnan(i):
            return False
    return True

def elementos_lista_a_str(lista):
    lista = [str(elemento) for elemento in lista]
    return lista

def unir_listas_formato(l1, l2):
    l_final = []
    for i in l1:
        for j in l2:
            l_final.append((i,j))
    return l_final

def mostrar_lista(lista, titulo):
    if titulo:
        print(f"\n{titulo}:\n")
    else:
        print("\n")
    for elemento in lista:
        print(elemento)
    print("\n")

def mostrar_lista_archivos(lista, titulo):
    if titulo:
        print(f"\n{titulo}:\n")
    else:
        print("\n")
    for elemento in lista:
        print(acortar_nombre(elemento))
    print("\n")

def unir_listas_anio_mes(lista_anios, lista_meses):
    lista_anio_mes = []
    for i in lista_meses:
        for j in lista_anios:
            lista_anio_mes.append(f"{j} - {i}")
    return lista_anio_mes

# * -------------------------------------------------------------------------------------------------------
# *                                             Búsqueda archivos
# * -------------------------------------------------------------------------------------------------------
def busqueda_archivos_tipo(ubi_archivo,tipo):
    if tipo:
        archivos_tipo = glob.glob(os.path.join(ubi_archivo, '*'+tipo))
    else:
        archivos_tipo = glob.glob(ubi_archivo)
    return archivos_tipo


def mostrar_texto(texto, tipo):
    linea = 160
    if tipo == "salto":
        print("\n")
    elif tipo == "linea":
        print("-"*linea)
    elif tipo == "texto":
        n = (linea-len(texto))//2
        print(" "*n+" "+texto+" "+" "*n)

def mostrar_titulo(texto, principal, tipo):
    if tipo == "up":
        mostrar_texto("", "linea")
        mostrar_texto(texto, "texto")
    elif tipo == "down":
        mostrar_texto(texto, "texto")
        mostrar_texto("", "linea")
    else:
        if principal:
            mostrar_texto("", "salto")
        mostrar_texto("", "linea")
        mostrar_texto(texto, "texto")
        mostrar_texto("", "linea")
        if principal:
            mostrar_texto("", "salto")