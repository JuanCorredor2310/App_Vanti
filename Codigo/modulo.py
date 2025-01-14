import os
import sys
import time
import json
import zipfile
import glob
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import chardet
import math
import csv
import googlemaps
import shutil
import calendar
import warnings
import unicodedata
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QDialog, QPushButton, QScrollArea
from PyQt5.QtCore import QThread, pyqtSignal
import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos, ruta_guardar_archivos
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
sys.path.append(os.path.abspath(ruta_codigo))
import archivo_csv_a_excel as mod_5
import archivo_df_a_doc as mod_8
import archivo_crear_carpetas as mod_3
import archivo_creacion_json as mod_2
import archivo_busqueda_reportes as mod_4
import archivo_graficas as mod_6
import archivo_slides_dashboard as mod_7
ruta_guardar_archivos = mod_rp.v_guardar_archivos().replace('\\', '\\\\')

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

global lista_meses, lista_empresas, lista_anios, dic_reportes, lista_reportes_generales, reportes_generados, lista_reportes_totales,chunksize,llaves_dic_reporte, dic_carpetas, dic_filiales,antidad_datos_excel, dic_nit, cantidad_datos_estilo_excel,grupo_vanti,mercado_relevante,mercado_relevante_resumen,mercado_relevante_id,tabla_3,tabla_11,fecha_actual,lista_trimestres, dic_meses_abre,lista_clasi_reportes,categoria_matriz_requerimientos,lista_archivo_desviaciones,tabla_2_DS,tabla_3_DS,tabla_4_DS,tabla_5_DS,tabla_6_DS,tabla_8_DS,indicador_SUI,tabla_30,tabla_8_DS_categoria,tabla_71,tabla_16, tabla_3_data,lista_carpetas_extra,anio_actual,dic_ciudades,lista_reportes_generados,trimestre_mes
grupo_vanti = "Grupo Vanti"
dic_carpetas = leer_archivos_json(ruta_constantes+"carpetas.json")
lista_carpetas_extra = leer_archivos_json(ruta_constantes+"carpetas_extra.json")
lista_anios = list(leer_archivos_json(ruta_constantes+"anios.json")["datos"].values())
lista_meses = list(leer_archivos_json(ruta_constantes+"tabla_18.json")["datos"].values())
dic_meses_abre = leer_archivos_json(ruta_constantes+"meses_abre.json")["datos"]
lista_trimestres = list(leer_archivos_json(ruta_constantes+"trimestres.json")["datos"].values())
dic_filiales = leer_archivos_json(ruta_constantes+"tabla_empresa.json")["datos"]
dic_nit = leer_archivos_json(ruta_constantes+"tabla_nit.json")["datos"]
lista_clasi_reportes = leer_archivos_json(ruta_constantes+"carpetas_3.json")["carpeta_7"]
lista_filiales = list(dic_filiales.keys())
dic_reportes = dic_carpetas["carpeta_6"]
lista_reportes_generales = leer_archivos_json(ruta_constantes+"carpetas_1.json")["carpeta_2"]
mercado_relevante = leer_archivos_json(ruta_constantes+"mercado_relevante.json")
mercado_relevante_resumen = leer_archivos_json(ruta_constantes+"mercado_relevante_resumen.json")
mercado_relevante_id = leer_archivos_json(ruta_constantes+"mercado_relevante_id.json")
mercado_relevante_DANE = leer_archivos_json(ruta_constantes+"mercado_relevante_DANE.json")
chunksize = 60000
cantidad_datos_estilo_excel = 65000
cantidad_datos_excel = chunksize
llaves_dic_reporte = ["generales_no_float","generales_float","generales_fecha","generales_hora"]
tabla_3 = leer_archivos_json(ruta_constantes+"tabla_3.json")
tabla_3_data = tabla_3["datos"]
tabla_11 = leer_archivos_json(ruta_constantes+"/tabla_11.json")
tabla_16 = leer_archivos_json(ruta_constantes+"/tabla_16.json")["datos"]
tabla_71 = leer_archivos_json(ruta_constantes+"/tabla_71.json")["datos"]
categoria_matriz_requerimientos = leer_archivos_json(ruta_constantes+"categoria_matriz_requerimientos.json")["datos"]
lista_archivo_desviaciones = ["DS56","DS57","DS58"]
tabla_2_DS = leer_archivos_json(ruta_constantes+"/tabla_2_DS.json")["datos"]
tabla_3_DS = leer_archivos_json(ruta_constantes+"/tabla_3_DS.json")["datos"]
tabla_4_DS = leer_archivos_json(ruta_constantes+"/tabla_4_DS.json")["datos"]
tabla_5_DS = leer_archivos_json(ruta_constantes+"/tabla_5_DS.json")["datos"]
tabla_6_DS = leer_archivos_json(ruta_constantes+"/tabla_6_DS.json")["datos"]
tabla_8_DS = leer_archivos_json(ruta_constantes+"/tabla_8_DS.json")["datos"]
tabla_8_DS_categoria = leer_archivos_json(ruta_constantes+"/tabla_8_DS_categoria.json")["datos"]
tabla_30 = leer_archivos_json(ruta_constantes+"/tabla_30.json")["datos"]
indicador_SUI = leer_archivos_json(ruta_constantes+"/indicador_SUI.json")["datos"]
empresa_indicador_SUI = leer_archivos_json(ruta_constantes+"/empresa_indicador_SUI.json")["datos"]
dic_ciudades = leer_archivos_json(ruta_constantes+"ciudades_tarifas.json")["datos"]
trimestre_mes = mod_2.leer_archivos_json(ruta_constantes+"trimestre_mes.json")["datos"]
fecha_actual = datetime.now()
anio_actual = fecha_actual.year
fecha_actual_texto = f"{fecha_actual.day} de {lista_meses[int(fecha_actual.month)-1]} del {anio_actual}"
dia_corte, mes_corte, anio_corte = ((datetime.now() - relativedelta(months=2) + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)).day, ((datetime.now() - relativedelta(months=2) + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)).month, ((datetime.now() - relativedelta(months=2) + relativedelta(months=1)).replace(day=1) - relativedelta(days=1)).year
fecha_corte_tupla = (dia_corte,mes_corte,anio_corte)
dia_corte, mes_corte, anio_corte = (fecha_actual.replace(month=1, day=1) - relativedelta(days=1)).day, (fecha_actual.replace(month=1, day=1) - relativedelta(days=1)).month, (fecha_actual.replace(month=1, day=1) - relativedelta(days=1)).year
fecha_anio_anterior_tupla = (dia_corte,mes_corte,anio_corte)
def crear_lista_reportes_totales():
    dic = leer_archivos_json(ruta_constantes+"reportes_disponibles.json")["datos"]
    lista = []
    for i in dic:
        lista.extend(dic[i])
    return lista
lista_reportes_totales = crear_lista_reportes_totales()
fecha_actual = datetime.now()
anio_actual = fecha_actual.year
lista_reportes_generados = ["_resumen","_form_estandar", #formatos generales
                            "_reporte_consumo","_CLD","_PRD","_porcentaje_comparacion_SAP","_total_comparacion_SAP","SH","DANE","_reporte_DANE","_compilado_desviaciones","_compilado_DS_metricas","SAP",
                            "_comparacion_iguales","_comparacion_diferentes","_subsidio","_info_comercial","_reporte_compensacion","_compilado_compensacion", #formatos comerciales
                            "_reporte_tarifario", #formatos tarifarios
                            "_indicador_tecnico","_reporte_suspension","_indicador_tecnico_IRST","_indicador_tecnico_IRST_minutos","_indicador_tecnico_IRST_horas", #formatos tecnicos
                            "_inventario_suscriptores","_usuarios_unicos","_reporte_facturacion",#calidad de la información
                            "porcentaje_cumplimientos_regulatorios",
                            "_error","_nuevo","_completo","_procesado"] #formatos regulatorios
global val_res
val_res = 0.6

# * -------------------------------------------------------------------------------------------------------
# *                                             Uso de librería Geopy
# * -------------------------------------------------------------------------------------------------------
def encontrar_coordenadas(municipio):
    gmaps = googlemaps.Client(key="AIzaSyARSFO5ues9twiOidNkaH6ML3MCjfRLXtg")
    geocode_result = gmaps.geocode(municipio)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return location
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

def fecha_anterior(anio, mes):
    pos_mes = lista_meses.index(mes.capitalize())
    if pos_mes == 0:
        return str(int(anio)-1), lista_meses[-1]
    else:
        return str(anio), lista_meses[pos_mes-1]

def fecha_siguiente(anio, mes):
    pos_mes = lista_meses.index(mes.capitalize())
    if pos_mes == len(lista_meses)-1:
        return str(int(anio)+1), lista_meses[0]
    else:
        return str(anio), lista_meses[pos_mes+1]

def ultimos_12_meses(anio, mes):
    meses = []
    fecha = datetime(anio, mes, 1)
    for _ in range(12):
        meses.append((fecha.year, fecha.month))
        fecha = fecha.replace(day=1) - timedelta(days=1)
    return meses

def meses_anio_actual(anio, mes):
    meses = [(anio, i) for i in range(1, mes + 1)]
    return meses

def agregar_meses_anteriores(seleccionar_reporte):
    if seleccionar_reporte["meses"]:
        mes = seleccionar_reporte["meses"][0]
        seleccionar_reporte["meses"] = None
        anio = seleccionar_reporte["anios"][0]
        seleccionar_reporte["anios"] = None
        seleccionar_reporte["fecha_personalizada"] = [fecha_anterior_rango(anio, mes),(anio,mes)]
    elif seleccionar_reporte["fecha_personalizada"]:
        anio = seleccionar_reporte["fecha_personalizada"][0][0]
        mes = seleccionar_reporte["fecha_personalizada"][0][1]
        seleccionar_reporte["fecha_personalizada"][0] = fecha_anterior_rango(anio, mes)
    return seleccionar_reporte

# * -------------------------------------------------------------------------------------------------------
# *                                             Manejo DataFrames
# * -------------------------------------------------------------------------------------------------------
def leer_dataframe(archivo):
    encoding_1 = elegir_codificacion(archivo)
    df = pd.read_csv(archivo, encoding=encoding_1)
    return df

def leer_dataframe_utf_8(archivo):
    try:
        df = pd.read_csv(archivo, encoding="utf-8-sig").reset_index(drop=True)
    except Exception:
        df = pd.DataFrame()
    return df

def elegir_codificacion(archivo):
    with open(archivo, 'rb') as file:
        raw_data = file.read(8000)
        result = chardet.detect(raw_data)
        encoding_1 = result['encoding']
    return encoding_1

def normalizar_texto(texto):
    if isinstance(texto, str):
        texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
        texto = texto.replace('ñ', 'n').replace('Ñ', 'N').replace("_",'')
    return texto

def eliminar_caracteres_especiales(df):
    regex = r"[^\w\s]"
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].dtype.name == 'string':
            df[col] = df[col].str.replace(regex, "", regex=True)
            df[col] = df[col].apply(normalizar_texto)
    return df

def lectura_dataframe_chunk(archivo, valor_chunksize=chunksize,separador=","):
    lista_codificaciones = []
    lista_codificaciones.append(elegir_codificacion(archivo))
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','ansi','utf-16','utf-16-be','utf-32','ascii',
                                'windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
                                'shift-jis','euc-jp','mac_roman','utf-7','cp437','cp850','ibm866','tis-620',
                                "utf-8-sig","utf-8","iso-8859-1","latin-1","utf-16","utf-16-be","utf-32","ascii",
                                "windows-1252","iso-8859-2","iso-8859-5","koi8-r","big5","gb2312","shift-jis","euc-jp",
                                "mac_roman","utf-7","cp437","cp850","ibm866","tis-620","utf-16-le","utf-32-be","utf-32-le",
                                "iso-8859-3","iso-8859-4","iso-8859-6","iso-8859-7","iso-8859-8","iso-8859-9","iso-8859-10",
                                "iso-8859-13","iso-8859-14","iso-8859-15","cp737","cp775","cp852","cp855","cp857","cp858","cp860",
                                "cp861","cp862","cp863","cp864","cp865","cp866","cp869"])
    for sep in [separador, ";"]:
        for elemento in lista_codificaciones:
            try:
                lista_df = []
                for i, chunk in enumerate(pd.read_csv(archivo, chunksize=valor_chunksize, encoding=elemento, sep=separador,low_memory=False)):
                    chunk = eliminar_caracteres_especiales(chunk)
                    lista_df.append(chunk.reset_index(drop=True).copy())
                return lista_df
            except Exception:
                pass
            except BaseException:
                pass
    return None

def lectura_dataframe_chunk_prueba(archivo, valor_chunksize=8000,separador=","):
    lista_codificaciones = [elegir_codificacion(archivo)]
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','ansi','utf-16','utf-16-be','utf-32','ascii',
                                'windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
                                'shift-jis','euc-jp','mac_roman','utf-7','cp437','cp850','ibm866','tis-620',
                                "utf-8-sig","utf-8","iso-8859-1","latin-1","utf-16","utf-16-be","utf-32","ascii",
                                "windows-1252","iso-8859-2","iso-8859-5","koi8-r","big5","gb2312","shift-jis","euc-jp",
                                "mac_roman","utf-7","cp437","cp850","ibm866","tis-620","utf-16-le","utf-32-be","utf-32-le",
                                "iso-8859-3","iso-8859-4","iso-8859-6","iso-8859-7","iso-8859-8","iso-8859-9","iso-8859-10",
                                "iso-8859-13","iso-8859-14","iso-8859-15","cp737","cp775","cp852","cp855","cp857","cp858","cp860",
                                "cp861","cp862","cp863","cp864","cp865","cp866","cp869"])
    for v_sep in [separador, ";"]:
        for elemento in lista_codificaciones:
            try:
                for i, chunk in enumerate(pd.read_csv(archivo, chunksize=valor_chunksize, encoding=elemento, sep=v_sep,low_memory=False)):
                    df_prueba = chunk.reset_index(drop=True).copy()
                    return True
            except Exception:
                pass
            except BaseException:
                pass
    return False

def generar_suma_df_filiales(df, lista_total, lista_suma):
    df = df.reset_index(drop=True)
    columnas = list(df.columns)
    lista_df = []
    lista_filiales = list(df["Filial"].unique())
    for filial in lista_filiales:
        df_filial = df[df["Filial"]==filial].reset_index(drop=True).copy()
        lista_fila = []
        for columna in columnas:
            if columna in lista_total:
                lista_fila.append("Total")
            elif columna in lista_suma:
                lista_fila.append(df_filial[columna].sum())
            else:
                lista_fila.append(df_filial[columna][0])
        df_filial.loc[len(df_filial)] = lista_fila
        lista_df.append(df_filial)
    if not len(lista_df):
        return df
    df_final = pd.concat(lista_df, ignore_index=True)
    lista_fila = []
    df_suma = df_final[df_final[lista_total[0]]=="Total"]
    for columna in columnas:
        if columna in ["Filial","NIT"]:
            lista_fila.append(grupo_vanti)
        elif columna in lista_total:
            lista_fila.append("Total")
        elif columna in lista_suma:
            lista_fila.append(df_suma[columna].sum())
        else:
            lista_fila.append(df_final[columna][0])
    df_final.loc[len(df_final)] = lista_fila
    return df_final

# * -------------------------------------------------------------------------------------------------------
# *                                             Tiempo de procesamiento
# * -------------------------------------------------------------------------------------------------------
def mostrar_tiempo(t_f, t_i):
    tiempo = t_f-t_i
    if tiempo > 60:
        minutos = round(tiempo//60)
        segundos = round(tiempo%60,4)
        texto = f"t: {minutos} min, {segundos} seg"
    else:
        texto = f"t: {round(tiempo, 3) } seg"
    return texto

# * -------------------------------------------------------------------------------------------------------
# *                                             Edición de textos
# * -------------------------------------------------------------------------------------------------------

def lista_a_texto(lista, separador, salto=False):
    lista = [str(elemento) for elemento in lista]
    texto = separador.join(lista)
    if salto:
        texto += "\n"
    return texto

# * -------------------------------------------------------------------------------------------------------
# *                                             Edición reportes
# * -------------------------------------------------------------------------------------------------------

def v_listas_iguales(lista_1, lista_2):
    if len(lista_1) == len(lista_2):
        for i in lista_1:
            if i not in lista_2:
                return False
        return True
    else:
        return False

def editar_json_reporte(reporte):
    archivo = ruta_constantes+reporte+".xlsx"
    lista_hojas = ["generales", "generales_no_float", "generales_float", "generales_hora", "generales_fecha", "seleccionados"]
    if os.path.exists(archivo):
        v_hojas = mod_5.hojas_disponibles(archivo)
        dic_xlsx_json = {}
        if v_listas_iguales(lista_hojas, v_hojas):
            for hoja in lista_hojas:
                df,valor = mod_5.lectura_hoja_xlsx(archivo, hoja)
                if not valor:
                    return "error", f"Revisar el archivo {archivo}"
                dic_xlsx_json[hoja] = df
            v_convertir_dic_json = convertir_dic_json(dic_xlsx_json)
            archivo_json = archivo.replace(".xlsx",".json").replace("_json","")
            almacenar_json(v_convertir_dic_json, archivo_json)
            return "complete", f"Archivo {archivo_json} creado"
        else:
            return "no_complete", lista_hojas
    else:
        return "no_exist", archivo

def agregar_json_reporte(clasificacion, reporte):
    op, valor = editar_json_reporte(reporte)
    if op == "complete":
        cambiar_diccionario(clasificacion, reporte)
    return op, valor

def cambiar_diccionario(clasificacion, reporte):
        ruta = ruta_constantes+"reportes_disponibles.txt"
        texto = f"{clasificacion},{reporte}"
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                    lineas = archivo.readlines()
            lineas = [str(linea.strip()) for linea in lineas]
            if texto not in lineas:
                    lineas.append(texto)
            with open(ruta, 'w', encoding='utf-8') as archivo:
                    for linea in lineas:
                            archivo.write(linea + '\n')
        except IOError:
                pass

def convertir_dic_json(dic_xlsx_json):
    dic_json = {}
    for key, value in dic_xlsx_json.items():
        if key == "generales":
            valor = list(value["nombre_formato"])
            dic_json[key] = dict(zip(valor, list(value["nombre_no_formato"])))
        else:
            if len(value[key]):
                dic_json[key] = list(value[key])
            else:
                dic_json[key] = []
    dic_json["cantidad_columnas"] = len(dic_xlsx_json["generales_float"])+len(dic_xlsx_json["generales_no_float"])+len(dic_xlsx_json["generales_hora"])+len(dic_xlsx_json["generales_fecha"])
    return dic_json

def almacenar_json(diccionario, nombre_archivo):
        with open(nombre_archivo, 'w') as file:
                json.dump(diccionario, file, indent=4)

"""
generales_carga = ["NIU","Fecha_medicion","Hora_medicion","Tipo_gas","Presion_medida","Metodo","Sustancia_odorante",
                                "Nivel_concentracion_minimo","Nivel_concentracion_medido","Observaciones"]
                generales_presentacion = ["NIU","Fecha de medición","Hora de medición","Tipo de Gas","Presion Medida (mbar)","Método","Sustancia Odorante",
                                        "Nivel de Concentración Mínimo","Nivel de Concentración Medido ( mg/m³ )","Observaciones"]
                seleccionados = ["NIU","Fecha_medicion","Hora_medicion","Tipo_gas","Metodo","Sustancia_odorante",
                                "Observaciones"]
                generales_no_float = ["NIU","Tipo_gas","Metodo","Sustancia_odorante","Observaciones"]
                generales_float = ["Presion_medida","Nivel_concentracion_minimo","Nivel_concentracion_medido"]
                generales_hora = ["Hora_medicion"]
                generales_fecha = ["Fecha_medicion"]
                seleccionados = ["NIU","Fecha_medicion","Hora_medicion","Tipo_gas","Metodo","Sustancia_odorante",
                                "Observaciones","Presion_medida","Nivel_concentracion_minimo","Nivel_concentracion_medido"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
"""

# * -------------------------------------------------------------------------------------------------------
# *                                             Creación de carpetas
# * -------------------------------------------------------------------------------------------------------

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

def crear_carpeta(elemento):
    os.makedirs(elemento, exist_ok=True)

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

def crear_carpeta_anual(fecha, lista_archivo, thread=None):
    lista_archivo = lista_archivo[:-2]
    lista_archivo.append(fecha)
    nombre = lista_a_texto(lista_archivo, "\\")
    crear_carpeta(nombre)
    if not os.path.exists(nombre):
        if thread:
            thread.message_sent.emit(f"Se creó la carpeta {acortar_nombre(nombre)}\n", "white")
        else:
            print(f"\nSe creó la carpeta {acortar_nombre(nombre)}\n")
    lista_clasi = []
    lista_copia = lista_clasi_reportes.copy()
    lista_copia.append("Dashboard")
    for clasi in union_listas_numeros(lista_copia):
        lista_temp = lista_archivo.copy()
        lista_temp.append(clasi)
        lista_clasi.append(lista_temp)
        crear_carpeta(lista_a_texto(lista_temp, "\\"))
    for i in lista_clasi:
        lista_temp = i.copy()
        lista_temp.append("Imagenes")
        crear_carpeta(lista_a_texto(lista_temp, "\\"))

# * -------------------------------------------------------------------------------------------------------
# *                                             Edición de archivos
# * -------------------------------------------------------------------------------------------------------

def encontrar_codificacion(archivo):
    lista_codificaciones = []
    lista_codificaciones.append(elegir_codificacion(archivo))
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','utf-16','utf-16-be','utf-32','ascii','windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
                                    'shift-jis','euc-jp','mac_roman','utf-7','cp437','cp850','ibm866','tis-620'])
    for elemento in lista_codificaciones:
        try:
            with open(archivo, 'r', encoding=elemento) as file:
                sample = file.read(5000)
                dialect = csv.Sniffer().sniff(sample)
                return dialect
        except UnicodeDecodeError:
            pass
        except UnicodeError:
            pass
        except csv.Error:
            pass
    return None

def encontrar_codificacion_2(archivo):
    lista_codificaciones = []
    lista_codificaciones.append(elegir_codificacion(archivo))
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','utf-16','utf-16-be','utf-32','ascii','windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
                                    'shift-jis','euc-jp','mac_roman','utf-7','cp437','cp850','ibm866','tis-620'])
    for elemento in lista_codificaciones:
        try:
            with open(archivo, 'r', encoding=elemento) as file:
                sample = file.read(5000)
                dialect = csv.Sniffer().sniff(sample)
                return elemento
        except UnicodeDecodeError:
            pass
        except UnicodeError:
            pass
        except csv.Error:
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
        else:
            return None
    else:
        lista_df = lectura_dataframe_chunk(ruta, separador=",")
        if lista_df:
            df = pd.concat(lista_df, ignore_index=True)
            df.to_csv(ruta.replace(ext_original,ext_final), index=False, sep=',', encoding="utf-8-sig")
            return ruta.replace(ext_original,ext_final)
        else:
            return None

def eliminar_archivos(lista):
    for elemento in lista:
        if os.path.exists(elemento):
            os.remove(elemento)

def buscar_formato(archivo):
    lista_archivo = archivo.split("\\")
    if "_form_estandar" in lista_archivo[-1]:
        return True
    else:
        return False

def conversion_archivos_lista(lista_archivos, ext_original, ext_final, informar=False, lista_fallidos=[], thread=None):
    for archivo in lista_archivos:
        op = conversion_archivos(archivo, ext_original, ext_final)
        if op:
            if informar:
                informar_archivo_creado(archivo.replace(ext_original, ext_final), informar, thread=thread)
        else:
            lista_fallidos.append(archivo)
    return lista_fallidos

def conversion_archivos(archivo, ext_original, ext_final):
    if ext_original in archivo:
        archivo = cambio_archivo(archivo, ext_original, ext_final)
        if archivo:
            return True
        else:
            return False
    return True

def cambiar_formato_dataframe(df, dic_reporte):
    df.columns = list(dic_reporte["generales"].keys())
    return df

def acortar_nombre(nombre, cantidad=6):
    lista_nombre = nombre.split("\\")
    largo = len(lista_nombre)
    if largo > cantidad:
        texto = ("...\\"+lista_a_texto(lista_nombre[largo-cantidad:], "\\", False)).replace("\\\\","\\")
    else:
        texto = texto.replace("\\\\","\\")
    return texto

def informar_archivo_creado(nombre,valor,thread=None):
    texto = acortar_nombre(nombre)
    if valor:
        if thread:
            thread.message_sent.emit(f"\nArchivo {texto} creado\n", "white")
        else:
            print(f"\nArchivo {texto} creado\n")

def modificar_csv(input_file, output_file):
    codificacion = encontrar_codificacion_2(input_file)
    if codificacion:
        with open(input_file, 'r', newline='', encoding=codificacion) as infile:
            reader = csv.reader(infile)
            rows = []
            for row in reader:
                modified_row = []
                for cell in row:
                    modified_cell = cell.replace(',', '.').replace(';', ',')
                    modified_row.append(modified_cell)
                rows.append(modified_row)
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)


def estandarizacion_archivos(lista_archivos, informar, thread=None):
    dic_reporte = None
    for archivo in lista_archivos:
        exitoso = True
        conversion_archivos(archivo, ".csv", ".csv")
        dic_reporte = buscar_reporte(archivo)
        if dic_reporte:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                for i in range(len(lista_df)):
                    df = lista_df[i].copy()
                    if len(list(df.columns)) == dic_reporte["cantidad_columnas"]:
                        df = cambiar_formato_dataframe(df, dic_reporte)
                        lista_df[i] = df
                    else:
                        exitoso = False
                df = pd.concat(lista_df, ignore_index=True)
                nuevo_nombre = archivo.replace(".csv", "_form_estandar.csv")
                if exitoso:
                    almacenar_df_csv_y_excel(df, nuevo_nombre, almacenar_excel=False, thread=thread)
                else:
                    v_nombre_archivo_json_reporte = nombre_archivo_json_reporte(archivo)
                    if thread:
                        thread.message_sent.emit(f"El archivo {acortar_nombre(archivo,3)} no cumple con las columnas del archivo {acortar_nombre(v_nombre_archivo_json_reporte,3)}", "red")
                        thread.message_sent.emit(f"Revisar el archivo {acortar_nombre(archivo)}", "red")
                    else:
                        print(f"\nEl archivo {acortar_nombre(archivo,3)} no cumple con las columnas del archivo {acortar_nombre(v_nombre_archivo_json_reporte,3)}")
                        print(f"Revisar el archivo {acortar_nombre(archivo)}\n")

def cambiar_formato_dataframe_resumen(df, dic_reporte):
    df = df[dic_reporte["seleccionados"]]
    return df

def nombre_archivo_json_reporte(archivo):
    lista_archivo = archivo.split("\\")
    for reporte in lista_reportes_totales:
        if reporte in lista_archivo[-1]:
            return ruta_constantes+f"/{reporte.upper()}.json"
    return None

def buscar_reporte(archivo):
    v_nombre_archivo_json_reporte = nombre_archivo_json_reporte(archivo)
    if v_nombre_archivo_json_reporte:
        dic_reporte = leer_archivos_json(v_nombre_archivo_json_reporte)
        return dic_reporte
    return None

def archivos_resumen(lista_archivos, informar, thread=None):
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
                        informar_archivo_creado(nuevo_nombre, True, thread=thread)

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

def evaluar_archivos_prueba(lista_archivos, lista_fallidos):
    for archivo in lista_archivos:
        op = lectura_dataframe_chunk_prueba(archivo)
        if not op:
            lista_fallidos.append(archivo)
    return lista_fallidos

def retirar_archivos_fallidos(lista_archivos, lista_fallidos, thread=None):
    lista_archivos_final = []
    for archivo in lista_archivos:
        if archivo not in lista_fallidos:
            lista_archivos_final.append(archivo)
        else:
            if thread:
                thread.message_sent.emit(f"nArchivo {acortar_nombre(archivo)} posee errores en la lectura de información. Revisar el archivo", "red")
            else:
                print(f"\nArchivo {acortar_nombre(archivo)} posee errores en la lectura de información. Revisar el archivo\n")
    return lista_archivos_final

def cantidad_minima_info_archivo(lista_archivos):
    lista_archivos_info_min = []
    for archivo in lista_archivos:
        elemento = archivo.split("\\")[-1].replace(" ","_")
        for i in range(9):
            j = 10-i
            elemento = elemento.replace("_"*j, "_")
        if len(elemento.split("_")) >= 4:
            lista_archivos_info_min.append(archivo)
    return lista_archivos_info_min

def anio_abreviado(ext_archivo, i, lista_anios):
    for anio in lista_anios:
        if ext_archivo[i] == anio[-2:]:
            ext_archivo[i] = anio
            return ext_archivo
    return ext_archivo

def comprobar_info_nombre_archivo(ext_archivo):
    for i in range(0, 4):
        if i == 1:
            if ext_archivo[i] not in lista_filiales:
                return False
        elif i == 2:
            if ext_archivo[i] not in lista_anios:
                return False
        elif i == 3:
            if ext_archivo[i].lower().capitalize() not in lista_meses:
                return False
    return True

def archivos_aceptados_constantes(lista_archivos, informar=True, thread=None):
    try:
        with open(ruta_constantes+"Aceptados.txt", 'r') as archivo:
            lineas = archivo.readlines()
        proceso = True
    except FileNotFoundError:
        pass
    except PermissionError:
        pass
    if proceso:
        lista_archivos_aceptados = [linea.strip() for linea in lineas][1:]
        for archivo in lista_archivos:
            nombre_archivo = archivo.split("\\")[-1]
            if nombre_archivo in lista_archivos_aceptados:
                try:
                    shutil.move(archivo, ruta_constantes+"\\"+nombre_archivo)
                    if informar:
                        informar_archivo_creado(ruta_constantes+"\\"+nombre_archivo, informar, thread=thread)
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass

def archivos_tipo_csv_txt(lista_archivos):
    lista_nueva = []
    for archivo in lista_archivos:
        if archivo.endswith((".csv", ".txt",".TXT",".CSV")):
            lista_nueva.append(archivo)
    return lista_nueva

def formato_ext_archivo(ext_archivo, texto=False):
    ext_archivo = anio_abreviado(ext_archivo, 2, lista_anios)
    if ext_archivo[3].upper() in dic_meses_abre:
        ext_archivo[3] = dic_meses_abre[ext_archivo[3].upper()].upper()
    if texto:
        ext_archivo = lista_a_texto(ext_archivo, "_")
    return ext_archivo

def almacenar_archivos(ruta_guardar_archivos,informar):
    archivos_aceptados_constantes(busqueda_archivos_tipo(ruta_guardar_archivos))
    lista_archivos = busqueda_archivos_tipo(ruta_guardar_archivos)
    lista_archivos = archivos_tipo_csv_txt(lista_archivos)
    lista_carpetas = buscar_carpetas(ruta_nuevo_sui)
    ubi = None
    for i in lista_carpetas:
        if dic_carpetas["carpeta_2"][0] in i:
            ubi = i
    lista_fallidos = []
    lista_fallidos = conversion_archivos_CSV(lista_archivos, lista_fallidos=lista_fallidos)
    lista_fallidos = conversion_archivos_lista(lista_archivos,"TXT","txt",informar=True, lista_fallidos=lista_fallidos)
    lista_fallidos = conversion_archivos_lista(lista_archivos,"txt","csv",informar=True, lista_fallidos=lista_fallidos)
    lista_fallidos = evaluar_archivos_prueba(lista_archivos, lista_fallidos=lista_fallidos)
    lista_fallidos = list(set(lista_fallidos))
    lista_archivos = busqueda_archivos_tipo(ruta_guardar_archivos, lista_fallidos=lista_fallidos)
    lista_archivos = retirar_archivos_fallidos(lista_archivos, lista_fallidos)
    lista_archivos = cantidad_minima_info_archivo(lista_archivos)
    for archivo in lista_archivos:
        bool_DS = False
        bool_GRTT2SAP = False
        try:
            nombre_archivo = archivo.split("\\")[-1].replace(" ","_")
            for i in range(9):
                j = 10-i
                nombre_archivo = nombre_archivo.replace("_"*j, "_")
            nombre_archivo_lista = nombre_archivo.split(".")
            nombre_archivo_lista[0] = nombre_archivo_lista[0].upper()
            lista_nombre_aux = nombre_archivo_lista[0].split("_")
            nombre_archivo_lista[0] = formato_ext_archivo(lista_nombre_aux, texto=True)
            nombre_archivo = lista_a_texto(nombre_archivo_lista, ".")
            ext_archivo = nombre_archivo.split("_")
            ext_archivo[-1] = ext_archivo[-1].split(".")[0]
            ext_archivo = formato_ext_archivo(ext_archivo)
            tipo = ext_archivo[0]
            if tipo == "GRTT2SAP":
                tipo = "GRTT2"
                bool_GRTT2SAP = True
            elif tipo in lista_archivo_desviaciones:
                tipo = "DS"
                ext_archivo[4] = ext_archivo[4].upper()
                bool_DS = True
            categoria = encontrar_categoria_reporte(tipo)
            ext_archivo[3] = ext_archivo[3].lower().capitalize()
            ext_archivo.append(categoria)
            if None not in ext_archivo:
                if comprobar_info_nombre_archivo(ext_archivo):
                    ubi_1 = encontrar_nueva_ubi_archivo(ubi, ext_archivo)
                    nueva_ubi = ubi_1+"\\"+nombre_archivo
                    if bool_GRTT2SAP:
                        lista_nueva_ubi = nueva_ubi.split("\\")
                        valor = lista_nueva_ubi[-1]
                        lista_nueva_ubi[-1] = "00. GRTT2"
                        lista_nueva_ubi.append(valor)
                        nueva_ubi = lista_a_texto(lista_nueva_ubi, "\\")
                    if bool_DS:
                        lista_nueva_ubi = nueva_ubi.split("\\")
                        valor = lista_nueva_ubi[-1]
                        lista_nueva_ubi[-1] = "11. DS"
                        lista_nueva_ubi.append(valor)
                        nueva_ubi = lista_a_texto(lista_nueva_ubi, "\\")
                    shutil.move(archivo, nueva_ubi)
                    if informar:
                        informar_archivo_creado(nueva_ubi, informar)
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
        except BaseException:
            pass

def conversion_archivos_CSV(lista_archivos, lista_fallidos=[]):
    for archivo in lista_archivos:
        if ".CSV" in archivo:
            try:
                os.rename(archivo, archivo.replace(".CSV",".csv"))
            except OSError:
                lista_fallidos.append(archivo)
    return lista_fallidos

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

def fun_tamanio_archivos(archivo):
    file_size_bytes = os.path.getsize(archivo)
    return file_size_bytes

def tamanio_archivos(lista_archivos):
    suma = 0
    for archivo in lista_archivos:
        file_size_bytes = fun_tamanio_archivos(archivo)
        suma += float(round(file_size_bytes/(1024*1024),2))
    texto = f"{round(suma,2)} MB"
    return texto

def almacenar_2_archivos(lista_archivos):
    conteo = 0
    for archivo in lista_archivos:
        if archivo.endswith((".csv")):
            conteo += 1
        if conteo >= 2:
            return True
    else:
        return False

def comprimir_archivos_aux(seleccionar_reporte, evitar_extra=["_CLD","_PRD"], thread=None):
    lista_archivos_comprimir = []
    tipo = ".csv"
    proceso, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte,evitar_extra, informar=False)
    if proceso:
        lista_archivos_comprimir.extend(lista_archivos)
    tipo = "_form_estandar.csv"
    proceso, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte,evitar_extra, informar=False)
    if proceso:
        lista_archivos_comprimir.extend(lista_archivos)
    tipo = ".txt"
    proceso, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte,evitar_extra, informar=False)
    if proceso:
        lista_archivos_comprimir.extend(lista_archivos)
    if len(lista_archivos_comprimir):
        comprimir_archivos(lista_archivos_comprimir, thread=thread)

def comprimir_archivos(lista_archivos, informar=True, thread=None):
    diccionario_archivos = {}
    for archivo in lista_archivos:
        lista_archivo = archivo.split("\\")
        nombre_carpeta = lista_a_texto(lista_archivo[-1].replace(".txt","").replace(".csv","").replace(".txt".upper(),"").replace(".csv".upper(),"").split("_")[:4],"_")+".zip"
        lista_archivo[-1] = nombre_carpeta
        ubi_carpeta_zip = lista_a_texto(lista_archivo, "\\")
        if nombre_carpeta not in diccionario_archivos:
            diccionario_archivos[nombre_carpeta] = ([],ubi_carpeta_zip)
        diccionario_archivos[nombre_carpeta][0].append(archivo)
    for llave,tupla in diccionario_archivos.items():
        if almacenar_2_archivos(tupla[0]):
            with zipfile.ZipFile(tupla[1], 'w') as zipf:
                v_tamanio_archivos = tamanio_archivos(tupla[0])
                for file in tupla[0]:
                    zipf.write(file, os.path.basename(file))
                if informar:
                    if thread:
                        thread.message_sent.emit(f"Se recomienda almacenar la carpeta {llave} en un ubicación externa. \nLos archivos de la carpeta comprimida pesan {v_tamanio_archivos}", "orange")
                    else:
                        print(f"\nSe recomienda almacenar la carpeta {llave} en un ubicación externa. \nLos archivos de la carpeta comprimida pesan {v_tamanio_archivos}\n")
                eliminar_archivos(tupla[0])

def almacenar_df_csv_y_excel(df, nombre, informar=True, almacenar_excel=True, reporte_DANE=False, BOM=True, thread=None):
    if BOM:
        df.to_csv(nombre, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(nombre, index=False, encoding="utf-8")
    if informar:
        informar_archivo_creado(nombre, True, thread=thread)
    if almacenar_excel:
        df = leer_dataframe_utf_8(nombre)
        almacenar = mod_5.almacenar_csv_en_excel(df, nombre.replace(".csv",".xlsx"),"Datos", reporte_DANE=reporte_DANE)
        if informar and almacenar:
            informar_archivo_creado(nombre.replace(".csv",".xlsx"), True, thread=thread)

def generar_formato_almacenamiento_reportes(lista_df, nombre, informar=True,almacenar_excel=True,thread=None):
    df_total = pd.concat(lista_df, ignore_index=True)
    lista_nombre = nombre.split("\\")
    lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
    lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
    lista_nombre.pop(-2)
    nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
    almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel,thread=thread)
    return lista_df, nombre

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Comerciales
# * -------------------------------------------------------------------------------------------------------

def codigo_DANE_texto(codigo_DANE):
    if len(codigo_DANE) == 1:
        return str(codigo_DANE[0])[:5]
    elif len(codigo_DANE) > 1:
        lista_texto_codigo_DANE = []
        for elemento in codigo_DANE:
            lista_texto_codigo_DANE.append(int(str(elemento)[:5]))
        lista_texto_codigo_DANE.sort()
        lista_texto_codigo_DANE_str = [str(x) for x in lista_texto_codigo_DANE]
        return lista_a_texto(lista_texto_codigo_DANE_str,"_")
    else:
        return ""

def apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos, codigo_DANE, reporte, filial, valor_facturado=False, total=False, subsidio=False, facturas=False, reporte_DANE=False):
    for archivo in lista_archivos:
        if reporte in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                dic = {"Cantidad de usuarios":0,"Consumo m3":0,"Valor total facturado":0, "Valor consumo facturado":0,
                        "Cantidad de facturas":0, "Subsidios":0, "Contribuciones":0}
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                dic_dataframe = {}
                dic_codigo_DANE = {}
                if codigo_DANE:
                    for i in range(len(lista_df)):
                        df = lista_df[i].copy()
                        for ele_codigo_DANE in codigo_DANE:
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore", category=FutureWarning)
                                df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['Codigo_DANE'])
                            df["Codigo_DANE"] = df["Codigo_DANE"].astype(int)
                            df_codigo_DANE = df[df["Codigo_DANE"] == ele_codigo_DANE].reset_index(drop=True)
                            if len(df_codigo_DANE):
                                if ele_codigo_DANE not in dic_codigo_DANE:
                                    dic_codigo_DANE[ele_codigo_DANE] = {}
                                lista_sectores = list(df_codigo_DANE["Sector_consumo"].unique())
                                for sector in lista_sectores:
                                    try:
                                        s1 = int(sector)
                                        if s1 > 0:
                                            df_sector = df_codigo_DANE[df_codigo_DANE["Sector_consumo"] == s1].reset_index(drop=True).copy()
                                            if len(df_sector):
                                                if s1 not in dic_codigo_DANE[ele_codigo_DANE]:
                                                    dic_codigo_DANE[ele_codigo_DANE][s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                                df_sector.loc[:, 'Composicion_usuario'] = (
                                                    df_sector['ID_Factura'].astype(str) + '_' +
                                                    df_sector['Concepto_general_factura'].astype(str) + '_' +
                                                    df_sector['Sector_consumo'].astype(str))
                                                df_sector.loc[:, 'ID_Factura'] = df_sector['ID_Factura'].str.upper()
                                                df_facturas = df_sector[df_sector['ID_Factura'].str.startswith('F')]
                                                cantidad_facturas = len(df_facturas)
                                                cantidad_usuario = len(list(df_sector['Composicion_usuario'].unique()))
                                                volumen = df_sector["Volumen"].sum()
                                                valor_total_facturado = df_sector["Valor_total_facturado"].sum()
                                                valor_consumo_facturado = df_sector["Facturacion_por_suministro"].sum()
                                                contribuciones = df_sector["Valor_contribucion"].sum()
                                                dic_codigo_DANE[ele_codigo_DANE][s1][0] += cantidad_usuario
                                                dic_codigo_DANE[ele_codigo_DANE][s1][1] += volumen
                                                dic_codigo_DANE[ele_codigo_DANE][s1][2] += valor_total_facturado
                                                dic_codigo_DANE[ele_codigo_DANE][s1][3] += valor_consumo_facturado
                                                dic_codigo_DANE[ele_codigo_DANE][s1][4] += cantidad_facturas
                                                dic_codigo_DANE[ele_codigo_DANE][s1][6] += contribuciones
                                    except BaseException:
                                        pass
                    if len(dic_codigo_DANE):
                        lista_df_codigo_DANE = []
                        for ele_codigo_DANE, dic_dataframe in dic_codigo_DANE.items():
                            lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3", "Codigo DANE"]
                            dic_dataframe = dict(sorted(dic_dataframe.items()))
                            dic_dataframe_2 = {"Tipo de usuario":[],
                                                "Sector de consumo":[],
                                                "Cantidad de usuarios":[],
                                                "Consumo m3":[]}
                            if facturas:
                                dic_dataframe_2["Cantidad de facturas"] = []
                                lista_columnas.append("Cantidad de facturas")
                            if valor_facturado:
                                dic_dataframe_2["Valor facturación por consumo"] = []
                                dic_dataframe_2["Valor total facturado"] = []
                                lista_columnas.append("Valor facturación por consumo")
                                lista_columnas.append("Valor total facturado")
                            if subsidio:
                                dic_dataframe_2["Subsidios"] = []
                                dic_dataframe_2["Contribuciones"] = []
                                lista_columnas.append("Subsidios")
                                lista_columnas.append("Contribuciones")
                            for llave, valor in dic_dataframe.items():
                                try:
                                    str_llave = str(llave)
                                    if str_llave in tabla_11["datos"]:
                                        if reporte_DANE:
                                            valor_1 = str_llave
                                            dic_dataframe_2["Tipo de usuario"].append("No regulado")
                                        else:
                                            valor_1 = tabla_11["datos"][str(llave)]
                                            dic_dataframe_2["Tipo de usuario"].append("No regulados")
                                        dic_dataframe_2["Sector de consumo"].append(valor_1)
                                        dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                                        dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                                        if valor_facturado:
                                            dic_dataframe_2["Valor facturación por consumo"].append(round(valor[3]))
                                            dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                                        if facturas:
                                            dic_dataframe_2["Cantidad de facturas"].append(valor[4])
                                        if subsidio:
                                            dic_dataframe_2["Subsidios"].append(valor[5])
                                            dic_dataframe_2["Contribuciones"].append(valor[6])
                                except BaseException:
                                    pass
                            df_codigo_DANE_gen = pd.DataFrame(dic_dataframe_2)
                            df_codigo_DANE_gen["Codigo DANE"] = ele_codigo_DANE
                            df_codigo_DANE_gen["Anio reportado"] = anio_reportado
                            if reporte_DANE:
                                mes_reportado = lista_meses.index(mes_reportado)+1
                            df_codigo_DANE_gen["Mes reportado"] = mes_reportado
                            df_codigo_DANE_gen["Filial"] = dic_filiales[filial]
                            df_codigo_DANE_gen["NIT"] = dic_nit[dic_filiales[filial]]
                            df_codigo_DANE_gen = df_codigo_DANE_gen[lista_columnas]
                            lista_df_codigo_DANE.append(df_codigo_DANE_gen)
                        if len(lista_df_codigo_DANE) > 0:
                            df_codigo_DANE_gen_tot = pd.concat(lista_df_codigo_DANE, ignore_index=True)
                            v_codigo_DANE_texto = codigo_DANE_texto(codigo_DANE)
                            lista_nombre = archivo.split("\\")
                            if subsidio:
                                lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_consumo_{str(v_codigo_DANE_texto)}_subsidio.csv")
                            else:
                                if reporte_DANE:
                                    lista_nombre[-2] = "09. DANE"
                                    lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_DANE_{str(v_codigo_DANE_texto)}.csv")
                                else:
                                    lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_consumo_{str(v_codigo_DANE_texto)}.csv")
                            nombre = lista_a_texto(lista_nombre,"\\")
                            return df_codigo_DANE_gen_tot, nombre
                        else:
                            return None, None
                    else:
                        return None, None
                else:
                    for i in range(len(lista_df)):
                        df = lista_df[i].copy()
                        lista_sectores = list(df["Sector_consumo"].unique())
                        for sector in lista_sectores:
                            try:
                                s1 = int(sector)
                                df_sector = df[df["Sector_consumo"] == s1].copy()
                                if s1 not in dic_dataframe:
                                    dic_dataframe[s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                df_sector.loc[:, 'Composicion_usuario'] = (
                                    df_sector['ID_Factura'].astype(str) + '_' +
                                    df_sector['Concepto_general_factura'].astype(str) + '_' +
                                    df_sector['Sector_consumo'].astype(str))
                                cantidad = len(list(df_sector['Composicion_usuario'].unique()))
                                volumen = df_sector["Volumen"].sum()
                                valor_total = df_sector["Valor_total_facturado"].sum()
                                df_sector.loc[:, 'ID_Factura'] = df_sector['ID_Factura'].str.upper()
                                df_facturas = df[df['ID_Factura'].str.startswith('F')]
                                cantidad_facturas = len(df_facturas)
                                valor_consumo_facturado = df_sector["Facturacion_por_suministro"].sum()
                                contribuciones = df_sector["Valor_contribucion"].sum()
                                dic_dataframe[s1][0] += cantidad
                                dic_dataframe[s1][1] += volumen
                                dic_dataframe[s1][2] += valor_total
                                dic_dataframe[s1][3] += valor_consumo_facturado
                                dic_dataframe[s1][4] += cantidad_facturas
                                dic_dataframe[s1][6] += contribuciones
                                dic["Cantidad de usuarios"] += cantidad
                                dic["Consumo m3"] += volumen
                                dic["Valor total facturado"] += valor_total
                                dic["Valor consumo facturado"] += valor_consumo_facturado
                                dic["Cantidad de facturas"] += cantidad_facturas
                                dic["Contribuciones"] += contribuciones
                            except BaseException:
                                pass
                    dic_dataframe = dict(sorted(dic_dataframe.items()))
                    dic_dataframe_2 = {"Tipo de usuario":[],
                                        "Sector de consumo":[],
                                        "Cantidad de usuarios":[],
                                        "Consumo m3":[]}
                    lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3"]
                    if facturas:
                        dic_dataframe_2["Cantidad de facturas"] = []
                        lista_columnas.append("Cantidad de facturas")
                    if valor_facturado:
                        dic_dataframe_2["Valor facturación por consumo"] = []
                        dic_dataframe_2["Valor total facturado"] = []
                        lista_columnas.append("Valor facturación por consumo")
                        lista_columnas.append("Valor total facturado")
                    if subsidio:
                        dic_dataframe_2["Subsidios"] = []
                        dic_dataframe_2["Contribuciones"] = []
                        lista_columnas.append("Subsidios")
                        lista_columnas.append("Contribuciones")
                    for llave, valor in dic_dataframe.items():
                        try:
                            str_llave = str(llave)
                            if str_llave in tabla_11["datos"]:
                                if reporte_DANE:
                                    valor_1 = str_llave
                                    dic_dataframe_2["Tipo de usuario"].append("No regulado")
                                else:
                                    valor_1 = tabla_11["datos"][str(llave)]
                                    dic_dataframe_2["Tipo de usuario"].append("No regulados")
                                dic_dataframe_2["Sector de consumo"].append(valor_1)
                                dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                                dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                                if valor_facturado:
                                    dic_dataframe_2["Valor facturación por consumo"].append(round(valor[3]))
                                    dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                                if facturas:
                                    dic_dataframe_2["Cantidad de facturas"].append(valor[4])
                                if subsidio:
                                    dic_dataframe_2["Subsidios"].append(valor[5])
                                    dic_dataframe_2["Contribuciones"].append(valor[6])
                        except BaseException:
                            pass
                    df1 = pd.DataFrame(dic_dataframe_2)
                    df1["Filial"] = dic_filiales[filial]
                    df1["NIT"] = dic_nit[dic_filiales[filial]]
                    df1["Anio reportado"] = anio_reportado
                    if reporte_DANE:
                        mes_reportado = lista_meses.index(mes_reportado)+1
                    df1["Mes reportado"] = mes_reportado
                    lista_nombre = archivo.split("\\")
                    if subsidio:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo_subsidio.csv")
                    else:
                        if reporte_DANE:
                            lista_nombre[-2] = "09. DANE"
                            lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_DANE.csv")
                        else:
                            lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo.csv")
                    nombre = lista_a_texto(lista_nombre, "\\")
                    if len(df1) > 0:
                        df1 = df1[lista_columnas]
                        if total and not codigo_DANE and not reporte_DANE:
                            if not valor_facturado:
                                del dic["Valor total facturado"]
                                del dic["Valor facturación por consumo"]
                            if not facturas:
                                del dic["Cantidad de facturas"]
                            if not subsidio:
                                del dic["Subsidios"]
                                del dic["Contribuciones"]
                            nueva_fila = []
                            for columna in list(df1.columns):
                                if columna in dic:
                                    nueva_fila.append(dic[columna])
                                elif columna == "Sector de consumo":
                                    nueva_fila.append("Total")
                                else:
                                    nueva_fila.append(df1[columna][0])
                            df1.loc[len(df1)] = nueva_fila
                        return df1, nombre
                    else:
                        return None,None
            else:
                return None,None
    else:
        return None,None

def buscar_NIU(lista_NIU, dic_NIU, subsidio=False, rango=20):
    dic_2 = dic_NIU.copy()
    cantidad_usuario = 0
    volumen = 0
    valor_total_facturado = 0
    valor_consumo_facturado = 0
    cantidad_facturas = 0
    v_subsidios = 0
    v_contribuciones = 0
    for elemento in lista_NIU:
        if elemento in dic_2:
            valor = dic_2[elemento]#consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
            if subsidio:
                cantidad_usuario += 1
                if valor[0] > rango:
                    volumen += rango
                elif valor[0] <= rango:
                    volumen += valor[0]
                valor_total_facturado += valor[1]
                valor_consumo_facturado += valor[2]
                cantidad_facturas += valor[3]
                v_subsidios += valor[4]
                v_contribuciones += valor[5]
            else:
                cantidad_usuario += 1
                volumen += valor[0]
                valor_total_facturado += valor[1]
                valor_consumo_facturado += valor[2]
                cantidad_facturas += valor[3]
    return cantidad_usuario, volumen, valor_total_facturado,valor_consumo_facturado,cantidad_facturas,v_subsidios,v_contribuciones

def busqueda_sector_GRTT2(lista_archivos, dic_NIU, codigo_DANE, reporte, filial, nombre, valor_facturado=True, subsidio=False, facturas=False, reporte_DANE=False, rango=20):
    for archivo in lista_archivos:
        if reporte in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                dic_dataframe = {}
                dic_codigo_DANE = {}
                if codigo_DANE:
                    for i in range(len(lista_df)):
                        df = lista_df[i].copy()
                        for ele_codigo_DANE in codigo_DANE:
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore", category=FutureWarning)
                                df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['Codigo_DANE'])
                            df["Estado"] = pd.to_numeric(df["Estado"], errors='coerce').fillna(0).astype(int)
                            df["Estrato"] = pd.to_numeric(df["Estrato"], errors='coerce').fillna(0).astype(int)
                            df["Codigo_DANE"] = pd.to_numeric(df["Codigo_DANE"], errors='coerce').fillna(0).astype(int)
                            df_codigo_DANE = df[df["Codigo_DANE"] == ele_codigo_DANE].reset_index(drop=True)
                            if len(df_codigo_DANE) > 0:
                                if ele_codigo_DANE not in dic_codigo_DANE:
                                    dic_codigo_DANE[ele_codigo_DANE] = {}
                                lista_sectores = list(df_codigo_DANE["Estrato"].unique())
                                for sector in lista_sectores:
                                    if subsidio:
                                        if str(sector) in ["1","2"]:
                                            try:
                                                s1 = int(sector)
                                                df_sector = df_codigo_DANE[df_codigo_DANE["Estrato"] == s1].reset_index(drop=True)
                                                lista_NIU_sector = list(df_sector["NIU"].unique())
                                                if s1 not in dic_codigo_DANE[ele_codigo_DANE]:
                                                    dic_codigo_DANE[ele_codigo_DANE][s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                                cantidad_usuario,volumen,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,v_subsidios,v_contribuciones = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                                dic_codigo_DANE[ele_codigo_DANE][s1][0] += cantidad_usuario
                                                dic_codigo_DANE[ele_codigo_DANE][s1][1] += volumen
                                                dic_codigo_DANE[ele_codigo_DANE][s1][2] += valor_total_facturado
                                                dic_codigo_DANE[ele_codigo_DANE][s1][3] += valor_consumo_facturado
                                                dic_codigo_DANE[ele_codigo_DANE][s1][4] += cantidad_facturas
                                                dic_codigo_DANE[ele_codigo_DANE][s1][5] += v_subsidios
                                                dic_codigo_DANE[ele_codigo_DANE][s1][6] += v_contribuciones
                                            except TypeError:
                                                pass
                                            except ValueError:
                                                pass
                                    else:
                                        try:
                                            s1 = int(sector)
                                            if s1 > 0:
                                                df_sector = df_codigo_DANE[df_codigo_DANE["Estrato"] == s1].reset_index(drop=True)
                                                lista_NIU_sector = list(df_sector["NIU"].unique())
                                                if s1 not in dic_codigo_DANE[ele_codigo_DANE]:
                                                    dic_codigo_DANE[ele_codigo_DANE][s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                                cantidad_usuario,volumen,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,v_subsidios,v_contribuciones = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                                dic_codigo_DANE[ele_codigo_DANE][s1][0] += cantidad_usuario
                                                dic_codigo_DANE[ele_codigo_DANE][s1][1] += volumen
                                                dic_codigo_DANE[ele_codigo_DANE][s1][2] += valor_total_facturado
                                                dic_codigo_DANE[ele_codigo_DANE][s1][3] += valor_consumo_facturado
                                                dic_codigo_DANE[ele_codigo_DANE][s1][4] += cantidad_facturas
                                        except TypeError:
                                            pass
                                        except ValueError:
                                            pass
                    if len(dic_codigo_DANE) > 0:
                        lista_df_codigo_DANE = []
                        for ele_codigo_DANE, dic_dataframe in dic_codigo_DANE.items():
                            lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3", "Codigo DANE"]
                            dic_dataframe = dict(sorted(dic_dataframe.items()))
                            dic_dataframe_2 = {"Tipo de usuario":[],
                                                "Sector de consumo":[],
                                                "Cantidad de usuarios":[],
                                                "Consumo m3":[]}
                            if facturas:
                                dic_dataframe_2["Cantidad de facturas"] = []
                                lista_columnas.append("Cantidad de facturas")
                            if valor_facturado:
                                dic_dataframe_2["Valor facturación por consumo"] = []
                                dic_dataframe_2["Valor total facturado"] = []
                                lista_columnas.append("Valor facturación por consumo")
                                lista_columnas.append("Valor total facturado")
                            if subsidio:
                                dic_dataframe_2["Subsidios"] = []
                                dic_dataframe_2["Contribuciones"] = []
                                lista_columnas.append("Subsidios")
                                lista_columnas.append("Contribuciones")
                            for llave, valor in dic_dataframe.items():
                                try:
                                    str_llave = str(llave)
                                    if str_llave in tabla_3["datos"]:
                                        if reporte_DANE:
                                            valor_1 = str_llave
                                            dic_dataframe_2["Tipo de usuario"].append("Regulado")
                                        else:
                                            valor_1 = tabla_3["datos"][str(llave)]
                                            dic_dataframe_2["Tipo de usuario"].append("Regulados")
                                        dic_dataframe_2["Sector de consumo"].append(valor_1)
                                        dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                                        dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                                        if valor_facturado:
                                            dic_dataframe_2["Valor facturación por consumo"].append(round(valor[3]))
                                            dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                                        if facturas:
                                            dic_dataframe_2["Cantidad de facturas"].append(valor[4])
                                        if subsidio:
                                            dic_dataframe_2["Subsidios"].append(valor[5])
                                            dic_dataframe_2["Contribuciones"].append(valor[6])
                                except BaseException:
                                    pass
                            df_codigo_DANE_gen = pd.DataFrame(dic_dataframe_2)
                            df_codigo_DANE_gen["Codigo DANE"] = ele_codigo_DANE
                            df_codigo_DANE_gen["Anio reportado"] = anio_reportado
                            if reporte_DANE:
                                mes_reportado = lista_meses.index(mes_reportado)+1
                            df_codigo_DANE_gen["Mes reportado"] = mes_reportado
                            df_codigo_DANE_gen["Filial"] = dic_filiales[filial]
                            df_codigo_DANE_gen["NIT"] = dic_nit[dic_filiales[filial]]
                            df_codigo_DANE_gen = df_codigo_DANE_gen[lista_columnas]
                            lista_df_codigo_DANE.append(df_codigo_DANE_gen)
                        if len(lista_df_codigo_DANE) > 0:
                            df_codigo_DANE_gen_tot = pd.concat(lista_df_codigo_DANE, ignore_index=True)
                            v_codigo_DANE_texto = codigo_DANE_texto(codigo_DANE)
                            lista_nombre = nombre.split("\\")
                            if subsidio:
                                lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_consumo_{str(v_codigo_DANE_texto)}_subsidio.csv")
                            else:
                                if reporte_DANE:
                                    lista_nombre[-2] = "09. DANE"
                                    lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_DANE_{str(v_codigo_DANE_texto)}.csv")
                                else:
                                    lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", f"_reporte_consumo_{str(v_codigo_DANE_texto)}.csv")
                            nombre = lista_a_texto(lista_nombre,"\\")
                            return df_codigo_DANE_gen_tot, nombre
                        else:
                            return None, None
                    else:
                        return None, None
                else:
                    dic_dataframe = {}
                    for i in range(len(lista_df)):
                        df = lista_df[i].copy()
                        df["Estado"] = pd.to_numeric(df["Estado"], errors='coerce').fillna(0).astype(int)
                        df["Estrato"] = pd.to_numeric(df["Estrato"], errors='coerce').fillna(0).astype(int)
                        lista_sectores = list(df["Estrato"].unique())
                        for sector in lista_sectores:
                            if subsidio:
                                if str(sector) in ["1","2"]:
                                    try:
                                        s1 = int(sector)
                                        df_sector = df[df["Estrato"] == s1].reset_index(drop=True)
                                        lista_NIU_sector = list(df_sector["NIU"].unique())
                                        if s1 not in dic_dataframe:
                                            dic_dataframe[s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                        cantidad_usuario,volumen,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,v_subsidios,v_contribuciones = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                        dic_dataframe[s1][0] += cantidad_usuario
                                        dic_dataframe[s1][1] += volumen
                                        dic_dataframe[s1][2] += valor_total_facturado
                                        dic_dataframe[s1][3] += valor_consumo_facturado
                                        dic_dataframe[s1][4] += cantidad_facturas
                                        dic_dataframe[s1][5] += v_subsidios
                                        dic_dataframe[s1][6] += v_contribuciones
                                    except BaseException:
                                        pass
                            else:
                                try:
                                    s1 = int(sector)
                                    if s1 > 0:
                                        df_sector = df[df["Estrato"] == s1].reset_index(drop=True)
                                        lista_NIU_sector = list(df_sector["NIU"].unique())
                                        if s1 not in dic_dataframe:
                                            dic_dataframe[s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                        cantidad_usuario,volumen,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,v_subsidios,v_contribuciones = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                        dic_dataframe[s1][0] += cantidad_usuario
                                        dic_dataframe[s1][1] += volumen
                                        dic_dataframe[s1][2] += valor_total_facturado
                                        dic_dataframe[s1][3] += valor_consumo_facturado
                                        dic_dataframe[s1][4] += cantidad_facturas
                                except BaseException:
                                    pass
                    dic_dataframe = dict(sorted(dic_dataframe.items()))
                    dic_dataframe_2 = {"Tipo de usuario":[],
                                        "Sector de consumo":[],
                                        "Cantidad de usuarios":[],
                                        "Consumo m3":[]}
                    lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3"]
                    if facturas:
                        dic_dataframe_2["Cantidad de facturas"] = []
                        lista_columnas.append("Cantidad de facturas")
                    if valor_facturado:
                        dic_dataframe_2["Valor facturación por consumo"] = []
                        dic_dataframe_2["Valor total facturado"] = []
                        lista_columnas.append("Valor facturación por consumo")
                        lista_columnas.append("Valor total facturado")
                    if subsidio:
                        dic_dataframe_2["Subsidios"] = []
                        dic_dataframe_2["Contribuciones"] = []
                        lista_columnas.append("Subsidios")
                        lista_columnas.append("Contribuciones")
                    for llave, valor in dic_dataframe.items():
                        try:
                            str_llave = str(llave)
                            if str_llave in tabla_3["datos"]:
                                if reporte_DANE:
                                    valor_1 = str_llave
                                    dic_dataframe_2["Tipo de usuario"].append("Regulado")
                                else:
                                    valor_1 = tabla_3["datos"][str_llave]
                                    dic_dataframe_2["Tipo de usuario"].append("Regulados")
                                dic_dataframe_2["Sector de consumo"].append(valor_1)
                                dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                                dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                                if valor_facturado:
                                    dic_dataframe_2["Valor facturación por consumo"].append(round(valor[3]))
                                    dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                                if facturas:
                                    dic_dataframe_2["Cantidad de facturas"].append(valor[4])
                                if subsidio:
                                    dic_dataframe_2["Subsidios"].append(valor[5])
                                    dic_dataframe_2["Contribuciones"].append(valor[6])
                        except BaseException:
                            pass
                    df1 = pd.DataFrame(dic_dataframe_2)
                    df1["Anio reportado"] = anio_reportado
                    if reporte_DANE:
                        mes_reportado = lista_meses.index(mes_reportado)+1
                    df1["Mes reportado"] = mes_reportado
                    df1["Filial"] = dic_filiales[filial]
                    df1["NIT"] = dic_nit[dic_filiales[filial]]
                    df1 = df1[lista_columnas]
                    lista_nombre = nombre.split("\\")
                    if subsidio:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo_subsidio.csv")
                    else:
                        if reporte_DANE:
                            lista_nombre[-2] = "09. DANE"
                            lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_DANE.csv")
                        else:
                            lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo.csv")
                    nombre = lista_a_texto(lista_nombre,"\\")
                    return df1, nombre
            return None, None
    return None, None

def apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos, codigo_DANE, reporte, valor_facturado,filial, subsidio=False, total=False, facturas=False, reporte_DANE=False):
    for archivo in lista_archivos:
        if reporte in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                dic_1 = {}
                dic = {"Cantidad de usuarios":0,"Consumo m3":0,"Valor total facturado":0, "Valor consumo facturado":0,"Cantidad de facturas":0, "Subsidios":0, "Contribuciones":0}
                for i in range(len(lista_df)):
                    df = lista_df[i].reset_index(drop=True)
                    for pos in range(len(df)):
                        try:
                            elemento = int(df["NIU"][pos])
                            consumo = float(df["Consumo"][pos])
                            valor_total_facturado = float(df["Valor_total_facturado"][pos])
                            valor_consumo_facturado = float(df["Facturacion_consumo"][pos])
                            factura = str(df["ID_factura"][pos]).upper()
                            subsidio_contribuciones = float(df["Valor_subsidio_contribucion"][pos])
                            dic["Consumo m3"] += consumo
                            dic["Valor consumo facturado"] += valor_consumo_facturado
                            dic["Valor total facturado"] += valor_total_facturado
                            if factura[0] == "F":
                                dic["Cantidad de facturas"] += 1
                            if subsidio_contribuciones < 0:
                                dic["Subsidios"] += subsidio_contribuciones
                            else:
                                dic["Contribuciones"] += subsidio_contribuciones
                            if elemento not in dic_1:
                                dic_1[elemento] = [0,0,0,0,0,0].copy() #consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                            if not math.isnan(consumo) and not math.isnan(valor_total_facturado) and not math.isnan(valor_consumo_facturado) and not math.isnan(subsidio_contribuciones):
                                dic_1[elemento][0] += consumo
                                dic_1[elemento][1] += valor_total_facturado
                                dic_1[elemento][2] += valor_consumo_facturado
                                if factura[0] == "F":
                                    dic_1[elemento][3] += 1
                                if subsidio_contribuciones < 0:
                                    dic_1[elemento][4] += subsidio_contribuciones
                                else:
                                    dic_1[elemento][5] += subsidio_contribuciones
                        except BaseException:
                            pass
                df1, nombre = busqueda_sector_GRTT2(lista_archivos, dic_1, codigo_DANE, "GRTT2", filial, archivo, valor_facturado, subsidio, facturas, reporte_DANE)
                if total and not codigo_DANE and not reporte_DANE:
                    dic["Cantidad de usuarios"] = len(dic_1)
                    if not valor_facturado:
                        del dic["Valor total facturado"]
                        del dic["Valor consumo facturado"]
                    if not subsidio:
                        del dic["Subsidios"]
                        del dic["Contribuciones"]
                    if not facturas:
                        del dic["Cantidad de facturas"]
                    nueva_fila = []
                    for columna in list(df1.columns):
                        if columna in dic:
                            nueva_fila.append(dic[columna])
                        elif columna == "Sector de consumo":
                            nueva_fila.append("Total")
                        else:
                            nueva_fila.append(df1[columna][0])
                    df1.loc[len(df1)] = nueva_fila
                if nombre:
                    return df1, nombre
                else:
                    return None, None
            else:
                return None, None
    return None, None

def apoyo_reporte_comercial_sector_consumo(df1, n1, df2, n2, informar=True,reporte_DANE=False, thread=None):
    if n1 and n2:
        lista_n1 = n1.split("\\")
        nombre_1 = lista_n1[-1].split("_")[1:]
        lista_n1[-1] = lista_a_texto(nombre_1, "_", False)
        n1 = lista_a_texto(lista_n1, "\\", False)
        lista_n2 = n2.split("\\")
        nombre_2 = lista_n2[-1].split("_")[1:]
        lista_n2[-1] = lista_a_texto(nombre_2, "_", False)
        n2 = lista_a_texto(lista_n2, "\\", False)
        df3 = pd.concat([df1, df2])
        almacenar_df_csv_y_excel(df3, n1, informar, reporte_DANE=reporte_DANE, thread=thread)
        if not reporte_DANE:
            almacenar_df_csv_y_excel(df3, n2, informar, thread=thread)
        return df3, n1
    elif n1:
        lista_n1 = n1.split("\\")
        nombre_1 = lista_n1[-1].split("_")[1:]
        lista_n1[-1] = lista_a_texto(nombre_1, "_", False)
        n1 = lista_a_texto(lista_n1, "\\", False)
        df3 = df1.copy()
        almacenar_df_csv_y_excel(df3, n1, informar, reporte_DANE=reporte_DANE, thread=thread)
        return df3, n1
    elif n2:
        lista_n2 = n2.split("\\")
        nombre_2 = lista_n2[-1].split("_")[1:]
        lista_n2[-1] = lista_a_texto(nombre_2, "_", False)
        n2 = lista_a_texto(lista_n2, "\\", False)
        df3 = df2.copy()
        almacenar_df_csv_y_excel(df3, n2, informar, reporte_DANE=reporte_DANE, thread=thread)
        return df3, n2
    return None, None

def reporte_comercial_sector_consumo(dic_archivos, seleccionar_reporte, informar=True, codigo_DANE=None, valor_facturado=True, subsidio=False, almacenar_excel=True, total=False, facturas=False, reporte_DANE=False, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            n1 = None
            n2 = None
            df1 = pd.DataFrame()
            df2 = pd.DataFrame()
            nombre_compilado = None
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df1, n1 = apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos_filial, codigo_DANE, "GRC1", valor_facturado, filial, subsidio, total, facturas, reporte_DANE)
                df2, n2 = apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos_filial, codigo_DANE, "GRC2", filial, valor_facturado, total, subsidio, facturas, reporte_DANE)
                df,nombre = apoyo_reporte_comercial_sector_consumo(df1, n1, df2, n2, informar, reporte_DANE, thread=thread)
                if nombre:
                    if reporte_DANE:
                        df["ESTABLECIMIENTO"] = " "
                        df["No_Orden"] = list(range(1,len(df)+1))
                        df = df[['NIT', 'Filial', 'Anio reportado', 'Mes reportado', 'Tipo de usuario', 'Sector de consumo', 'Consumo m3', 'Valor total facturado', "ESTABLECIMIENTO", "No_Orden"]]
                        df.columns = ['NIT', 'RAZON SOCIAL', 'AÑO', 'MES', 'TIPO DE MERCADO', 'SECTOR DE CONSUMO', 'VOLUMEN M3 FACTURADO', 'VALOR FACTURADO', "ESTABLECIMIENTO", "No_Orden"]
                        df = df[["No_Orden", 'NIT', 'RAZON SOCIAL', "ESTABLECIMIENTO", 'TIPO DE MERCADO', 'SECTOR DE CONSUMO', 'AÑO', 'MES', 'VALOR FACTURADO','VOLUMEN M3 FACTURADO']]
                    lista_df_filiales.append(df)
                    nombre_compilado = nombre
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales)
            df_total["No_Orden"] = list(range(1,len(df_total)+1))
            lista_nombre = nombre_compilado.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            if total and not codigo_DANE:
                df_total_suma, proceso = generar_sumatoria_df(df_total)
                if proceso:
                    df_total = df_total_suma.copy()
                    nuevo_nombre = nuevo_nombre.replace(".csv","_sumatoria.csv")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel, reporte_DANE=reporte_DANE, thread=thread)

def reporte_SH(dic_archivos, seleccionar_reporte, informar=True, codigo_DANE=[], thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            apoyo_reporte_SH(lista_archivos_filial, codigo_DANE, thread=thread)

def apoyo_reporte_SH(lista_archivos_filial, codigo_DANE, thread=None):
    ele_codigo_DANE = codigo_DANE[0]
    bool_GRC1 = False
    bool_GRTT2 = False
    for archivo in lista_archivos_filial:
        if "GRC1" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                dic_GRC1 = {}
                nombre = archivo
                bool_GRC1 = True
                for i in range(len(lista_df)):
                    df = lista_df[i].copy()
                    for j in range(len(df)):
                        v_NIU = df["NIU"][j]
                        if v_NIU not in dic_GRC1:
                            dic_GRC1[v_NIU] = [0,0,0,0,0] #consumo,valor_sub_con,cargo_aplicado,valor_otros,valor_total
                        try:
                            consumo = float(df["Consumo"][j])
                            valor_sub_con = float(df["Valor_subsidio_contribucion"][j])
                            cargo_aplicado = float(df["Cuv_cargo_aplicado_consumo"][j])
                            valor_otros = float(df["Valor_otros_conceptos"][j])
                            valor_total = float(df["Valor_total_facturado"][j])
                            dic_GRC1[v_NIU][0] += consumo
                            dic_GRC1[v_NIU][1] += valor_sub_con
                            dic_GRC1[v_NIU][2] += cargo_aplicado
                            dic_GRC1[v_NIU][3] += valor_otros
                            dic_GRC1[v_NIU][4] += valor_total
                        except BaseException:
                            pass
        if "GRTT2" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if len(lista_df):
                bool_GRTT2 = True
            dic_GRTT2 = {}
            for i in range(len(lista_df)):
                df = lista_df[i].copy()
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=FutureWarning)
                    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['Codigo_DANE'])
                df["Codigo_DANE"] = df["Codigo_DANE"].astype(int)
                df["Codigo_DANE"] = df["Codigo_DANE"].fillna(0).astype(int)
                df["Codigo_DANE"] = df["Codigo_DANE"].astype(str).replace("0", "").replace("nan", "")
                df["Codigo_DANE"] = df["Codigo_DANE"].apply(completar_codigo_DANE)
                df["Codigo_DANE"] = df["Codigo_DANE"].astype(int)
                df_codigo_DANE = df[df["Codigo_DANE"] == ele_codigo_DANE].reset_index(drop=True)
                for j in range(len(df_codigo_DANE)):
                    v_NIU = df["NIU"][j]
                    if v_NIU not in dic_GRTT2:
                        dic_GRTT2[v_NIU] = [df_codigo_DANE["Estrato"][j], df_codigo_DANE["Direccion"][j]] #Estrato, Dirección
    if bool_GRC1 and bool_GRTT2:
        dic_df = {"NIU":[],
                    "ESTRATO":[],
                    "DIRECCION":[],
                    "CONSUMO":[],
                    "VALOR DEL SUBSIDIO O CONTRIBUCION":[],
                    "CARGO APLICADO POR CONSUMO":[],
                    "VALOR OTROS CONCEPTOS":[],
                    "VALOR TOTAL FACTURADO":[],
                    "CODIGO DANE":[]}
        for v_NIU, lista_datos in dic_GRC1.items():
            if v_NIU in dic_GRTT2:
                dic_df["NIU"].append(v_NIU)
                dic_df["ESTRATO"].append(dic_GRTT2[v_NIU][0])
                dic_df["DIRECCION"].append(dic_GRTT2[v_NIU][1])
                dic_df["CONSUMO"].append(lista_datos[0])
                dic_df["VALOR DEL SUBSIDIO O CONTRIBUCION"].append(lista_datos[1])
                dic_df["CARGO APLICADO POR CONSUMO"].append(lista_datos[2])
                dic_df["VALOR OTROS CONCEPTOS"].append(lista_datos[3])
                dic_df["VALOR TOTAL FACTURADO"].append(lista_datos[4])
                dic_df["CODIGO DANE"].append(ele_codigo_DANE)
        df_SH = pd.DataFrame(dic_df)
        lista_nombre = nombre.split("\\")
        lista_nombre[-2] = "10. SH"
        lista_nombre[-1] = "SH_"+lista_nombre[-1].split("_")[2]+"_"+lista_nombre[-1].split("_")[3]+".csv"
        nombre = lista_a_texto(lista_nombre,"\\")
        almacenar_df_csv_y_excel(df_SH, nombre, almacenar_excel=False, thread=thread)

def diferencia_columnas_dataframe(df_actual, df_anterior):
    df_actual = df_actual.copy().reset_index(drop=True)
    df_anterior = df_anterior.copy().reset_index(drop=True)
    lista_columnas_num = ["Cantidad de usuarios","Consumo m3","Valor total facturado","Valor facturación por consumo",
                        "Cantidad de facturas"]
    for columna in lista_columnas_num:
        df_actual["Diferencia "+columna] = None
    for i in range(len(df_actual)):
        try:
            df_filtro_anterior = df_anterior[(df_anterior["Tipo de usuario"] == df_actual["Tipo de usuario"][i]) &
                                                (df_anterior["Sector de consumo"] == df_actual["Sector de consumo"][i]) &
                                                (df_anterior["Filial"] == df_actual["Filial"][i])].reset_index(drop=True)
            df_filtro_actual = df_actual[(df_actual["Tipo de usuario"] == df_actual["Tipo de usuario"][i]) &
                                                (df_actual["Sector de consumo"] == df_actual["Sector de consumo"][i]) &
                                                (df_actual["Filial"] == df_actual["Filial"][i])].reset_index(drop=True)
            if len(df_filtro_anterior) and len(df_filtro_actual):
                for columna in lista_columnas_num:
                    valor_actual = df_filtro_actual[columna][0]
                    valor_anterior = df_filtro_anterior[columna][0]
                    df_actual.iloc[i, df_actual.columns.get_loc("Diferencia "+columna)] = valor_actual - valor_anterior
        except BaseException:
            pass
    return df_actual

def union_archivos_mensuales_anual_reporte_consumo(dic_archivos, seleccionar_reporte, informar, almacenar_excel=True, subsidio=True, thread=None):
    #v_fecha_siguiente = fecha_siguiente(seleccionar_reporte["fecha_personalizada"][0][0],seleccionar_reporte["fecha_personalizada"][0][1])
    #v_fecha_anterior = fecha_anterior(seleccionar_reporte["fecha_personalizada"][1][0],seleccionar_reporte["fecha_personalizada"][1][1])
    fecha_nombre = (seleccionar_reporte["fecha_personalizada"][0][0]+"_"+seleccionar_reporte["fecha_personalizada"][0][1].upper()
                    +"_"+seleccionar_reporte["fecha_personalizada"][1][0]+"_"+seleccionar_reporte["fecha_personalizada"][1][1].upper())
    lista_anual = []
    lista_df_anual_dif = []
    for _, lista_archivos in dic_archivos.items():
        for archivo in lista_archivos:
            df = leer_dataframe_utf_8(archivo)
            nombre = archivo
            if len(df):
                lista_anual.append(df)
    largo = len(lista_anual)
    if subsidio:
        if largo == 12:
            lista_df_anual_dif = lista_anual.copy()
        elif largo > 12:
            lista_df_anual_dif = lista_anual.copy()[-12:]
        else:
            lista_df_anual_dif = lista_anual.copy()
    else:
        if len(seleccionar_reporte["filial"]) == 4:
            for i in range(1,len(lista_anual)):
                df = lista_anual[i]
                df_actual = diferencia_columnas_dataframe(lista_anual[i], lista_anual[i-1])
                lista_df_anual_dif.append(df_actual)
        else:
            if largo == 12:
                lista_df_anual_dif = lista_anual.copy()
            elif largo > 12:
                lista_df_anual_dif = lista_anual.copy()[-12:]
            else:
                lista_df_anual_dif = lista_anual.copy()
    if len(lista_df_anual_dif):
        if len(seleccionar_reporte["filial"]) == 4:
            lista_nombre = nombre.split("\\")
            lista_nombre[-5] = "00. Compilado"
            lista_nombre[-3] = "00. Compilado"
            ext_nombre = lista_nombre[-1].split("_")
            ext_nombre.pop(0)
            ext_nombre[0] = fecha_nombre
            lista_nombre[-1] = lista_a_texto(ext_nombre, "_")
            crear_carpeta_anual(fecha_nombre, lista_nombre)
            lista_nombre.insert(-2, fecha_nombre)
            nombre = lista_a_texto(lista_nombre, "\\")
            df_anual = pd.concat(lista_df_anual_dif)
            almacenar_df_csv_y_excel(df_anual, nombre, informar, almacenar_excel, thread=thread)
            return nombre
        else:
            lista_nombre = nombre.split("\\")
            lista_nombre[-6] = "00. Compilado"
            lista_nombre[-4] = "00. Compilado"
            ext_nombre = lista_nombre[-1].split("_")
            ext_nombre.pop(1)
            ext_nombre[1] = fecha_nombre
            lista_nombre[-1] = lista_a_texto(ext_nombre, "_")
            nombre = lista_a_texto(lista_nombre, "\\")
            df_anual = pd.concat(lista_df_anual_dif)
            almacenar_df_csv_y_excel(df_anual, nombre, informar, almacenar_excel, thread=thread)
            return None
    else:
        return None

def apoyo_reporte_comparacion_prd_cld_cer(lista_archivos, informar, filial, thread=None):
    dic_GRTT2 = {}
    dic_SAP_CLD = {}
    dic_SAP_PRD = {}
    dic_GRC1 = {}
    proceso_CLD = False
    proceso_PRD = False
    proceso_GRTT2 = False
    lista_df_porcentaje = []
    for archivo in lista_archivos:
        if "SAP" not in archivo and "GRC1" in archivo:
            nombre_final = archivo
        dic_conteo = {"Lectura_real":0,
                    "Lectura_estimada":0,
                    "Consumo":0,
                    "Valor total facturado":0}
        dic_NIU_unico = {"Lectura_real":{},
                        "Lectura_estimada":{}}
        lista_df = lectura_dataframe_chunk(archivo)
        if lista_df:
            anio_reportado = lista_df[0]["Anio_reportado"][0]
            mes_reportado = lista_df[0]["Mes_reportado"][0]
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
                    if "_CLD" in archivo:
                        for pos in range(len(df)):
                            elemento = df["NIU"][pos]
                            factura = df["ID_factura"][pos]
                            lectura = df["Tipo_lectura"][pos]
                            if elemento not in dic_SAP_CLD:
                                dic_SAP_CLD[elemento] = [factura, lectura]
                            try:
                                lectura_str = str(lectura)
                                if lectura_str == "R" or lectura_str == "1":
                                    if elemento not in dic_NIU_unico["Lectura_real"]:
                                        dic_NIU_unico["Lectura_real"][elemento] = True
                                if lectura_str == "E" or lectura_str == "2":
                                    if elemento not in dic_NIU_unico["Lectura_estimada"]:
                                        dic_NIU_unico["Lectura_estimada"][elemento] = True
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                        proceso_CLD = True
                    elif "_PRD" in archivo:
                        for pos in range(len(df)):
                            elemento = df["NIU"][pos]
                            factura = df["ID_factura"][pos]
                            lectura = df["Tipo_lectura"][pos]
                            if elemento not in dic_SAP_PRD:
                                dic_SAP_PRD[elemento] = [factura, lectura]
                            try:
                                lectura_str = str(lectura)
                                if lectura_str == "R" or lectura_str == "1":
                                    if elemento not in dic_NIU_unico["Lectura_real"]:
                                        dic_NIU_unico["Lectura_real"][elemento] = True
                                if lectura_str == "E" or lectura_str == "2":
                                    if elemento not in dic_NIU_unico["Lectura_estimada"]:
                                        dic_NIU_unico["Lectura_estimada"][elemento] = True
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                        proceso_PRD =True
                    elif "_PRD" not in archivo and "_CLD" not in archivo:
                        for pos in range(len(df)):
                            elemento = df["NIU"][pos]
                            factura = df["ID_factura"][pos]
                            lectura = df["Tipo_lectura"][pos]
                            if elemento not in dic_GRC1:
                                dic_GRC1[elemento] = [factura, lectura]
                            try:
                                lectura_str = str(lectura)
                                if lectura_str == "R" or lectura_str == "1":
                                    if elemento not in dic_NIU_unico["Lectura_real"]:
                                        dic_NIU_unico["Lectura_real"][elemento] = True
                                if lectura_str == "E" or lectura_str == "2":
                                    if elemento not in dic_NIU_unico["Lectura_estimada"]:
                                        dic_NIU_unico["Lectura_estimada"][elemento] = True
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                else:
                    for pos in range(len(df)):
                        elemento = df["NIU"][pos]
                        if elemento not in dic_GRTT2:
                            dic_GRTT2[elemento] = True
                    proceso_GRTT2 = True
            if "GRTT2" not in archivo:
                if dic_conteo["Lectura_real"]+dic_conteo["Lectura_estimada"] == 0:
                    porcentaje_1 = "0 %"
                    porcentaje_2 = "0 %"
                else:
                    porcentaje_1 = str(round((dic_conteo["Lectura_real"]/(dic_conteo["Lectura_real"]+dic_conteo["Lectura_estimada"]))*100,2))+"%"
                    porcentaje_2 = str(round((dic_conteo["Lectura_estimada"]/(dic_conteo["Lectura_real"]+dic_conteo["Lectura_estimada"]))*100,2))+"%"
                dic_df = {"Tipo de Lectura":["R","E"],
                            "Cantidad Lecturas Totales":[dic_conteo["Lectura_real"], dic_conteo["Lectura_estimada"]],
                            "Porcentaje de Lectura":[porcentaje_1, porcentaje_2],
                            "Consumo m3":[dic_conteo["Consumo"], dic_conteo["Consumo"]],
                            "Valor total facturado":[dic_conteo["Valor total facturado"], dic_conteo["Valor total facturado"]],
                            "Usuarios NIU Unicos":[len(dic_NIU_unico["Lectura_real"]),len(dic_NIU_unico["Lectura_estimada"])]}
                df_conteo = pd.DataFrame(dic_df)
                df_conteo["Filial"] = dic_filiales[filial]
                if "_CLD" in archivo:
                    df_conteo["Archivo"] = "GRC1_SAP_CLD"
                elif "_PRD" in archivo:
                    df_conteo["Archivo"] = "GRC1_SAP_PRD"
                else:
                    df_conteo["Archivo"] = "GRC1"
                lista_df_porcentaje.append(df_conteo)
        else:
            return None
    if not (proceso_CLD or proceso_PRD):
        if thread:
            thread.message_sent.emit("No es posible generar el reporte sin el archivo GRC1_PRD o GRC1_CLD", "red")
        else:
            print("\nNo es posible generar el reporte sin el archivo GRC1_PRD o GRC1_CLD\n")
        return None
    df_porcentaje = pd.concat(lista_df_porcentaje, ignore_index=True)
    df_porcentaje["Diff. Porcentual Valor Total Facturado"] = "0 %"
    df_porcentaje["Diff. Porcentual Consumo m3"] = "0 %"
    df_porcentaje["Nuevos NIU"] = 0
    df_GRC1 = df_porcentaje[df_porcentaje["Archivo"] == "GRC1"].reset_index(drop=True)
    if len(df_GRC1) > 0:
        valor_consumo_GRC1 = df_GRC1["Consumo m3"].sum()
        valor_facturado_GRC1 = df_GRC1["Valor total facturado"].sum()
    else:
        valor_consumo_GRC1 = 0
        valor_facturado_GRC1 = 0
    if proceso_CLD:
        df_GRC1_CLD = df_porcentaje[df_porcentaje["Archivo"] == "GRC1_SAP_CLD"].reset_index(drop=True)
        if len(df_GRC1_CLD) > 0:
            valor_consumo_GRC1_CLD = df_GRC1_CLD["Consumo m3"].sum()
            valor_facturado_GRC1_CLD = df_GRC1_CLD["Valor total facturado"].sum()
        else:
            valor_consumo_GRC1_CLD = 0
            valor_facturado_GRC1_CLD = 0
    if proceso_PRD:
        df_GRC1_PRD = df_porcentaje[df_porcentaje["Archivo"] == "GRC1_SAP_PRD"].reset_index(drop=True)
        if len(df_GRC1_PRD) > 0:
            valor_consumo_GRC1_PRD = df_GRC1_PRD["Consumo m3"].sum()
            valor_facturado_GRC1_PRD = df_GRC1_PRD["Valor total facturado"].sum()
        else:
            valor_consumo_GRC1_PRD = 0
            valor_facturado_GRC1_PRD = 0
    porcentaje_consumo_GRC1_CLD = "0 %"
    porcentaje_consumo_GRC1_PRD = "0 %"
    porcentaje_facturado_GRC1_CLD = "0 %"
    porcentaje_facturado_GRC1_PRD = "0 %"
    if proceso_CLD:
        df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_CLD', 'Nuevos NIU'] = len(dic_GRC1)-len(dic_SAP_CLD)
    if proceso_PRD:
        df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_PRD', 'Nuevos NIU'] = len(dic_GRC1)-len(dic_SAP_PRD)
    if valor_consumo_GRC1 > 0:
        if proceso_CLD:
            porcentaje_consumo_GRC1_CLD = str(round((abs(valor_consumo_GRC1_CLD-valor_consumo_GRC1)/valor_consumo_GRC1)*100,2))+" %"
        if proceso_PRD:
            porcentaje_consumo_GRC1_PRD = str(round((abs(valor_consumo_GRC1_PRD-valor_consumo_GRC1)/valor_consumo_GRC1)*100,2))+" %"
    if valor_facturado_GRC1 > 0:
        if proceso_CLD:
            porcentaje_facturado_GRC1_CLD = str(round((abs(valor_facturado_GRC1_CLD-valor_facturado_GRC1)/valor_facturado_GRC1)*100,2))+" %"
            df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_CLD', 'Diff. Porcentual Consumo m3'] = porcentaje_consumo_GRC1_CLD
            df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_CLD', "Diff. Porcentual Valor Total Facturado"] = porcentaje_facturado_GRC1_CLD
        if proceso_PRD:
            porcentaje_facturado_GRC1_PRD = str(round((abs(valor_facturado_GRC1_PRD-valor_facturado_GRC1)/valor_facturado_GRC1)*100,2))+" %"
            df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_PRD', 'Diff. Porcentual Consumo m3'] = porcentaje_consumo_GRC1_PRD
            df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_PRD', "Diff. Porcentual Valor Total Facturado"] = porcentaje_facturado_GRC1_PRD
    df_porcentaje["Anio_reportado"] = anio_reportado
    df_porcentaje["Mes_reportado"] = mes_reportado
    df_porcentaje = df_porcentaje[["Archivo","Filial","Anio_reportado","Mes_reportado","Tipo de Lectura","Cantidad Lecturas Totales","Usuarios NIU Unicos","Porcentaje de Lectura","Consumo m3",
                                    "Valor total facturado",'Diff. Porcentual Consumo m3','Diff. Porcentual Valor Total Facturado',"Nuevos NIU"]]
    nombre = nombre_final.replace("_resumen", "_porcentaje_comparacion_SAP")
    almacenar_df_csv_y_excel(df_porcentaje, nombre, thread=thread)
    dic_total = {"NIU":[],
                "Tipo de lectura GRC1":[],
                "Factura GRC1":[]}
    if proceso_GRTT2:
        dic_total["Existe GRTT2"] = []
    if proceso_CLD:
        dic_total["Tipo de lectura GRC1 CLD"] = []
        dic_total["Factura GRC1 CLD"] = []
        if len(dic_SAP_CLD) > cantidad_datos_excel:
            lista_llaves = list(dic_SAP_CLD.keys())[:cantidad_datos_excel]
            lista_valores = list(dic_SAP_CLD.values())[:cantidad_datos_excel]
        else:
            lista_llaves = list(dic_SAP_CLD.keys())
            lista_valores = list(dic_SAP_CLD.values())
    if proceso_PRD:
        dic_total["Tipo de lectura GRC1 PRD"] = []
        dic_total["Factura GRC1 PRD"] = []
        if len(dic_SAP_PRD) > cantidad_datos_excel:
            lista_llaves = list(dic_SAP_PRD.keys())[:cantidad_datos_excel]
            lista_valores = list(dic_SAP_PRD.values())[:cantidad_datos_excel]
        else:
            lista_llaves = list(dic_SAP_PRD.keys())
            lista_valores = list(dic_SAP_PRD.values())
    for i in range(len(lista_llaves)):
        llave = lista_llaves[i]
        valor = lista_valores[i]
        valor_1 = None
        valor_2 = None
        try:
            valor_1 = dic_GRC1[llave]
            if proceso_PRD:
                valor_2 = dic_SAP_PRD[llave]
            elif proceso_CLD:
                valor_2 = dic_SAP_CLD[llave]
            if valor_1 and valor_2:
                dic_total["Tipo de lectura GRC1"].append(valor_1[1])
                dic_total["Factura GRC1"].append(valor_1[0])
                dic_total["NIU"].append(llave)
                if proceso_PRD:
                    dic_total["Tipo de lectura GRC1 PRD"].append(valor_2[1])
                    dic_total["Factura GRC1 PRD"].append(valor_2[0])
                if proceso_CLD:
                    dic_total["Tipo de lectura GRC1 CLD"].append(valor[1])
                    dic_total["Factura GRC1 CLD"].append(valor[0])
                if proceso_GRTT2:
                    if llave in dic_GRTT2:
                        dic_total["Existe GRTT2"].append(1)
                    else:
                        dic_total["Existe GRTT2"].append(2)
        except KeyError:
            pass
    try:
        df_total = pd.DataFrame(dic_total)
        nombre_final = nombre_final.replace("_resumen", "_total_comparacion_SAP")
        df_total["Anio_reportado"] = anio_reportado
        df_total["Mes_reportado"] = mes_reportado
        df_total["Filial"] = dic_filiales[filial]
        almacenar_df_csv_y_excel(df_total, nombre_final, thread=thread)
    except ValueError:
        pass

def reporte_comparacion_prd_cld_cer(dic_archivos, seleccionar_reporte, informar, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                if len(lista_archivos_filial) > 1:
                    apoyo_reporte_comparacion_prd_cld_cer(lista_archivos_filial, informar, filial, thread=thread)
                else:
                    if thread:
                        thread.message_sent.emit("Se necesitan al menos 2 archivos para generar la comparación entre reportes comerciales GRC1", "red")
                    else:
                        print(f"Se necesitan al menos 2 archivos para generar la comparación entre reportes comerciales GRC1")

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

def apoyo_reporte_comparacion_p1_p2(lista_archivos, informar, cantidad_filas, p1, p2, thread=None):
    proceso_1 = True
    proceso_2 = True
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
        if p1 in archivo and p2 not in archivo:
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
                    return None
            proceso_1 = True
        if p2 in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            dic_dataframe_CLD = {}
            if lista_df:
                for df in lista_df:
                    df1 = df[lista_1]
                    for i in range(len(df1)):
                        dic_dataframe_CLD[df1["ID_factura"][i]] = df1.iloc[i].tolist()
            else:
                return None
            proceso_2 = True
    if proceso_1 and proceso_2:
        if p1 == "GRC1_":
            p1 = "_CER"
        lista_iguales = []
        lista_diferentes = []
        for llave in dic_dataframe:
            try:
                diferentes,valor,conteo = listas_diferentes(dic_dataframe[llave], dic_dataframe_CLD[llave],llave)
                if diferentes:
                    lista_diferentes.append(valor)
                else:
                    lista_iguales.append(valor)
            except BaseException:
                pass
        largo = len(lista_1)
        texto = f"Para {len(lista_iguales)+len(lista_diferentes)} filas evaluadas: {len(lista_iguales)} filas iguales, {len(lista_diferentes)} filas diferentes"
        if thread:
            thread.message_sent.emit(texto, "orange")
        else:
            print(texto)
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
        nombre = nombre_archivo.replace("_resumen", f"_comparacion_iguales{p1}{p2}")
        almacenar_df_csv_y_excel(df_iguales, nombre, thread=thread)
        for dic in lista_diferentes:
            for lista in dic.values():
                for i in range(len(lista)):
                    lista_df_diferentes[i].append((lista[i][0],lista[i][1]))
        dic_df_diferentes = {}
        for i in range(largo):
            dic_df_diferentes[lista_1[i]] = lista_df_diferentes[i]
        df_diferentes = pd.DataFrame(dic_df_diferentes)
        nombre = nombre_archivo.replace("_resumen", f"_comparacion_diferentes{p1}{p2}")
        almacenar_df_csv_y_excel(df_diferentes, nombre, almacenar_excel=False, thread=thread)
        for dic in lista_diferentes:
            for lista in dic.values():
                for i in range(len(lista)):
                    lista_df_diferentes_excel[i].append(lista[i])
        dic_df_diferentes_excel = {}
        for i in range(largo):
            dic_df_diferentes_excel[lista_1[i]] = lista_df_diferentes_excel[i]
        df_diferentes_excel = pd.DataFrame(dic_df_diferentes_excel)
        nombre = nombre_archivo.replace("_resumen", f"_comparacion_diferentes{p1}{p2}").replace(".csv",".xlsx")
        almacenar = mod_5.almacenar_csv_en_excel_patrones(df_diferentes_excel, nombre,"Datos")
        if informar and almacenar:
            informar_archivo_creado(nombre, True, thread=thread)
    else:
        if thread:
            thread.message_sent.emit(f"Deben existir los archivos {p1} y {p2} para el proceso de comparacion", "white")
        else:
            print(f"\nDeben existir los archivos {p1} y {p2} para el proceso de comparacion\n")

def reporte_comparacion_SAP(dic_archivos, seleccionar_reporte, informar, cantidad_filas, p1, p2, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                if len(lista_archivos_filial) > 1:
                    apoyo_reporte_comparacion_p1_p2(lista_archivos_filial, informar, cantidad_filas, p1, p2, thread=thread) #Colocar SIEMPRE primero GRC1, PRD / GRC1, PRD / PRD, CLD
                else:
                    if thread:
                        thread.message_sent.emit("Se necesitan al menos 2 archivos para generar la comparación entre reportes comerciales GRC1", "red")
                    else:
                        print(f"Se necesitan al menos 2 archivos para generar la comparación entre reportes comerciales GRC1")

def generar_sumatoria_df(df):
    columnas = list(df.columns)
    lista_df = []
    lista_filiales = list(df["Filial"].unique())
    columnas_valores = ["Cantidad de usuarios","Consumo m3","Valor total facturado","Valor consumo facturado",
                        "Cantidad de facturas","Subsidios","Contribuciones"]
    for filial in lista_filiales:
        df_filial = df[df["Filial"] == filial].reset_index(drop=True)
        if len(df_filial):
            nueva_fila_final = []
            df_total = df_filial[df_filial["Sector de consumo"] == "Total"].reset_index(drop=True)
            for columna in columnas:
                if columna in columnas_valores:
                    nueva_fila_final.append(df_total[columna].sum())
                elif columna in ["NIT","Filial","Anio reportado","Mes reportado"]:
                    nueva_fila_final.append(df_total[columna][0])
                else:
                    nueva_fila_final.append("Total")
            df_filial.loc[len(df_filial)] = nueva_fila_final
            lista_df.append(df_filial)
    if len(lista_df):
        df_total = pd.concat(lista_df, ignore_index=True)
        lista_tipo_usuarios = list(df_total["Tipo de usuario"].unique())
        lista_tipo_usuarios.remove("Total")
        for tipo_usuario in lista_tipo_usuarios:
            df_final = df_total[(df_total["Sector de consumo"] == "Total") & (df_total["Tipo de usuario"] == tipo_usuario)].reset_index(drop=True)
            if len(df_final):
                nueva_fila_final = []
                for columna in columnas:
                    if columna in columnas_valores:
                        nueva_fila_final.append(df_final[columna].sum())
                    elif columna in ["Anio reportado","Mes reportado"]:
                        nueva_fila_final.append(df_final[columna][0])
                    elif columna in ["NIT","Filial"]:
                        nueva_fila_final.append(grupo_vanti)
                    elif columna == "Tipo de usuario":
                        nueva_fila_final.append(tipo_usuario)
                    else:
                        nueva_fila_final.append("Total")
                df_total.loc[len(df_total)] = nueva_fila_final
        df_final = df_total[(df_total["Sector de consumo"] == "Total") & ((df_total["Tipo de usuario"] == "Total"))].reset_index(drop=True)
        nueva_fila_final = []
        for columna in columnas:
            if columna in columnas_valores:
                nueva_fila_final.append(df_final[columna].sum())
            elif columna in ["Anio reportado","Mes reportado"]:
                nueva_fila_final.append(df_final[columna][0])
            elif columna in ["NIT","Filial"]:
                nueva_fila_final.append(grupo_vanti)
            else:
                nueva_fila_final.append("Total")
        df_total.loc[len(df_total)] = nueva_fila_final
        df_total = lista_porcentaje_dataframe(df_total)
        return df_total, True
    else:
        return None, None

def aux_lista_porcentaje_dataframe(df_filial, columna):
    dic = {}
    lista_porcentaje = []
    lista_tipo_usuario = list(df_filial["Tipo de usuario"].unique())
    for tipo_usuario in lista_tipo_usuario:
        df_total = df_filial[(df_filial["Tipo de usuario"] == tipo_usuario) & (df_filial["Sector de consumo"]=="Total")].reset_index(drop=True)
        dic[tipo_usuario] = float(df_total[columna][0])
    lista_tipo_usuario.remove("Total")
    for tipo_usuario in lista_tipo_usuario:
        df_usuario = df_filial[(df_filial["Tipo de usuario"] == tipo_usuario) & (df_filial["Sector de consumo"] != "Total")].reset_index(drop=True)
        lista_sector_consumo = list(df_usuario["Sector de consumo"].unique())
        for sector_consumo in lista_sector_consumo:
            df_sector_consumo = df_usuario[df_usuario["Sector de consumo"] == sector_consumo].reset_index(drop=True)
            valor = float(df_sector_consumo[columna][0])
            if dic[tipo_usuario] > 0:
                porcentaje = round((valor/dic[tipo_usuario])*100,2)
            else:
                porcentaje = 0
            lista_porcentaje.append(str(porcentaje)+" %")
    for tipo_usuario in lista_tipo_usuario:
        df_usuario = df_filial[(df_filial["Tipo de usuario"] == tipo_usuario) & (df_filial["Sector de consumo"] == "Total")].reset_index(drop=True)
        valor = float(df_usuario[columna][0])
        if dic["Total"] > 0:
            porcentaje = round((valor/dic["Total"])*100,2)
        else:
            porcentaje = 0
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

def apoyo_reporte_usuarios_filial(lista_archivos,informar,filial,almacenar_excel=True, usuarios_unicos=True, thread=None):
    proceso_GRTT2 = False
    proceso_GRC1 = False
    for archivo in lista_archivos:
        if "GRTT2" in archivo:
            nombre = archivo
            lista_df = lectura_dataframe_chunk(archivo)
            dic_dataframe = {}
            dic_dataframe_NIU = {}
            if lista_df:
                proceso_GRTT2 = True
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                for i in range(len(lista_df)):
                    df = lista_df[i].copy()
                    df = df[["NIU","Codigo_DANE","Direccion","Cedula_Catastral","Estrato","Longitud","Latitud","Estado"]]
                    df["Estrato"] = df["Estrato"].fillna(0).astype(int)
                    df["Estado"] = df["Estado"].fillna(0).astype(int)
                    lista_estrato_texto = []
                    for j in range(len(df)):
                        try:
                            estrato_texto = tabla_3["datos"][str(df["Estrato"][j])]
                            lista_estrato_texto.append(estrato_texto)
                            if int(df["Estrato"][j]) not in dic_dataframe:
                                dic_dataframe[int(df["Estrato"][j])] = 0
                            dic_dataframe[int(df["Estrato"][j])] += 1
                        except BaseException:
                            lista_estrato_texto.append("")
                        valor = df["NIU"][j]
                        estado = df["Estado"][j]
                        if valor not in dic_dataframe_NIU:
                            dic_dataframe_NIU[valor] = [1, [estado]] #Cantidad de apariciones de NIU, Estado cuenta (1=Sí, 2=No)
                        else:
                            dic_dataframe_NIU[valor][0] += 1
                            if estado not in dic_dataframe_NIU[valor][1]:
                                dic_dataframe_NIU[valor][1].append(estado)
                    df["Estrato"] = lista_estrato_texto
                    lista_df[i] = df
        elif "GRC1" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            dic_dataframe_NIU_GRC1 = {}
            if lista_df:
                proceso_GRC1 = True
                for df in lista_df:
                    for i in range(len(df)):
                        valor = df["NIU"][i]
                        if valor not in dic_dataframe_NIU_GRC1:
                            dic_dataframe_NIU_GRC1[valor] = True
    if proceso_GRTT2 and proceso_GRC1:
        if usuarios_unicos:
            dic_df_NIU_GRTT2_GRC1 = {"NIU":[],
                                        "Apariciones_GRTT2":[],
                                        "Existe_GRC1":[],
                                        "Estado_cuenta":[]}
            for llave, valor in dic_dataframe_NIU.items():
                dic_df_NIU_GRTT2_GRC1["NIU"].append(llave)
                dic_df_NIU_GRTT2_GRC1["Apariciones_GRTT2"].append(valor[0])
                if len(valor[1]) > 1:
                    dic_df_NIU_GRTT2_GRC1["Estado_cuenta"].append(f"{valor[1][0]} - {valor[1][1]}")
                else:
                    dic_df_NIU_GRTT2_GRC1["Estado_cuenta"].append(valor[1][0])
                if llave in dic_dataframe_NIU_GRC1:
                    dic_df_NIU_GRTT2_GRC1["Existe_GRC1"].append(1)
                else:
                    dic_df_NIU_GRTT2_GRC1["Existe_GRC1"].append(2)
            df_NIU_GRTT2_GRC1 = pd.DataFrame(dic_df_NIU_GRTT2_GRC1)
            df_NIU_GRTT2_GRC1["Mes_reportado"] = mes_reportado
            df_NIU_GRTT2_GRC1["Anio_reportado"] = anio_reportado
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            nombre = lista_a_texto(lista_nombre,"\\")
            almacenar_df_csv_y_excel(df_NIU_GRTT2_GRC1, nombre.replace("_resumen","_inventario_suscriptores_activos"), almacenar_excel=False, thread=thread)
        nombre = nombre.replace("_resumen","_inventario_suscriptores_sector_consumo")
        dic_dataframe = dict(sorted(dic_dataframe.items()))
        dic_dataframe_texto = {}
        for i,j in dic_dataframe.items():
            dic_dataframe_texto[tabla_3["datos"][str(i)]] = j
        dic_dataframe_texto = {"Estrato":list(dic_dataframe_texto.keys()),
                                "Cantidad de usuarios":list(dic_dataframe_texto.values())}
        df_filial_resumen = pd.DataFrame(dic_dataframe_texto)
        df_filial_resumen["Filial"] = dic_filiales[filial]
        df_filial_resumen["NIT"] = dic_nit[dic_filiales[filial]]
        df_filial_resumen["Mes_reportado"] = mes_reportado
        df_filial_resumen["Anio_reportado"] = anio_reportado
        almacenar_df_csv_y_excel(df_filial_resumen, nombre, thread=thread)
        return df_filial_resumen, nombre
    else:
        return None,None

def generar_listas_fechas(lista_fechas):
    lista_final = []
    for i in range(1,len(lista_fechas)):
        lista_final.append((lista_fechas[i-1],lista_fechas[i]))
    return lista_final

def encontrar_errores_inventario_suscriptores(dic_archivos, seleccionar_reporte, thread=None):
    lista_fechas = generar_listas_fechas(list(dic_archivos.keys()))
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for union in lista_fechas:
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            proceso_GRTT2 = False
            proceso_GRTT2SAP = False
            for archivo in dic_archivos[union[0]]:
                if "GRTT2" in archivo and "SAP" not in archivo and filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                proceso_GRTT2 = True
            for archivo in dic_archivos[union[1]]:
                if "GRTT2SAP" in archivo and filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial) == 2:
                proceso_GRTT2SAP = True
            if proceso_GRTT2SAP and proceso_GRTT2:
                apoyo_encontrar_errores_inventario_suscriptores(lista_archivos_filial,filial, union[0], thread=thread)
            else:
                if thread:
                    thread.message_sent.emit(f"No es posible generar el reporte. Deben existir los archivos de los periodos {union[0]} y {union[1]}", "red")
                else:
                    print(f"No es posible generar el reporte. Deben existir los archivos de los periodos {union[0]} y {union[1]}")

def unir_archivos_csv(arc_1, arc_2, nombre):
    lista_arc_1 = lectura_dataframe_chunk(arc_1)
    lista_arc_2 = lectura_dataframe_chunk(arc_2)
    columnas = list(lista_arc_1[0].columns)
    lista_total = []
    try:
        for i in lista_arc_1:
            lista_total.append(i.copy())
        for i in lista_arc_2:
            i = i[columnas]
            lista_total.append(i.copy())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            df_total = pd.concat(lista_total, ignore_index=True)
        almacenar_df_csv_y_excel(df_total, nombre, almacenar_excel=False, informar=False)
        return True
    except BaseException:
        return False

def corregir_errores_inventario_suscriptores(dic_archivos, seleccionar_reporte, thread=None):
    lista_fechas = generar_listas_fechas(list(dic_archivos.keys()))
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for union in lista_fechas:
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            proceso_GRTT2 = False
            proceso_GRTT2SAP = False
            for archivo in dic_archivos[union[0]]:
                if "GRTT2" in archivo and "SAP" not in archivo and filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                proceso_GRTT2 = True
            for archivo in dic_archivos[union[1]]:
                if "GRTT2SAP" in archivo and filial in archivo:
                    n1 = archivo.replace("_resumen","_completo")
                    n2 = archivo.replace("_resumen","_error")
                    n3 = archivo.replace("_resumen","_apoyo_error")
                    if os.path.exists(n1) and os.path.exists(n2):
                        proceso = unir_archivos_csv(n1, n2, n3)
                        if proceso:
                            lista_archivos_filial.append(n3)
            if len(lista_archivos_filial) == 2:
                proceso_GRTT2SAP = True
            if proceso_GRTT2SAP and proceso_GRTT2:
                apoyo_encontrar_errores_inventario_suscriptores(lista_archivos_filial,filial, union[0], thread=thread)
                eliminar_archivos([n3])
            else:
                if thread:
                    thread.message_sent.emit(f"No es posible corregir los errores. Deben existir los archivos (_resumen.csv, _completo.csv, _error.csv) de los periodos {union[0]} y {union[1]}\nLos archivos deben cumplir con la estructura de certificación del GRTT2", "red")
                else:
                    print(f"No es posible corregir los errores. Deben existir los archivos (_resumen.csv, _completo.csv, _error.csv) de los periodos {union[0]} y {union[1]}\nLos archivos deben cumplir con la estructura de certificación del GRTT2")

def listas_iguales(lista_1, lista_2):
    l1 = len(lista_1)
    l2 = len(lista_2)
    lista_cambios = []
    if l1 == l2:
        for i in range(1, l1-1):
            if i != 11 and i != 12:
                if lista_1[i] != lista_2[i]:
                    lista_cambios.append(i)
            else:
                if lista_1[i] == "" and lista_2[i] != "":
                    lista_cambios.append(i+1)
        texto_cambios = lista_a_texto(lista_cambios, " y ")
        if len(lista_cambios):
            return True, lista_2, texto_cambios
        else:
            return False, lista_1, texto_cambios
    else:
        return False, lista_1, ""

def convertir_fecha(fecha):
    fecha = str(fecha)
    if fecha == "0":
        return ""
    else:
        fecha_str = str(fecha).zfill(8)
        dia = fecha_str[0:2]
        mes = fecha_str[2:4]
        anio = fecha_str[4:]
        return f"{dia}-{mes}-{anio}"

def errores_lista(lista, indicador_SUI_filial, dic_filial_mercado, dic_filial_DANE):
    columnas_error = []
    largo = len(lista)
    for i in range(1, largo-1):
        if i == 1:
            if lista[i] != 1:
                columnas_error.append(i+1)
        elif i == 2:
            if lista[i] != indicador_SUI_filial:
                columnas_error.append(i+1)
        elif i == 3:
            if lista[i] not in dic_filial_mercado:
                columnas_error.append(i+1)
        elif i == 4:
            if lista[i] not in dic_filial_DANE:
                columnas_error.append(i+1)
        elif i == 6:
            if not len(lista[i]):
                columnas_error.append(i+1)
        elif i == 9:
            if lista[i] not in tabla_3_data:
                columnas_error.append(i+1)
        elif i == 10:
            if lista[i] >= 6000 or lista[i] < 0:
                columnas_error.append(i+1)
        elif i == 13:
            if lista[i] not in tabla_30:
                columnas_error.append(i+1)
        else:
            if largo > 17:
                if i == 20:
                    if lista[i] == "Gasificado" or lista[i] == "Potencial":
                        columnas_error.append(i+1)
    if len(columnas_error):
        lista.append(lista_a_texto(columnas_error, "-"))
    else:
        lista.append("")
    return lista

def apoyo_encontrar_errores_inventario_suscriptores(lista_archivos, filial, fecha, thread=None):
    if len(lista_archivos) == 2:
        filas_minimas = ["NIU","ID_Comercializador","ID_Mercado"]
        columnas_GRTT2 = leer_archivos_json(ruta_constantes+"/GRTT2.json")["seleccionados"]
        archivo_previo = lista_archivos[0]
        archivo_SAP = lista_archivos[1]
        dic_error = {}
        lista_df_SAP = lectura_dataframe_chunk(archivo_SAP)
        lista_df_previo = lectura_dataframe_chunk(archivo_previo)
        columnas_SAP = list(lista_df_SAP[0].columns)[:-2]
        indicador_SUI_filial = indicador_SUI[filial]
        dic_filial_mercado = mercado_relevante_id[str(indicador_SUI_filial)]
        dic_filial_DANE = mercado_relevante_DANE[str(indicador_SUI_filial)]
        fecha = fecha.split(" - ")
        mes = fecha[1]
        anio = fecha[0]
        pos_mes = lista_meses.index(mes)+1
        if pos_mes < 10:
            pos_mes = "0" + str(pos_mes)
        else:
            pos_mes = str(pos_mes)
        inicio_mes = f"01-{pos_mes}-{anio}"
        inicio_mes_dt = pd.to_datetime(inicio_mes, dayfirst=True)
        inicio_mes_str = inicio_mes_dt.strftime('%d-%m-%Y')
        lista_df_previo = lectura_dataframe_chunk(archivo_previo)
        dic_NIU_SAP = {}
        dic_NIU_previo = {}
        lista_aceptado = []
        if lista_df_SAP and lista_df_previo:
            #lista_df_catastro = []
            for i in range(len(lista_df_SAP)):
                df = lista_df_SAP[i].copy()
                df = df.reset_index(drop=True)
                columnas = list(df.columns)
                df["NIU"] = pd.to_numeric(df["NIU"], errors='coerce').fillna(0).astype(int)
                if "Codigo_SAP" in columnas:
                    df["Codigo_SAP"] = pd.to_numeric(df["Codigo_SAP"], errors='coerce').fillna(0).astype(int)
                df["Tipo_usuario"] = pd.to_numeric(df["Tipo_usuario"], errors='coerce').fillna(0).astype(int)
                df["ID_Comercializador"] = pd.to_numeric(df["ID_Comercializador"], errors='coerce').fillna(0).astype(int)
                df["ID_Comercializador"] = df["ID_Comercializador"].astype(str)
                df["ID_Mercado"] = pd.to_numeric(df["ID_Mercado"], errors='coerce').fillna(0).astype(int)
                df["ID_Mercado"] = df["ID_Mercado"].astype(str)
                df["Codigo_DANE"] = pd.to_numeric(df["Codigo_DANE"], errors='coerce').fillna(0).astype(int)
                df["Codigo_DANE"] = df["Codigo_DANE"].astype(str)
                df["Codigo_DANE"] = df["Codigo_DANE"].apply(completar_codigo_DANE)
                df["Ubicacion"] = df["Ubicacion"].astype(str)
                df["Ubicacion"] = df["Ubicacion"].str.upper()
                df["Ubicacion"] = df["Ubicacion"].apply(
                            lambda x: 1 if x=="R" else
                                    3 if x=="C" else 2)
                df["Direccion"] = df["Direccion"].astype(str)
                df["Direccion"] = df["Direccion"].str.replace(r"\s{2,}", "", regex=True)
                df["Direccion"] = df["Direccion"].fillna("")
                df["Cedula_Catastral"] = df["Cedula_Catastral"].apply(lambda x: int(Decimal(x)) if pd.notna(x) and str(x).replace('.', '', 1).isdigit() else Decimal(0))
                df["Cedula_Catastral"] = df["Cedula_Catastral"].astype(str).replace("0", "").replace("nan", "")
                df["Estrato"] = pd.to_numeric(df["Estrato"], errors='coerce').fillna(0).astype(int)
                df["Estrato"] = df["Estrato"].astype(str)
                df["Altitud"] = pd.to_numeric(df["Altitud"], errors="coerce").fillna(0).astype(int)
                df["Latitud"] = pd.to_numeric(df["Latitud"], errors="coerce").fillna(-100).astype(float)
                df["Latitud"] = df["Latitud"].apply(lambda x: -100 if x > 12.462778 or x < -4.225 else x)
                df["Latitud"] = df["Latitud"].round(15)
                df["Longitud"] = pd.to_numeric(df["Longitud"], errors="coerce").fillna(-100).astype(float)
                df["Longitud"] = df["Longitud"].apply(lambda x: -100 if x > -66.848333 or x < -79.006389 else x)
                df["Longitud"] = df["Longitud"].round(15)
                df["Latitud"] = df["Latitud"].apply(lambda x: "" if x == -100 else x)
                df["Longitud"] = df["Longitud"].apply(lambda x: "" if x == -100 else x)
                with warnings.catch_warnings():
                    warnings.simplefilter(action='ignore', category=FutureWarning)
                    mask_latitud = df["Latitud"] == ""
                    mask_longitud = df["Longitud"] == ""
                    df.loc[mask_latitud, "Longitud"] = ""
                    df.loc[mask_longitud, "Latitud"] = ""
                    #df.loc[mask_latitud, "Altitud"] = 0
                    #df.loc[mask_longitud, "Altitud"] = 0
                df["Estado"] = pd.to_numeric(df["Estado"], errors='coerce').fillna(0).astype(int)
                df["Estado"] = df["Estado"].astype(str)
                df.loc[(df['Codigo_DANE'] == '11001000') & (df['Cedula_Catastral'].str.len() == 12), 'Cedula_Catastral'] = df.loc[(df['Codigo_DANE'] == '11001000') & (df['Cedula_Catastral'].str.len() == 12), 'Cedula_Catastral'].str.zfill(21)
                df.loc[(df['Codigo_DANE'] == '11001000') & (df['Cedula_Catastral'].str.len() != 21), 'Cedula_Catastral'] = "0"
                df['Informacion_predial_actualizada'] = df['Cedula_Catastral'].apply(
                    lambda x: 2 if len(x) == 30 else
                            1 if len(x) == 21 else 4)
                #df_catastro = df[df["Informacion_predial_actualizada"]==4]
                #lista_df_catastro.append(df_catastro)
                df['Cedula_Catastral'] = np.where(df['Informacion_predial_actualizada'] == 4, 0, df['Cedula_Catastral'])
                df["Fecha_ajuste"] = inicio_mes_str
                if "STS_Regularizacion" in columnas:
                    df["STS_Regularizacion"] = df["STS_Regularizacion"].str.capitalize()
                for col in columnas_SAP:
                    if col == "NIU":
                        df_filter = df[df[col] > 0].reset_index(drop=True)
                        df_error = df[df[col] == 0].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "Tipo_usuario":
                        df_filter = df[df[col] == 1].reset_index(drop=True)
                        df_error = df[df[col] != 1].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "ID_Comercializador":
                        df_filter = df[df[col] == indicador_SUI_filial].reset_index(drop=True)
                        df_error = df[df[col] != indicador_SUI_filial].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "ID_Mercado":
                        df_filter = df[df[col].isin(dic_filial_mercado)].reset_index(drop=True)
                        df_error = df[~df[col].isin(dic_filial_mercado)].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "Codigo_DANE":
                        df_filter = df[df[col].isin(dic_filial_DANE)].reset_index(drop=True)
                        df_error = df[~df[col].isin(dic_filial_DANE)].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "Ubicacion":
                        df_filter = df.copy()
                    elif col == "Direccion":
                        df_filter = df[~(df[col].isna()) & ~(df[col] == '') & ~(df[col]==' ')].reset_index(drop=True)
                        df_error = df[df[col].isna() | (df[col] == ' ') | (df[col]=='')].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "Cedula_Catastral":
                        df_filter = df.copy()
                    elif col == "Estrato":
                        df_filter = df[df[col].isin(tabla_3_data)].reset_index(drop=True)
                        df_error = df[~df[col].isin(tabla_3_data)].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "Altitud":
                        df_filter = df[(df[col] >= 0) & (df[col] < 6000)].reset_index(drop=True)
                        df_error = df[(df[col] < 0) | (df[col] >= 6000)].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "Estado":
                        df_filter = df[df[col].isin(tabla_30)].reset_index(drop=True)
                        df_error = df[~df[col].isin(tabla_30)].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    elif col == "STS_Regularizacion":
                        df[col] = df[col].str.capitalize()
                        df_filter = df[(df[col]!="Potencial") & (df[col]!="Gasificado")].reset_index(drop=True)
                        df_error = df[(df[col]=="Gasificado") | (df[col]=="Potencial")].reset_index(drop=True)
                        if len(df_error):
                            if col not in dic_error:
                                dic_error[col] = []
                            dic_error[col].append(df_error)
                    df = df_filter.copy()
                lista_aceptado.append(df)
            #lista_archivo = archivo_SAP.split("\\")
            #df_SAP_catastro = pd.concat(lista_df_catastro, ignore_index=True)
            #lista_archivo[-1] = lista_archivo[-1].replace("_resumen","_ajuste_catastro")
            #nombre_catastro = lista_a_texto(lista_archivo, "\\")
            #almacenar_df_csv_y_excel(df_SAP_catastro, nombre_catastro, almacenar_excel=False)
            df_SAP_preliminar = pd.concat(lista_aceptado, ignore_index=True)
            df_SAP_preliminar = df_SAP_preliminar[columnas_GRTT2]
            df_SAP_preliminar["Tipo_usuario"] = pd.to_numeric(df_SAP_preliminar["Tipo_usuario"], errors='coerce').fillna(0).astype(int)
            df_SAP_preliminar["ID_Comercializador"] = pd.to_numeric(df_SAP_preliminar["ID_Comercializador"], errors='coerce').fillna(0).astype(int)
            df_SAP_preliminar["ID_Mercado"] = pd.to_numeric(df_SAP_preliminar["ID_Mercado"], errors='coerce').fillna(0).astype(int)
            df_SAP_preliminar["Estrato"] = pd.to_numeric(df_SAP_preliminar["Estrato"], errors='coerce').fillna(0).astype(int)
            df_SAP_preliminar["Estado"] = pd.to_numeric(df_SAP_preliminar["Estado"], errors='coerce').fillna(0).astype(int)
            for i in range(len(df_SAP_preliminar)):
                niu = df_SAP_preliminar["NIU"][i]
                if niu > 0:
                    if str(niu) not in dic_NIU_SAP:
                        dic_NIU_SAP[str(niu)] = df_SAP_preliminar.iloc[i].tolist()
            for df in lista_df_previo:
                df = df.reset_index(drop=True)
                df = df[columnas_GRTT2]
                df["Codigo_DANE"] = df["Codigo_DANE"].astype(str)
                df["Codigo_DANE"] = df["Codigo_DANE"].apply(completar_codigo_DANE)
                df["Cedula_Catastral"] = df["Cedula_Catastral"].apply(lambda x: int(Decimal(x)) if pd.notna(x) and str(x).replace('.', '', 1).isdigit() else Decimal(0))
                df["Cedula_Catastral"] = df["Cedula_Catastral"].astype(str)
                df['Fecha_ajuste'] = df['Fecha_ajuste'].astype(str).replace('-', "").replace('/', '').replace('_', '')
                df["Fecha_ajuste"] = df["Fecha_ajuste"].fillna(0).astype(int)
                df['Fecha_ajuste'] = df['Fecha_ajuste'].apply(convertir_fecha)
                df['Fecha_ajuste'] = pd.to_datetime(df['Fecha_ajuste'], errors='coerce', dayfirst=True).dt.strftime('%d-%m-%Y').fillna('')
                for i in range(len(df)):
                    niu = df["NIU"][i]
                    if niu > 0:
                        if str(niu) not in dic_NIU_previo:
                            dic_NIU_previo[str(niu)] = df.iloc[i].tolist()
            if len(dic_error):
                lista_df_error = []
                dic_error_2 = {}
                total = 0
                for col, lista_df in dic_error.items():
                    columnas_minimas = filas_minimas.copy()
                    if col not in columnas_minimas:
                        columnas_minimas.append(col)
                    columnas_minimas.append("Columna_error")
                    df_unido = pd.concat(lista_df, ignore_index=True)
                    df_unido['Fecha_ajuste'] = pd.to_datetime(df_unido['Fecha_ajuste'], errors='coerce', dayfirst=True).dt.strftime('%d-%m-%Y').fillna('')
                    lista_df_error.append(df_unido)
                    df_unido_2 = df_unido.copy()
                    df_unido_2["Columna_error"] = col
                    df_unido_2 = df_unido_2[columnas_minimas]
                    largo = len(df_unido_2)
                    total += largo
                    if largo > 150:
                        df_unido_2 = df_unido_2.head(150)
                    if largo == 1:
                        texto = f"1 error en la columna {col}."
                    else:
                        texto = f"{largo} errores en la columna {col}."
                    dic_error_2[col] = [texto, df_unido_2.copy()]
                lista_archivo = archivo_SAP.split("\\")
                lista_archivo[-1] = "log_errores_"+lista_archivo[-1]
                nombre_error = lista_a_texto(lista_archivo, "\\").replace("_resumen","").replace("_apoyo_error","")
                nombre_error_doc = nombre_error.replace(".csv",".docx")
                nombre_error_pdf = nombre_error.replace(".csv",".pdf")
                op = mod_8.almacenar_errores(dic_error_2, filial, indicador_SUI[filial], mes, anio, nombre_error_doc, total, "GRTT2", "", thread=thread)
                if op:
                    informar_archivo_creado(nombre_error_pdf, True, thread=thread)
                else:
                    if thread:
                        thread.message_sent.emit(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}", "red")
                    else:
                        print(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}")
                df_error = pd.concat(lista_df_error, ignore_index=True)
                columnas = list(df_error.columns)
                columnas.append("Columna_error")
                lista_errores = []
                for i in range(len(df_error)):
                    lista_errores.append(errores_lista(df_error.iloc[i].tolist(), indicador_SUI_filial, dic_filial_mercado, dic_filial_DANE))
                df_error_col = pd.DataFrame(lista_errores, columns=columnas)
                nombre = archivo_SAP.replace("_resumen","_error").replace("_apoyo_error","_error")
                almacenar_df_csv_y_excel(df_error_col, nombre, almacenar_excel=False, thread=thread)
            lista_cambios = []
            lista_nuevos = []
            lista_completo = []
            lista_comparacion = []
            for niu in dic_NIU_SAP:
                lista_sap = dic_NIU_SAP[niu]
                if niu in dic_NIU_previo:
                    op, lista, texto_cambios = listas_iguales(dic_NIU_previo[niu], lista_sap)
                    if op:
                        lista_cambios.append(lista)
                        lista_comparacion.append([niu, texto_cambios])
                    lista_completo.append(lista)
                else:
                    lista_cambios.append(lista_sap)
                    lista_completo.append(lista_sap)
                    lista_nuevos.append(lista_sap)
            df_cambios = pd.DataFrame(lista_comparacion, columns=["NIU","Cambios"])
            nombre = archivo_SAP.replace("_resumen","_cambios").replace("_apoyo_error","_cambios")
            almacenar_df_csv_y_excel(df_cambios, nombre, almacenar_excel=False, thread=thread)
            df_completo = pd.DataFrame(lista_completo, columns=columnas_GRTT2)
            nombre = archivo_SAP.replace("_resumen","_completo").replace("_apoyo_error","_completo")
            almacenar_df_csv_y_excel(df_completo, nombre, almacenar_excel=False, thread=thread)
            df_procesado = pd.DataFrame(lista_cambios, columns=columnas_GRTT2)
            nombre = archivo_SAP.replace("_resumen","_procesado").replace("_apoyo_error","_procesado")
            almacenar_df_csv_y_excel(df_procesado, nombre, almacenar_excel=False, thread=thread)
            df_nuevo = pd.DataFrame(lista_nuevos, columns=columnas_GRTT2)
            nombre = archivo_SAP.replace("_resumen","_nuevo").replace("_apoyo_error","_nuevo")
            almacenar_df_csv_y_excel(df_nuevo, nombre, almacenar_excel=False, thread=thread)

def reporte_usuarios_filial(dic_archivos, seleccionar_reporte, informar, almacenar_excel=True, usuarios_unicos=True, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df1,nombre = apoyo_reporte_usuarios_filial(lista_archivos_filial,informar,filial, usuarios_unicos=usuarios_unicos, thread=thread)
                if nombre:
                    lista_df_filiales.append(df1)
        if len(lista_archivos_filial) > 0 and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales, ignore_index=True)
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            lista_nombre.pop(-2)
            lista_nombre[-4] = "05. REPORTES_GENERADOS_APLICATIVO"
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, almacenar_excel=almacenar_excel, thread=thread)

def apoyo_generar_reporte_compensacion_mensual(lista_archivos,informar,filial,inventario,thread=None):
    proceso1 = False
    df1 = pd.DataFrame()
    nombre = None
    for archivo in lista_archivos:
        if "GRC3" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                nombre = archivo
                dic_df = {"Mes_compensado":[],"Anio_compensado":[],"CI":[],"Usuarios_compensados":[],"Valor_compensado":[]}
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                for df in lista_df:
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
                almacenar_df_csv_y_excel(df1, nombre.replace("_resumen","_compilado_compensacion"), thread=thread)
                proceso1=True
            else:
                return None,None
    if proceso1 and inventario:
        for archivo in lista_archivos:
            if "GRTT2" in archivo:
                lista_df = lectura_dataframe_chunk(archivo)
                dic_GRTT2 = {}
                if lista_df:
                    columnas = ["NIU","Codigo_DANE","Estrato","Longitud","Latitud","ID_Mercado"]
                    for df in lista_df:
                        df = df[columnas]
                        df = df[df['Estrato'].apply(lambda x: isinstance(x, int))].reset_index(drop=True)
                        for j in range(len(df)):
                            valor_NIU = df["NIU"][j]
                            if valor_NIU not in dic_GRTT2:
                                dic_GRTT2[valor_NIU] = df.iloc[j].tolist()
                    columnas_compen = list(df_compensacion.columns)
                    columnas_df = columnas_compen.copy()
                    columnas_df.extend(columnas)
                    dic_dataframe = {col: [] for col in columnas_df}
                    for i in range(len(df_compensacion)):
                        valor = df_compensacion["NIU"][i]
                        if valor in dic_GRTT2:
                            lista_GRTT2 = dic_GRTT2[valor]
                            for j in range(1,len(lista_GRTT2)):
                                if columnas[j] == "Estrato":
                                    try:
                                        estrato_texto = tabla_3["datos"][str(lista_GRTT2[j])]
                                    except KeyError:
                                        estrato_texto = ""
                                    dic_dataframe[columnas[j]].append(estrato_texto)
                                else:
                                    dic_dataframe[columnas[j]].append(lista_GRTT2[j])
                            for col in columnas_compen:
                                dic_dataframe[col].append(df_compensacion[col][i])
                    df_compensacion_info = pd.DataFrame(dic_dataframe)
                    df_compensacion_info = df_compensacion_info.rename(columns={'Estrato': 'Sector_consumo'})
                    almacenar_df_csv_y_excel(df_compensacion_info, nombre.replace("_resumen","_reporte_compensacion"),thread=thread)
    return df1, nombre

def generar_reporte_compensacion_mensual(dic_archivos, seleccionar_reporte, informar=True, inventario=False, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df1,nombre = apoyo_generar_reporte_compensacion_mensual(lista_archivos_filial,informar,filial,inventario,thread=thread)
                if nombre:
                    lista_df_filiales.append(df1)
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
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
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_")
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            nuevo_nombre = nuevo_nombre.replace("_resumen","_compilado_compensacion")
            almacenar_df_csv_y_excel(df_total_compilado,nuevo_nombre, informar,thread=thread)

def apoyo_generar_reporte_desviaciones_mensual_DS56(lista_archivos,filial,fecha,filas_minimas,reporte,informar=True, thread=None):
    lista_reporte = []
    indicador_SUI_filial = indicador_SUI[filial]
    lista_fecha = fecha.split(" - ")
    v_fecha_anterior = fecha_anterior(lista_fecha[0], lista_fecha[1])
    mes = v_fecha_anterior[1]
    anio = v_fecha_anterior[0]
    ultimo_dia = calendar.monthrange(int(anio), lista_meses.index(mes)+1)[1]
    pos_mes = lista_meses.index(mes)+1
    if pos_mes < 10:
        pos_mes = "0" + str(pos_mes)
    else:
        pos_mes = str(pos_mes)
    for archivo in lista_archivos:
        if "HC" in archivo or "GC" in archivo:
            if "HC" in archivo:
                clasi = "(Hogar y Comercial)"
            elif "GC" in archivo:
                clasi = "(Grandes Clientes)"
            conteo_error = 0
            dic_error = {}
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                df = pd.concat(lista_df, ignore_index=True)
                columnas = list(df.columns)[:-2]
                df = df[columnas]
                mask = pd.Series([True] * len(df))
                for col in columnas:
                    if col == 'SERVICIO':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        mask &= df[col] == 5
                        lista = list(df[col].unique())
                        if len(lista) > 1:
                            conteo_error += 1
                            if 5 in lista:
                                lista.remove(5)
                            lista_df_error = []
                            for elemento in lista:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna debe ser {5} ({tabla_2_DS[str(5)]}) (Tabla_2_DS)"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna debe ser {5} ({tabla_2_DS[str(5)]}) (Tabla_2_DS)"
                            dic_error[col] = [texto, df_error]
                    elif col == 'ID_EMPRESA':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        mask &= (df[col] == int(indicador_SUI_filial))
                        lista = list(df[col].unique())
                        if len(lista) > 1:
                            conteo_error += 1
                            if int(indicador_SUI_filial) in lista:
                                lista.remove(int(indicador_SUI_filial))
                            lista_df_error = []
                            for elemento in lista:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna debe ser {indicador_SUI_filial} (Indicador SUI {filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna debe ser {indicador_SUI_filial} (Indicador SUI {filial})"
                            dic_error[col] = [texto, df_error]
                    elif col == 'NIU':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        lista_df_error = []
                        df[col] = df[col].astype(str)
                        for i in [""," ","0"]:
                            df_error = df[df[col]==i].reset_index(drop=True)
                            if len(df_error):
                                lista_df_error.append(df_error)
                        df_error = df[(df[col].str.len() < 8)|(df[col].str.len() > 8)].reset_index(drop=True)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna NO debe ser vacío o cero"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna NO debe ser vacío o cero"
                            dic_error[col] = [texto, df_error]
                        df[col] = df[col].astype(str)
                        mask &= (df[col] != "") & (df[col] != " ") & (df[col] != "0") & (df[col].str.len() == 8)
                    elif col == 'ID_MERCADO':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        dic_indicador_SUI_filial = mercado_relevante_id[str(indicador_SUI_filial)]
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in dic_indicador_SUI_filial:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Mercados relevantes que no existen en la filial {filial} ({indicador_SUI_filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Mercados relevantes que no existen en la filial {filial} ({indicador_SUI_filial})"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(dic_indicador_SUI_filial)
                    elif col == 'ESTRATO_SECTOR':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        if 11 in lista:
                            conteo_error += 1
                            df_error = df[df[col]==11].reset_index(drop=True)
                            if len(df_error):
                                filas_minimas_c = filas_minimas.copy()
                                filas_minimas_c.append(col)
                                df_error = df_error[filas_minimas_c]
                                if len(df_error) == 1:
                                    texto = f"1 error en la columna {col}. El valor de columna NO debe ser {11} ({tabla_3_DS[str(11)]}) (Tabla_3_DS)"
                                else:
                                    texto = f"{len(df_error)} errores en la columna {col}. El valor de columna NO debe ser {11} ({tabla_3_DS[str(11)]}) (Tabla_3_DS)"
                                dic_error[col+"_"+str(11)] = [texto, df_error]
                                lista.remove(11)
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_3_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_3_DS"
                            else:
                                texto = f"{(len(df_error))} errores en la columna {col}. Los valores no se encuentran en la Tabla_3_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_3_DS)
                    elif col == 'TIPO_TARIFA':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_4_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_4_DS"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_4_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_4_DS)
                    elif col == 'ID_FACTURA_INICIAL':
                        lista = list(df[col].unique())
                        lista_df_error = []
                        if "" in lista or " " in lista:
                            conteo_error += 1
                            for elemento in lista:
                                df_error = df[(df[col]=="") | (df[col]==" ")].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de la columna NO debe ser vacío"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de la columna NO debe ser vacío"
                            dic_error[col] = [texto, df_error]
                        mask &= (df[col].astype(str).str.len() > 0)
                    elif col == 'CODIGO_DANE_NIU':
                        df[col] = df[col].astype(str)
                        df[col] = df[col].apply(completar_codigo_DANE_000)
                        lista = list(df[col].unique())
                        dic_indicador_SUI_filial = mercado_relevante_DANE[str(indicador_SUI_filial)]
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in dic_indicador_SUI_filial:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Códigos DANE que no existen en la filial {filial} ({indicador_SUI_filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Códigos DANE que no existen en la filial {filial} ({indicador_SUI_filial})"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(dic_indicador_SUI_filial)
                    elif col == 'DETERMINADOR':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_5_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_5_DS"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_5_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_5_DS)
                nombre = archivo.replace("_HC","").replace("_GC","")
                df_filtrado = df[mask].copy()
                lista_reporte.append(df_filtrado)
                if conteo_error:
                    lista_archivo = archivo.split("\\")
                    lista_archivo[-1] = "log_errores_"+lista_archivo[-1]
                    nombre_error = lista_a_texto(lista_archivo, "\\").replace("_resumen","")
                    nombre_error_doc = nombre_error.replace(".csv",".docx")
                    nombre_error_pdf = nombre_error.replace(".csv",".pdf")
                    largo = 0
                    for valor in dic_error.values():
                        largo += len(valor[1])
                    op = mod_8.almacenar_errores(dic_error, filial, indicador_SUI[filial], mes, anio, nombre_error_doc, largo, reporte[2:], clasi, thread=thread)
                    if op:
                        informar_archivo_creado(nombre_error_pdf, True, thread=thread)
                    else:
                        if thread:
                            thread.message_sent.emit(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}", "red")
                        else:
                            print(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}")
    if len(lista_reporte):
        df_reporte = pd.concat(lista_reporte, ignore_index=True)
        ext = f"Desviaciones_{indicador_SUI_filial}_56_{pos_mes}{v_fecha_anterior[0]}.csv"
        lista_nombre = nombre.split("\\")
        carpeta = lista_nombre[-1]
        lista_nombre[-1] = ext
        nombre_1 = lista_a_texto(lista_nombre, "\\")
        almacenar_df_csv_y_excel(df_reporte, nombre_1, BOM=False, almacenar_excel=False, thread=thread)
        v_fun_tamanio_archivos = fun_tamanio_archivos(nombre_1)/(1024**2)
        if v_fun_tamanio_archivos >= 25:
            archivo_zip = os.path.join(carpeta, ext.replace(".csv", ".zip"))
            with zipfile.ZipFile(archivo_zip, 'w') as zipf:
                zipf.write(nombre_1, arcname=os.path.basename(nombre_1))
        return df_reporte, nombre
    else:
        return None, None

def completar_codigo_DANE_000(valor):
    valor = valor.zfill(8)
    valor = valor[:-3] + '000'
    return valor

def completar_codigo_DANE(valor):
    if len(valor):
        return valor.zfill(8)
    else:
        return ""

def apoyo_generar_reporte_desviaciones_mensual_DS57(lista_archivos,filial,fecha,filas_minimas,reporte,dic_reporte,dic_reporte_empresa,informar=True, thread=None):
    lista_reporte = []
    lista_fecha = fecha.split(" - ")
    v_fecha_anterior = fecha_anterior(lista_fecha[0], lista_fecha[1])
    mes = v_fecha_anterior[1]
    anio = v_fecha_anterior[0]
    ultimo_dia = calendar.monthrange(int(anio), lista_meses.index(mes)+1)[1]
    pos_mes = lista_meses.index(mes)+1
    if pos_mes < 10:
        pos_mes = "0" + str(pos_mes)
    else:
        pos_mes = str(pos_mes)
    inicio_mes = f"01-{pos_mes}-{anio}"
    fin_mes = f"{ultimo_dia}-{pos_mes}-{anio}"
    inicio_mes_dt = pd.to_datetime(inicio_mes, dayfirst=True)
    inicio_mes_str = inicio_mes_dt.strftime('%d-%m-%Y')
    fin_mes_dt = pd.to_datetime(fin_mes, dayfirst=True)
    fin_mes_str = fin_mes_dt.strftime('%d-%m-%Y')
    indicador_SUI_filial = indicador_SUI[filial]
    if str(indicador_SUI_filial) not in dic_reporte:
        dic_reporte[str(indicador_SUI_filial)] = 0
    if str(indicador_SUI_filial) not in dic_reporte_empresa:
        dic_reporte_empresa[str(indicador_SUI_filial)] = {}
    for archivo in lista_archivos:
        if "HC" in archivo or "GC" in archivo:
            if "HC" in archivo:
                clasi = "(Hogar y Comercial)"
            elif "GC" in archivo:
                clasi = "(Grandes Clientes)"
            conteo_error = 0
            dic_error = {}
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                df = pd.concat(lista_df, ignore_index=True)
                dic_reporte[indicador_SUI_filial] += len(df)
                columnas = list(df.columns)[:-2]
                df = df[columnas]
                df["FECHA_VISITA"] = df["FECHA_VISITA"].fillna(0).astype(int)
                df['FECHA_VISITA'] = df['FECHA_VISITA'].astype(str).replace('-', "").replace('/', '').replace('_', '')
                df['FECHA_VISITA'] = df['FECHA_VISITA'].apply(convertir_fecha)
                df['FECHA_VISITA'] = pd.to_datetime(df['FECHA_VISITA'], errors='coerce', dayfirst=True).dt.strftime('%d-%m-%Y').fillna('')
                mask = pd.Series([True] * len(df))
                for col in columnas:
                    if col == 'SERVICIO':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        mask &= df[col] == 5
                        lista = list(df[col].unique())
                        if len(lista) > 1:
                            conteo_error += 1
                            if 5 in lista:
                                lista.remove(5)
                            lista_df_error = []
                            for elemento in lista:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna debe ser {5} ({tabla_2_DS[str(5)]}) (Tabla_2_DS)"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna debe ser {5} ({tabla_2_DS[str(5)]}) (Tabla_2_DS)"
                            dic_error[col] = [texto, df_error]
                    elif col == 'ID_EMPRESA':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        mask &= (df[col] == int(indicador_SUI_filial))
                        lista = list(df[col].unique())
                        if len(lista) > 1:
                            conteo_error += 1
                            if int(indicador_SUI_filial) in lista:
                                lista.remove(int(indicador_SUI_filial))
                            lista_df_error = []
                            for elemento in lista:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna debe ser {indicador_SUI_filial} (Indicador SUI {filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna debe ser {indicador_SUI_filial} (Indicador SUI {filial})"
                            dic_error[col] = [texto, df_error]
                    elif col == 'NIU':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        lista_df_error = []
                        df[col] = df[col].astype(str)
                        for i in [""," ","0"]:
                            df_error = df[df[col]==i].reset_index(drop=True)
                            if len(df_error):
                                lista_df_error.append(df_error)
                        df_error = df[(df[col].str.len() < 8)|(df[col].str.len() > 8)].reset_index(drop=True)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna NO debe ser vacío o cero"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna NO debe ser vacío o cero"
                            dic_error[col] = [texto, df_error]
                        df[col] = df[col].astype(str)
                        mask &= (df[col] != "") & (df[col] != " ") & (df[col] != "0") & (df[col].str.len() == 8)
                    elif col == 'ID_MERCADO':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        dic_indicador_SUI_filial = mercado_relevante_id[str(indicador_SUI_filial)]
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in dic_indicador_SUI_filial:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            else:
                                if str(elemento) not in dic_reporte_empresa[str(indicador_SUI_filial)]:
                                    dic_reporte_empresa[str(indicador_SUI_filial)][str(elemento)] = 0
                                dic_reporte_empresa[str(indicador_SUI_filial)][str(elemento)] += len(df[df[col]==elemento])
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Mercados relevantes que no existen en la filial {filial} ({indicador_SUI_filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Mercados relevantes que no existen en la filial {filial} ({indicador_SUI_filial})"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(dic_indicador_SUI_filial)
                    elif col == 'CODIGO_DANE_NIU':
                        df[col] = df[col].astype(str)
                        df[col] = df[col].apply(completar_codigo_DANE_000)
                        lista = list(df[col].unique())
                        dic_indicador_SUI_filial = mercado_relevante_DANE[str(indicador_SUI_filial)]
                        lista_df_error = []
                        for elemento in lista:
                            if elemento not in dic_indicador_SUI_filial:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Códigos DANE que no existen en la filial {filial} ({indicador_SUI_filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Códigos DANE que no existen en la filial {filial} ({indicador_SUI_filial})"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(dic_indicador_SUI_filial)
                    elif col == 'ESTRATO_SECTOR':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        if 11 in lista:
                            conteo_error += 1
                            df_error = df[df[col]==11].reset_index(drop=True)
                            if len(df_error):
                                filas_minimas_c = filas_minimas.copy()
                                filas_minimas_c.append(col)
                                df_error = df_error[filas_minimas_c]
                                if len(df_error) == 1:
                                    texto = f"1 error en la columna {col}. El valor de columna NO debe ser {11} ({tabla_3_DS[str(11)]}) (Tabla_3_DS)"
                                else:
                                    texto = f"{len(df_error)} errores en la columna {col}. El valor de columna NO debe ser {11} ({tabla_3_DS[str(11)]}) (Tabla_3_DS)"
                                dic_error[col+"_"+str(11)] = [texto, df_error]
                                lista.remove(11)
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_3_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_3_DS"
                            else:
                                texto = f"{(len(df_error))} errores en la columna {col}. Los valores no se encuentran en la Tabla_3_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_3_DS)
                    elif col == 'TIPO_TARIFA':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_4_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_4_DS"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_4_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_4_DS)
                    elif col == 'PERIODO_FACTURACION':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_6_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_6_DS"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_6_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_6_DS)
                    elif col == 'ID_FACTURA_INICIAL':
                        lista = list(df[col].unique())
                        lista_df_error = []
                        if "" in lista or " " in lista:
                            conteo_error += 1
                            for elemento in lista:
                                df_error = df[(df[col]=="") | (df[col]==" ")].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de la columna NO debe ser vacío"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de la columna NO debe ser vacío"
                            dic_error[col] = [texto, df_error]
                        mask &= (df[col].astype(str).str.len() > 0)
                    elif col == "CONSUMO_USUARIO":
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista_df_error = []
                        df_filtro = df[df[col] < 0].reset_index(drop=True)
                        if len(df_filtro):
                            conteo_error += 1
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_filtro = df_filtro[filas_minimas_c]
                            if len(df_filtro) == 1:
                                texto = f"1 error en la columna {col}. Los valores de la columna deben ser positivos"
                            else:
                                texto = f"{len(df_filtro)} errores en la columna {col}. Los valores de la columna deben ser positivos"
                            dic_error[col] = [texto, df_filtro]
                        mask &= (df[col] >= 0)
                    elif col == "DIAS_FACTURADOS":
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        limite = 100
                        lista_df_error = []
                        df_filtro = df[(df[col] < 0)|((df[col] > limite))].reset_index(drop=True)
                        if len(df_filtro):
                            conteo_error += 1
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_filtro = df_filtro[filas_minimas_c]
                            if len(df_filtro) == 1:
                                texto = f"1 error en la columna {col}. Los valores de la columna deben ser positivos y menores a {limite}"
                            else:
                                texto = f"{len(df_filtro)} errores en la columna {col}. Los valores de la columna deben ser positivos y menores a {limite}"
                            dic_error[col] = [texto, df_filtro]
                        mask &= (df[col] >= 0) & (df[col] <= limite)
                    elif col in ["PROM_CONS_NORMALIZADO_12M","CONSUMO_NORMALIZADO","RAZON","DESVIACION_ESTANDAR","LIMITE_SUPERIOR","LIMITE_INFERIOR"]:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.00).round(2)
                        df_filtro = df[df[col] < 0].reset_index(drop=True)
                        lista_df_error = []
                        if len(df_filtro):
                            conteo_error += 1
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_filtro = df_filtro[filas_minimas_c]
                            if len(df_filtro) == 1:
                                texto = f"1 error en la columna {col}. Los valores de la columna deben ser positivos"
                            else:
                                texto = f"{len(df_filtro)} errores en la columna {col}. Los valores de la columna deben ser positivos"
                            dic_error[col] = [texto, df_filtro]
                        mask &= (df[col] >= 0)
                    elif col in ['REQUIERE_VISITA',"REALIZO_VISITA"]:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        if col == "REQUIERE_VISITA":
                            df.loc[df[col] == 2, 'REALIZO_VISITA'] = 2
                        df.loc[df[col] == 2, 'FECHA_VISITA'] = np.nan
                        df.loc[df[col] == 2, 'RESULTADO_FINAL_VISITA'] = 9
                        lista = list(df[col].unique())
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_30:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_30"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_30"
                            dic_error[col] = [texto, df_error]
                        if col == "REALIZO_VISITA":
                            df_error = df[(df["REQUIERE_VISITA"]==1)&(df["REALIZO_VISITA"]==1)&(df['FECHA_VISITA']==np.nan)].reset_index(drop=True)
                            if len(df_error):
                                conteo_error += 1
                                filas_minimas_c = filas_minimas.copy()
                                filas_minimas_c.append(col)
                                filas_minimas_c.append("FECHA_VISITA")
                                df_error = df_error[filas_minimas_c]
                                if len(df_error) == 1:
                                    texto = f"1 error en la columna {col}. Cuando el valor de REQUIERE_VISITA es 1 y {col} es 1, los valores de FECHA_VISITA no deben ser vacios"
                                else:
                                    texto = f"{(len(df_error))} errores en la columna {col}. Cuando el valor de REQUIERE_VISITA es 1 y {col} es 1, los valores de FECHA_VISITA no deben ser vacios"
                                dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_30)
                    elif col == "FECHA_VISITA":
                        df['FECHA_VISITA'] = pd.to_datetime(df['FECHA_VISITA'], errors='coerce', dayfirst=True)
                        df_filtro = df[(df['FECHA_VISITA']<inicio_mes_dt)|(df["FECHA_VISITA"]>fin_mes_dt)].reset_index(drop=True)
                        lista_df_error = []
                        if len(df_filtro):
                            conteo_error += 1
                            df_filtro["FECHA_VISITA"] = df_filtro["FECHA_VISITA"].fillna("").astype(str)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_filtro = df_filtro[filas_minimas_c]
                            if len(df_filtro) == 1:
                                texto = f"1 error en la columna {col}. Las fechas no se encuentran en el rango de fecha {inicio_mes_str} a {fin_mes_str}"
                            else:
                                texto = f"{len(df_filtro)} errores en la columna {col}. Las fechas no se encuentran en el rango de fecha {inicio_mes_str} a {fin_mes_str}"
                            dic_error[col] = [texto, df_filtro]
                        mask &= ((df['FECHA_VISITA'] > inicio_mes_dt) & (df["FECHA_VISITA"] < fin_mes_dt)) | (df['FECHA_VISITA'].isna())
                    elif col == "RESULTADO_FINAL_VISITA":
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", category=FutureWarning)
                            df.loc[df[col] == 9, 'OBSERVACION'] = "No realizo visita"
                        lista_df_error = []
                        lista = list(df[col].unique())
                        for elemento in lista:
                            if str(elemento) not in tabla_8_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_8_DS"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_8_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_8_DS)
                    elif col == "OBSERVACION":
                        df.loc[df[col] == "", 'OBSERVACION'] = "NA"
                        df.loc[df[col] == " ", 'OBSERVACION'] = "NA"
                        df[col] = df[col].fillna('NA')
                        mask &= (df[col].astype(str).str.len() > 0)
                nombre = archivo.replace("_HC","").replace("_GC","")
                df_filtrado = df[mask].copy()
                df_filtrado["FECHA_VISITA"] = df_filtrado["FECHA_VISITA"].dt.strftime('%d-%m-%Y')
                df_filtrado["FECHA_VISITA"] = df_filtrado["FECHA_VISITA"].fillna('')
                lista_reporte.append(df_filtrado)
                if conteo_error:
                    lista_archivo = archivo.split("\\")
                    lista_archivo[-1] = "log_errores_"+lista_archivo[-1]
                    nombre_error = lista_a_texto(lista_archivo, "\\").replace("_resumen","")
                    nombre_error_doc = nombre_error.replace(".csv",".docx")
                    nombre_error_pdf = nombre_error.replace(".csv",".pdf")
                    largo = 0
                    for valor in dic_error.values():
                        largo += len(valor[1])
                    op = mod_8.almacenar_errores(dic_error, filial, indicador_SUI[filial], mes, anio, nombre_error_doc, largo, reporte[2:], clasi, thread=thread)
                    if op:
                        informar_archivo_creado(nombre_error_pdf, True, thread=thread)
                    else:
                        if thread:
                            thread.message_sent.emit(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}", "red")
                        else:
                            print(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}")
    if len(lista_reporte):
        df_reporte = pd.concat(lista_reporte, ignore_index=True)
        ext = f"Desviaciones_{indicador_SUI_filial}_57_{pos_mes}{v_fecha_anterior[0]}.csv"
        lista_nombre = nombre.split("\\")
        carpeta = lista_nombre[-1]
        lista_nombre[-1] = ext
        nombre_1 = lista_a_texto(lista_nombre, "\\")
        almacenar_df_csv_y_excel(df_reporte, nombre_1, BOM=False, almacenar_excel=False, thread=thread)
        v_fun_tamanio_archivos = fun_tamanio_archivos(nombre_1)/(1024**2)
        if v_fun_tamanio_archivos >= 25:
            archivo_zip = os.path.join(carpeta, ext.replace(".csv", ".zip"))
            with zipfile.ZipFile(archivo_zip, 'w') as zipf:
                zipf.write(nombre_1, arcname=os.path.basename(nombre_1))
        return df_reporte, nombre, dic_reporte, dic_reporte_empresa
    else:
        return None, None, None, None

def apoyo_generar_reporte_desviaciones_mensual_DS58(lista_archivos,filial,fecha,filas_minimas,reporte,informar=True, thread=None):
    lista_reporte = []
    lista_fecha = fecha.split(" - ")
    v_fecha_reporte = fecha_anterior(lista_fecha[0], lista_fecha[1])
    v_fecha_reporte = fecha_anterior(v_fecha_reporte[0], v_fecha_reporte[1])
    mes_reporte = v_fecha_reporte[1]
    anio_reporte = v_fecha_reporte[0]

    v_fecha_anterior = fecha_anterior(anio_reporte, mes_reporte)
    mes_anterior = v_fecha_anterior[1]
    anio_anterior = v_fecha_anterior[0]
    ultimo_dia = calendar.monthrange(int(anio_reporte), lista_meses.index(mes_reporte)+1)[1]
    pos_mes = lista_meses.index(mes_anterior)+1
    if pos_mes < 10:
        pos_mes = "0" + str(pos_mes)
    else:
        pos_mes = str(pos_mes)
    pos_mes_1 = lista_meses.index(mes_reporte)+1
    if pos_mes_1 < 10:
        pos_mes_1 = "0" + str(pos_mes_1)
    else:
        pos_mes_1 = str(pos_mes_1)
    inicio_mes = f"01-{pos_mes}-{anio_anterior}"
    fin_mes = f"{ultimo_dia}-{pos_mes_1}-{anio_reporte}"
    inicio_mes_dt = pd.to_datetime(inicio_mes, dayfirst=True)
    inicio_mes_str = inicio_mes_dt.strftime('%d-%m-%Y')
    fin_mes_dt = pd.to_datetime(fin_mes, dayfirst=True)
    fin_mes_str = fin_mes_dt.strftime('%d-%m-%Y')
    indicador_SUI_filial = indicador_SUI[filial]
    for archivo in lista_archivos:
        if "HC" in archivo or "GC" in archivo:
            if "HC" in archivo:
                clasi = "(Hogar y Comercial)"
            elif "GC" in archivo:
                clasi = "(Grandes Clientes)"
            conteo_error = 0
            dic_error = {}
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                df = pd.concat(lista_df, ignore_index=True)
                columnas = list(df.columns)[:-2]
                df = df[columnas]
                df["FECHA_VISITA"] = df["FECHA_VISITA"].fillna(0).astype(int)
                df['FECHA_VISITA'] = df['FECHA_VISITA'].astype(str).replace('-', "").replace('/', '').replace('_', '')
                df['FECHA_VISITA'] = df['FECHA_VISITA'].apply(convertir_fecha)
                df['FECHA_VISITA'] = pd.to_datetime(df['FECHA_VISITA'], errors='coerce', dayfirst=True).dt.strftime('%d-%m-%Y').fillna('')
                mask = pd.Series([True] * len(df))
                for col in columnas:
                    if col == 'SERVICIO':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        mask &= df[col] == 5
                        lista = list(df[col].unique())
                        if len(lista) > 1:
                            conteo_error += 1
                            if 5 in lista:
                                lista.remove(5)
                            lista_df_error = []
                            for elemento in lista:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna debe ser {5} ({tabla_2_DS[str(5)]}) (Tabla_2_DS)"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna debe ser {5} ({tabla_2_DS[str(5)]}) (Tabla_2_DS)"
                            dic_error[col] = [texto, df_error]
                    elif col == 'ID_EMPRESA':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        mask &= (df[col] == int(indicador_SUI_filial))
                        lista = list(df[col].unique())
                        if len(lista) > 1:
                            conteo_error += 1
                            if int(indicador_SUI_filial) in lista:
                                lista.remove(int(indicador_SUI_filial))
                            lista_df_error = []
                            for elemento in lista:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna debe ser {indicador_SUI_filial} (Indicador SUI {filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna debe ser {indicador_SUI_filial} (Indicador SUI {filial})"
                            dic_error[col] = [texto, df_error]
                    elif col == 'NIU':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        lista_df_error = []
                        df[col] = df[col].astype(str)
                        for i in [""," ","0"]:
                            df_error = df[df[col]==i].reset_index(drop=True)
                            if len(df_error):
                                lista_df_error.append(df_error)
                        df_error = df[(df[col].str.len() < 8)|(df[col].str.len() > 8)].reset_index(drop=True)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de columna NO debe ser vacío o cero"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de columna NO debe ser vacío o cero"
                            dic_error[col] = [texto, df_error]
                        df[col] = df[col].astype(str)
                        mask &= (df[col] != "") & (df[col] != " ") & (df[col] != "0") & (df[col].str.len() == 8)
                    elif col == 'ID_MERCADO':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        dic_indicador_SUI_filial = mercado_relevante_id[str(indicador_SUI_filial)]
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in dic_indicador_SUI_filial:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Mercados relevantes que no existen en la filial {filial} ({indicador_SUI_filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Mercados relevantes que no existen en la filial {filial} ({indicador_SUI_filial})"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(dic_indicador_SUI_filial)
                    elif col == 'CODIGO_DANE_NIU':
                        df[col] = df[col].astype(str)
                        df[col] = df[col].apply(completar_codigo_DANE_000)
                        lista = list(df[col].unique())
                        dic_indicador_SUI_filial = mercado_relevante_DANE[str(indicador_SUI_filial)]
                        lista_df_error = []
                        for elemento in lista:
                            if elemento not in dic_indicador_SUI_filial:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Códigos DANE que no existen en la filial {filial} ({indicador_SUI_filial})"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Códigos DANE que no existen en la filial {filial} ({indicador_SUI_filial})"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(dic_indicador_SUI_filial)
                    elif col == 'ESTRATO_SECTOR':
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        lista = list(df[col].unique())
                        if 11 in lista:
                            conteo_error += 1
                            df_error = df[df[col]==11].reset_index(drop=True)
                            if len(df_error):
                                filas_minimas_c = filas_minimas.copy()
                                filas_minimas_c.append(col)
                                df_error = df_error[filas_minimas_c]
                                if len(df_error) == 1:
                                    texto = f"1 error en la columna {col}. El valor de columna NO debe ser {11} ({tabla_3_DS[str(11)]}) (Tabla_3_DS)"
                                else:
                                    texto = f"{len(df_error)} errores en la columna {col}. El valor de columna NO debe ser {11} ({tabla_3_DS[str(11)]}) (Tabla_3_DS)"
                                dic_error[col+"_"+str(11)] = [texto, df_error]
                                lista.remove(11)
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_3_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_3_DS"
                            else:
                                texto = f"{(len(df_error))} errores en la columna {col}. Los valores no se encuentran en la Tabla_3_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_3_DS)
                    elif col == 'ID_FACTURA_INICIAL':
                        lista = list(df[col].unique())
                        lista_df_error = []
                        if "" in lista or " " in lista:
                            conteo_error += 1
                            for elemento in lista:
                                df_error = df[(df[col]=="") | (df[col]==" ")].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. El valor de la columna NO debe ser vacío"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. El valor de la columna NO debe ser vacío"
                            dic_error[col] = [texto, df_error]
                        mask &= (df[col].astype(str).str.len() > 0)
                    elif col == "REALIZO_VISITA":
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        df.loc[df[col] == 2, 'FECHA_VISITA'] = np.nan
                        df.loc[df[col] == 2, 'RESULTADO_FINAL_VISITA'] = 9
                        lista = list(df[col].unique())
                        lista_df_error = []
                        for elemento in lista:
                            if str(elemento) not in tabla_30:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_30"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_30"
                            dic_error[col] = [texto, df_error]
                        df_error = df[(df[col]==1)&(df['FECHA_VISITA']==np.nan)].reset_index(drop=True)
                        if len(df_error):
                            conteo_error += 1
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            filas_minimas_c.append("FECHA_VISITA")
                            df_error = df_error[filas_minimas_c]
                            df_error["FECHA_VISITA"] = df_error["FECHA_VISITA"].fillna('')
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Cuando el valor de {col} es 1, los valores de FECHA_VISITA no deben ser vacios"
                            else:
                                texto = f"{(len(df_error))} errores en la columna {col}. Cuando el valor de {col} es 1, los valores de FECHA_VISITA no deben ser vacios"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_30)
                    elif col == "FECHA_VISITA":
                        df['FECHA_VISITA'] = pd.to_datetime(df['FECHA_VISITA'], errors='coerce', dayfirst=True)
                        df_filtro = df[(df['FECHA_VISITA']<inicio_mes_dt)|(df["FECHA_VISITA"]>fin_mes_dt)].reset_index(drop=True)
                        lista_df_error = []
                        if len(df_filtro):
                            conteo_error += 1
                            df_filtro["FECHA_VISITA"] = df_filtro["FECHA_VISITA"].fillna("").astype(str)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_filtro = df_filtro[filas_minimas_c]
                            if len(df_filtro) == 1:
                                texto = f"1 error en la columna {col}. Las fechas no se encuentran en el rango de fecha {inicio_mes_str} a {fin_mes_str}"
                            else:
                                texto = f"{len(df_filtro)} errores en la columna {col}. Las fechas no se encuentran en el rango de fecha {inicio_mes_str} a {fin_mes_str}"
                            dic_error[col] = [texto, df_filtro]
                        mask &= ((df['FECHA_VISITA'] > inicio_mes_dt) & (df["FECHA_VISITA"] < fin_mes_dt)) | (df['FECHA_VISITA'].isna())
                    elif col == "RESULTADO_FINAL_VISITA":
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", category=FutureWarning)
                            df.loc[df[col] == 9, 'OBSERVACION'] = "No realizo visita"
                        lista_df_error = []
                        lista = list(df[col].unique())
                        for elemento in lista:
                            if str(elemento) not in tabla_8_DS:
                                df_error = df[df[col]==elemento].reset_index(drop=True)
                                if len(df_error):
                                    lista_df_error.append(df_error)
                        if len(lista_df_error):
                            conteo_error += 1
                            df_error = pd.concat(lista_df_error, ignore_index=True)
                            filas_minimas_c = filas_minimas.copy()
                            filas_minimas_c.append(col)
                            df_error = df_error[filas_minimas_c]
                            if len(df_error) == 1:
                                texto = f"1 error en la columna {col}. Los valores no se encuentran en la Tabla_8_DS"
                            else:
                                texto = f"{len(df_error)} errores en la columna {col}. Los valores no se encuentran en la Tabla_8_DS"
                            dic_error[col] = [texto, df_error]
                        mask &= df[col].astype(str).isin(tabla_8_DS)
                    elif col == "OBSERVACION":
                        df.loc[df[col] == "", 'OBSERVACION'] = "NA"
                        df.loc[df[col] == " ", 'OBSERVACION'] = "NA"
                        df[col] = df[col].fillna('NA')
                        mask &= (df[col].astype(str).str.len() > 0)
                nombre = archivo.replace("_HC","").replace("_GC","")
                df_filtrado = df[mask].copy()
                df_filtrado["FECHA_VISITA"] = df_filtrado["FECHA_VISITA"].dt.strftime('%d-%m-%Y')
                df_filtrado["FECHA_VISITA"] = df_filtrado["FECHA_VISITA"].fillna('')
                lista_reporte.append(df_filtrado)
                if conteo_error:
                    lista_archivo = archivo.split("\\")
                    lista_archivo[-1] = "log_errores_"+lista_archivo[-1]
                    nombre_error = lista_a_texto(lista_archivo, "\\").replace("_resumen","")
                    nombre_error_doc = nombre_error.replace(".csv",".docx")
                    nombre_error_pdf = nombre_error.replace(".csv",".pdf")
                    largo = 0
                    for valor in dic_error.values():
                        largo += len(valor[1])
                    op = mod_8.almacenar_errores(dic_error, filial, indicador_SUI[filial], mes_reporte, anio_reporte, nombre_error_doc, largo, reporte[2:], clasi, thread=thread)
                    if op:
                        informar_archivo_creado(nombre_error_pdf, True, thread=thread)
                    else:
                        if thread:
                            thread.message_sent.emit(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}", "red")
                        else:
                            print(f"No es posible acceder al archivo {acortar_nombre(nombre_error_pdf)}")
    if len(lista_reporte):
        df_reporte = pd.concat(lista_reporte, ignore_index=True)
        ext = f"Desviaciones_{indicador_SUI_filial}_58_{pos_mes_1}{v_fecha_reporte[0]}.csv"
        lista_nombre = nombre.split("\\")
        carpeta = lista_nombre[-1]
        lista_nombre[-1] = ext
        nombre_1 = lista_a_texto(lista_nombre, "\\")
        almacenar_df_csv_y_excel(df_reporte, nombre_1, BOM=False, almacenar_excel=False, thread=thread)
        v_fun_tamanio_archivos = fun_tamanio_archivos(nombre_1)/(1024**2)
        if v_fun_tamanio_archivos >= 25:
            archivo_zip = os.path.join(carpeta, ext.replace(".csv", ".zip"))
            with zipfile.ZipFile(archivo_zip, 'w') as zipf:
                zipf.write(nombre_1, arcname=os.path.basename(nombre_1))
        return df_reporte, nombre
    else:
        return None, None

def generar_reporte_desviaciones_mensual(dic_archivos, seleccionar_reporte, informar=True, thread=None):
    filas_minimas = ["ID_EMPRESA","NIU","ID_MERCADO"]
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        dic_reporte = {}
        dic_reporte_empresa = {}
        for reporte in lista_archivo_desviaciones:
            lista_df_filiales = []
            for filial in lista_filiales_archivo:
                lista_archivos_filial = []
                for archivo in lista_archivos:
                    if filial in archivo and reporte in archivo:
                        lista_archivos_filial.append(archivo)
                if len(lista_archivos_filial):
                    if reporte == "DS56":
                        df1,nombre = apoyo_generar_reporte_desviaciones_mensual_DS56(lista_archivos_filial,filial,fecha, filas_minimas, reporte, thread=thread)
                        if nombre:
                            lista_df_filiales.append(df1)
                    elif reporte == "DS57":
                        df1,nombre,dic_reporte,dic_reporte_empresa = apoyo_generar_reporte_desviaciones_mensual_DS57(lista_archivos_filial,filial,fecha, filas_minimas, reporte, dic_reporte,dic_reporte_empresa, thread=thread)
                        if nombre:
                            lista_df_filiales.append(df1)
                    elif reporte == "DS58":
                        df1,nombre = apoyo_generar_reporte_desviaciones_mensual_DS58(lista_archivos_filial,filial,fecha, filas_minimas, reporte, thread=thread)
                        if nombre:
                            lista_df_filiales.append(df1)
            if len(lista_df_filiales) and len(lista_filiales_archivo) == 4 and reporte == "DS57":
                df_total_compilado = pd.concat(lista_df_filiales, ignore_index=True)
                lista_nombre = nombre.split("\\")
                valor = lista_nombre[-1].split("_")
                valor.pop(1)
                lista_nombre[-1] = lista_a_texto(valor,"_")
                lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
                lista_nombre.pop(-2)
                nuevo_nombre = lista_a_texto(lista_nombre,"\\")
                nuevo_nombre = nuevo_nombre.replace("_resumen","_compilado_DS")
                almacenar_df_csv_y_excel(df_total_compilado,nuevo_nombre, informar, almacenar_excel=False, thread=thread)
                lista_id_empresa = list(df_total_compilado["ID_EMPRESA"].unique())
                dic_reporte_atendidos = {}
                dic_df = {"Filial":[],
                        "Indicador_SUI":[],
                        "Mercado_relevante":[],
                        "Desviaciones_totales":[],
                        "Visitas_realizadas":[],
                        "No_realizo_viista":[],
                        "Porcentaje_atendidos":[]}
                dic_df_1 = {"Filial":[],
                        "Indicador_SUI":[],
                        "Mercado_relevante":[],
                        "Desviaciones_totales":[],
                        "Categoria":[],
                        "Total_categoria":[]}
                dic_reporte_categoria = {}
                for id_empresa in lista_id_empresa:
                    if str(id_empresa) not in dic_reporte_atendidos:
                        dic_reporte_atendidos[str(id_empresa)] = {}
                    if str(id_empresa) not in dic_reporte_categoria:
                        dic_reporte_categoria[str(id_empresa)] = {}
                    df_empresa = df_total_compilado[df_total_compilado["ID_EMPRESA"]==id_empresa].reset_index(drop=True)
                    id_mercado = list(df_empresa["ID_MERCADO"].unique())
                    for id_mercado in id_mercado:
                        if str(id_mercado) not in dic_reporte_atendidos[str(id_empresa)]:
                            dic_reporte_atendidos[str(id_empresa)][str(id_mercado)] = None
                        if str(id_mercado) not in dic_reporte_categoria[str(id_empresa)]:
                            dic_reporte_categoria[str(id_empresa)][str(id_mercado)] = {}
                        df_mercado = df_empresa[df_empresa["ID_MERCADO"]==id_mercado].reset_index(drop=True)
                        df_mercado_1 = df_mercado.copy()
                        c_nan = df_mercado['FECHA_VISITA'].isna().sum()
                        df_mercado = df_mercado.dropna(subset=['FECHA_VISITA'])
                        largo = len(df_mercado)
                        valor = dic_reporte_empresa[str(id_empresa)][str(id_mercado)]
                        dic_reporte_categoria[str(id_empresa)][str(id_mercado)]["Total"] = valor
                        porcentaje = f"{round((largo/valor)*100,2)} %"
                        dic_reporte_atendidos[str(id_empresa)][str(id_mercado)] = porcentaje
                        dic_df["Filial"].append(dic_filiales[empresa_indicador_SUI[str(id_empresa)]])
                        dic_df["Indicador_SUI"].append(id_empresa)
                        dic_df["Mercado_relevante"].append(id_mercado)
                        dic_df["Desviaciones_totales"].append(valor)
                        dic_df["Visitas_realizadas"].append(largo)
                        dic_df["No_realizo_viista"].append(c_nan)
                        dic_df["Porcentaje_atendidos"].append(porcentaje)
                        lista_resultados = list(df_mercado_1["RESULTADO_FINAL_VISITA"].unique())
                        for resultado in lista_resultados:
                            llave = tabla_8_DS_categoria[str(resultado)]
                            cantidad = len(df_mercado_1[df_mercado_1["RESULTADO_FINAL_VISITA"]==resultado])
                            if llave not in dic_reporte_categoria[str(id_empresa)][str(id_mercado)]:
                                dic_reporte_categoria[str(id_empresa)][str(id_mercado)][llave] = 0
                            dic_reporte_categoria[str(id_empresa)][str(id_mercado)][llave] += cantidad
                for id_empresa, dic_empresa in dic_reporte_categoria.items():
                    for id_mercado, dic_mercado in dic_empresa.items():
                        for categoria, valor in dic_mercado.items():
                            if categoria != "Total":
                                dic_df_1["Filial"].append(dic_filiales[empresa_indicador_SUI[str(id_empresa)]])
                                dic_df_1["Indicador_SUI"].append(id_empresa)
                                dic_df_1["Mercado_relevante"].append(id_mercado)
                                dic_df_1["Desviaciones_totales"].append(dic_mercado["Total"])
                                dic_df_1["Categoria"].append(categoria)
                                dic_df_1["Total_categoria"].append(valor)
                df_metricas = pd.DataFrame(dic_df)
                lista_fecha = fecha.split(" - ")
                lista_fecha = fecha_anterior(lista_fecha[0], lista_fecha[1])
                df_metricas["Anio_reportado"] = lista_fecha[0]
                df_metricas["Mes_reportado"] = lista_fecha[1]
                df_metricas_categoria = pd.DataFrame(dic_df_1)
                ultima_fila = [grupo_vanti, grupo_vanti, grupo_vanti, df_metricas_categoria["Total_categoria"].sum(), "Total", df_metricas_categoria["Total_categoria"].sum()]
                lista_categoria = list(df_metricas_categoria["Categoria"].unique())
                matriz_fila = []
                for categoria in lista_categoria:
                    df_categoria = df_metricas_categoria[df_metricas_categoria["Categoria"]==categoria].reset_index(drop=True)
                    nueva_fila = [grupo_vanti, grupo_vanti, grupo_vanti, df_metricas_categoria["Total_categoria"].sum(), categoria, df_categoria["Total_categoria"].sum()]
                    matriz_fila.append(nueva_fila)
                for fila in matriz_fila:
                    df_metricas_categoria.loc[len(df_metricas_categoria)] = fila
                df_metricas_categoria.loc[len(df_metricas_categoria)] = ultima_fila
                df_metricas_categoria["Anio_reportado"] = lista_fecha[0]
                df_metricas_categoria["Mes_reportado"] = lista_fecha[1]
                nombre = nuevo_nombre.replace(".csv", "_metricas.csv")
                almacenar_df_csv_y_excel(df_metricas, nombre, thread=thread)
                nombre = nuevo_nombre.replace(".csv", "_metricas_categorias.csv")
                almacenar_df_csv_y_excel(df_metricas_categoria, nombre, thread=thread)

def apoyo_reporte_usuarios_unicos_mensual(lista_archivos, informar, filial, almacenar_excel=True, thread=None):
    proceso_GRC1 = False
    proceso_GRC2 = False
    proceso_GRTT2 = False
    nombre_1 = None
    nombre_2 = None
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    for archivo in lista_archivos:
        if "GRC1" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                proceso_GRC1 = True
                nombre_GRC1 = archivo
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                dic_reg = {}
                lista_reg = [0,0,0] #m3, Valor_total_facturado, Valor_consumo_facturado
                dic_reg_factura = {}
                for df in lista_df:
                    df["ID_factura"] = df["ID_factura"].astype(str)
                    df["NIU"] = df["NIU"].fillna(0).astype(int)
                    df["Consumo"] = df["Consumo"].fillna(0).astype(int)
                    df["Valor_total_facturado"] = df["Valor_total_facturado"].fillna(0).astype(float)
                    df["Facturacion_consumo"] = df["Facturacion_consumo"].fillna(0).astype(float)
                    for i in range(len(df)):
                        try:
                            valor = int(df["NIU"][i])
                            if valor not in dic_reg and valor > 0:
                                dic_reg[valor] = [valor,0,0,0,0,None,None] #NIU,Cantidad_facturas,Consumo,Valor_consumo_facturado,Valor_total_facturado,Codigo_DANE,Sector_consumo
                            factura = str(df["ID_factura"][i]).upper().strip()
                            if factura[0] == "F":
                                dic_reg[valor][1] += 1
                                if factura not in dic_reg_factura:
                                    dic_reg_factura[factura] = True
                            valor_1 = int(df["Consumo"][i])
                            if valor_1 > 0:
                                lista_reg[0] += valor_1
                                dic_reg[valor][2] += valor_1
                            valor_2 = float(df["Valor_total_facturado"][i])
                            if valor_2 > 0:
                                lista_reg[1] += valor_2
                                dic_reg[valor][4] += valor_2
                            valor_3 = float(df["Facturacion_consumo"][i])
                            if valor_3 > 0:
                                lista_reg[2] += valor_3
                                dic_reg[valor][3] += valor_3
                        except BaseException:
                            pass
        elif "GRC2" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                proceso_GRC2 = True
                nombre_GRC2 = archivo
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                dic_no_reg = {}
                lista_no_reg = [0,0,0] #m3, Valor_total_facturado, Valor_consumo_facturado
                dic_no_reg_factura = {}
                for df in lista_df:
                    df["Codigo_DANE"] = df["Codigo_DANE"].fillna(0).astype(int)
                    df["Codigo_DANE"] = df["Codigo_DANE"].astype(str).replace("0", "").replace("nan", "")
                    df["Codigo_DANE"] = df["Codigo_DANE"].apply(completar_codigo_DANE)
                    df["NIU"] = df["NIU"].fillna(0).astype(int)
                    df["Sector_consumo"] = df["Sector_consumo"].fillna(0).astype(int)
                    df["ID_Factura"] = df["ID_Factura"].astype(str)
                    df["Volumen"] = df["Volumen"].fillna(0).astype(int)
                    df["Valor_total_facturado"] = df["Valor_total_facturado"].fillna(0).astype(float)
                    df["Facturacion_por_demanda_volumen"] = df["Facturacion_por_demanda_volumen"].fillna(0).astype(float)
                    for i in range(len(df)):
                        try:
                            valor = int(df["NIU"][i])
                            if valor not in dic_no_reg:
                                dic_no_reg[valor] = [valor,0,0,0,0,None,None] #NIU,Cantidad_facturas,Consumo,Valor_consumo_facturado,Valor_total_facturado,Codigo_DANE,Sector_consumo
                            dic_no_reg[valor][5] = df["Codigo_DANE"][i]
                            factura = str(df["ID_Factura"][i]).upper().strip()
                            if factura[0] == "F":
                                dic_no_reg[valor][1] += 1
                                if factura not in dic_no_reg_factura:
                                    dic_no_reg_factura[factura] = True
                            valor_1 = int(df["Sector_consumo"][i])
                            try:
                                valor_1 = tabla_11["datos"][str(valor_1)]
                                dic_no_reg[valor][6] = valor_1
                            except KeyError:
                                dic_no_reg[valor][6] = ""
                            valor_2 = int(df["Volumen"][i])
                            if valor_2 > 0:
                                lista_no_reg[0] += valor_2
                                dic_no_reg[valor][2] += valor_2
                            valor_3 = float(df["Valor_total_facturado"][i])
                            if valor_3 > 0:
                                lista_no_reg[1] += valor_3
                                dic_no_reg[valor][4] += valor_3
                            valor_4 = float(df["Facturacion_por_demanda_volumen"][i])
                            if valor_4 > 0:
                                lista_no_reg[2] += valor_4
                                dic_no_reg[valor][3] += valor_4
                        except BaseException:
                            pass
        elif "GRTT2" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                proceso_GRTT2 = True
                dic_GRTT2 = {}
                for df in lista_df:
                    df["Estrato"] = df["Estrato"].fillna(0).astype(int)
                    df["Codigo_DANE"] = df["Codigo_DANE"].fillna(0).astype(int)
                    df["Codigo_DANE"] = df["Codigo_DANE"].astype(str).replace("0", "").replace("nan", "")
                    df["Codigo_DANE"] = df["Codigo_DANE"].apply(completar_codigo_DANE)
                    df["NIU"] = df["NIU"].fillna(0).astype(int)
                    for i in range(len(df)):
                        valor = int(df["NIU"][i])
                        if valor not in dic_GRTT2:
                            dic_GRTT2[valor] = [df["Codigo_DANE"][i], df["Estrato"][i]] #Código DANE, Sector de consumo
    dic_NIU_factura = {"Clasificacion_usuario":[],
                    "NIU":[],
                    "Consumo_m3":[],
                    "Cantidad_facturas_emitidas":[],
                    "Valor_consumo_facturado":[],
                    "Valor_total_facturado":[],
                    "Codigo_DANE":[],
                    "Sector_consumo":[]}
    if proceso_GRTT2 and proceso_GRC1:
        for v_NIU in dic_reg:
            if v_NIU in dic_GRTT2:
                dic_reg[v_NIU][5] = dic_GRTT2[v_NIU][0]
                try:
                    valor_1 = int(dic_GRTT2[v_NIU][1])
                    try:
                        valor_1 = tabla_3["datos"][str(valor_1)]
                        dic_reg[v_NIU][6] = valor_1
                    except BaseException:
                        dic_reg[v_NIU][6] = ""
                except BaseException:
                    dic_reg[v_NIU][6] = ""
            else:
                dic_reg[v_NIU][5] = ""
                dic_reg[v_NIU][6] = ""
        for lista_NIU in dic_reg.values():
            dic_NIU_factura["Clasificacion_usuario"].append("Regulado")
            dic_NIU_factura["NIU"].append(lista_NIU[0])
            dic_NIU_factura["Consumo_m3"].append(lista_NIU[2])
            dic_NIU_factura["Cantidad_facturas_emitidas"].append(lista_NIU[1])
            dic_NIU_factura["Valor_consumo_facturado"].append(lista_NIU[3])
            dic_NIU_factura["Valor_total_facturado"].append(lista_NIU[4])
            dic_NIU_factura["Codigo_DANE"].append(lista_NIU[5])
            dic_NIU_factura["Sector_consumo"].append(lista_NIU[6])
    if proceso_GRC2:
        for lista_NIU in dic_no_reg.values():
            dic_NIU_factura["Clasificacion_usuario"].append("No Regulado")
            dic_NIU_factura["NIU"].append(lista_NIU[0])
            dic_NIU_factura["Consumo_m3"].append(lista_NIU[2])
            dic_NIU_factura["Cantidad_facturas_emitidas"].append(lista_NIU[1])
            dic_NIU_factura["Valor_consumo_facturado"].append(lista_NIU[3])
            dic_NIU_factura["Valor_total_facturado"].append(lista_NIU[4])
            dic_NIU_factura["Codigo_DANE"].append(lista_NIU[5])
            dic_NIU_factura["Sector_consumo"].append(lista_NIU[6])
    df1 = pd.DataFrame(dic_NIU_factura)
    if proceso_GRC1:
        nombre_arc = nombre_GRC1
    else:
        nombre_arc = nombre_GRC2
    if len(df1):
        lista_nombre = nombre_arc.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        nombre = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_usuarios_unicos_facturacion")
        almacenar_df_csv_y_excel(df1, nombre, almacenar_excel=False, thread=thread)
        dic_reporte_facturacion = {"Clasificacion_usuarios":[],
                                    "Sector_consumo":[],
                                    "Cantidad_NIU_Unicos":[],
                                    "Cantidad_facturas_emitidas":[],
                                    "Consumo_m3":[],
                                    "Valor_consumo_facturado":[],
                                    "Valor_total_facturado":[]}
        lista_tipo_usuario = list(df1["Clasificacion_usuario"].unique())
        for tipo_usuario in lista_tipo_usuario:
            df_temp_1 = df1[df1["Clasificacion_usuario"] == tipo_usuario]
            lista_sector_consumo = list(df_temp_1["Sector_consumo"].unique())
            for sector in lista_sector_consumo:
                df_temp = df_temp_1[df_temp_1["Sector_consumo"] == sector]
                dic_reporte_facturacion["Clasificacion_usuarios"].append(tipo_usuario)
                dic_reporte_facturacion["Sector_consumo"].append(sector)
                dic_reporte_facturacion["Cantidad_NIU_Unicos"].append(len(df_temp))
                dic_reporte_facturacion["Consumo_m3"].append(df_temp["Consumo_m3"].sum())
                dic_reporte_facturacion["Cantidad_facturas_emitidas"].append(df_temp["Cantidad_facturas_emitidas"].sum())
                dic_reporte_facturacion["Valor_consumo_facturado"].append(df_temp["Valor_consumo_facturado"].sum())
                dic_reporte_facturacion["Valor_total_facturado"].append(df_temp["Valor_total_facturado"].sum())
        df2 = pd.DataFrame(dic_reporte_facturacion)
        df2["Filial"] = dic_filiales[filial]
        df2["NIT"] = dic_nit[dic_filiales[filial]]
        df2["Mes_reportado"] = mes_reportado
        df2["Anio_reportado"] = anio_reportado
        df2 = df2[["Filial","NIT","Anio_reportado","Mes_reportado","Clasificacion_usuarios","Sector_consumo",
                "Cantidad_facturas_emitidas","Consumo_m3","Valor_consumo_facturado","Valor_total_facturado"]]
        lista_nombre = nombre_arc.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        nombre_1 = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_reporte_facturacion")
        almacenar_df_csv_y_excel(df2, nombre_1, thread=thread)
    dic_df = {"Clasificacion_usuarios":[],
                "Cantidad_usuarios_unicos":[],
                "Consumo_m3":[],
                "Cantidad_facturas_emitidas":[],
                "Valor_consumo_facturado":[],
                "Valor_total_facturado":[]}
    if proceso_GRC1:
        dic_df["Clasificacion_usuarios"].append("Regulados")
        dic_df["Cantidad_usuarios_unicos"].append(len(dic_reg))
        dic_df["Cantidad_facturas_emitidas"].append(len(dic_reg_factura))
        dic_df["Consumo_m3"].append(lista_reg[0])
        dic_df["Valor_consumo_facturado"].append(lista_reg[2])
        dic_df["Valor_total_facturado"].append(lista_reg[1])
    if proceso_GRC2:
        dic_df["Clasificacion_usuarios"].append("No Regulados")
        dic_df["Cantidad_usuarios_unicos"].append(len(dic_no_reg))
        dic_df["Cantidad_facturas_emitidas"].append(len(dic_no_reg_factura))
        dic_df["Consumo_m3"].append(lista_no_reg[0])
        dic_df["Valor_consumo_facturado"].append(lista_no_reg[2])
        dic_df["Valor_total_facturado"].append(lista_no_reg[1])
    df = pd.DataFrame(dic_df)
    if len(df):
        df["Filial"] = dic_filiales[filial]
        df["NIT"] = dic_nit[dic_filiales[filial]]
        df["Mes_reportado"] = mes_reportado
        df["Anio_reportado"] = anio_reportado
        df = df[["Filial","NIT","Anio_reportado","Mes_reportado","Clasificacion_usuarios","Cantidad_usuarios_unicos",
                "Cantidad_facturas_emitidas","Consumo_m3","Valor_consumo_facturado","Valor_total_facturado"]]
        lista_nombre = nombre_arc.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        nombre_2 = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_usuarios_unicos")
        almacenar_df_csv_y_excel(df, nombre_2, thread=thread)
    return df, nombre_2, df2, nombre_1

def reporte_usuarios_unicos_mensual(dic_archivos, seleccionar_reporte, informar, almacenar_excel=True, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales_1 = []
        lista_df_filiales_2 = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df1,nombre_1,df2,nombre_2 = apoyo_reporte_usuarios_unicos_mensual(lista_archivos_filial,informar,filial, almacenar_excel, thread=thread)
                if nombre_1:
                    lista_df_filiales_1.append(df1)
                if nombre_2:
                    lista_df_filiales_2.append(df2)
        if len(lista_filiales_archivo) == 4:
            if len(lista_df_filiales_2):
                df_total = pd.concat(lista_df_filiales_2, ignore_index=True)
                df_total = generar_suma_df_filiales(df_total, ["Clasificacion_usuarios","Sector_consumo"],["Cantidad_facturas_emitidas","Consumo_m3",
                                                                "Valor_consumo_facturado","Valor_total_facturado"])
                lista_nombre = nombre_2.split("\\")
                lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
                lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
                lista_nombre.pop(-2)
                nuevo_nombre = lista_a_texto(lista_nombre,"\\")
                almacenar_df_csv_y_excel(df_total, nuevo_nombre, thread=thread)
            if len(lista_df_filiales_1):
                df_total = pd.concat(lista_df_filiales_1, ignore_index=True)
                df_total = generar_suma_df_filiales(df_total,["Clasificacion_usuarios"],["Cantidad_facturas_emitidas",
                                                                "Consumo_m3","Valor_consumo_facturado","Valor_total_facturado", "Cantidad_usuarios_unicos"])
                lista_nombre = nombre_1.split("\\")
                lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
                lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
                lista_nombre.pop(-2)
                nuevo_nombre = lista_a_texto(lista_nombre,"\\")
                almacenar_df_csv_y_excel(df_total, nuevo_nombre, thread=thread)

def reporte_comportamiento_patrimonial(fi,ff,listas_unidas):
    nombre = "info_trimestral"
    hoja = "comportamiento_patrimonial"
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsx"
    if os.path.exists(archivo):
        df, proceso = mod_5.lectura_hoja_xlsx(archivo, hoja)
        if proceso:
            lista_df = []
            try:
                ubi_1 = listas_unidas.index(f"{fi[0]} - {fi[1]}")
            except ValueError:
                ubi_1 = 0
            try:
                ubi_2 = listas_unidas.index(f"{ff[0]} - {ff[1]}")
            except ValueError:
                ubi_2 = len(listas_unidas)
            f_inicial = listas_unidas[ubi_1].split(" - ")
            f_final = listas_unidas[ubi_2].split(" - ")
            for i in listas_unidas[ubi_1:ubi_2]:
                fecha = i.split(" - ")
                df_filtro = df[(df['Anio_reportado'] == int(fecha[0])) & (df['Periodo_reportado'] == fecha[1])].copy()
                lista_fila = [grupo_vanti, fecha[1], int(fecha[0]), df_filtro['Saldo_patrimonio_neto'].sum(), df_filtro['Saldo_capital_emitido'].sum()]
                df_filtro.loc[len(df_filtro)] = lista_fila
                df_filtro = df_filtro.reset_index(drop=True)
                lista_porcentaje = []
                for j in range(len(df_filtro)):
                    lista_porcentaje.append(str(round((df_filtro['Saldo_capital_emitido'][j]/df_filtro['Saldo_patrimonio_neto'][j])*100,2))+" %")
                df_filtro["Porcentaje_patrimonial"] = lista_porcentaje
                lista_df.append(df_filtro)
            df_total = pd.concat(lista_df, ignore_index=True)
            lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
            nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_patrimonial_{f_inicial[0]}_{f_inicial[1]}_{f_final[0]}_{f_final[1]}")
            lista_nombre = nuevo_nombre.split("\\")
            ext = lista_nombre[-1]
            lista_nombre[-1] = "KPIs"
            nombre_carpeta = lista_a_texto(lista_nombre, "\\")
            crear_carpeta(nombre_carpeta)
            lista_nombre.append(ext)
            nuevo_nombre = lista_a_texto(lista_nombre, "\\")
            almacenar_df_csv_y_excel(df_total,nuevo_nombre)
            return nuevo_nombre
        else:
            print(f"No es posible acceder al archivo {archivo}.")
            return None
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

def reporte_info_reclamos(fi,ff,listas_unidas, dashboard=False, texto_fecha=None, thread=None):
    nombre = "info_trimestral"
    hoja = "relacion_reclamos_facturacion"
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsx"
    if os.path.exists(archivo):
        df, proceso = mod_5.lectura_hoja_xlsx(archivo, hoja)
        if proceso:
            lista_df = []
            try:
                ubi_1 = listas_unidas.index(f"{fi[0]} - {fi[1]}")
            except ValueError:
                ubi_1 = 0
            try:
                ubi_2 = listas_unidas.index(f"{ff[0]} - {ff[1]}")
            except ValueError:
                ubi_2 = len(listas_unidas)-1
            f_inicial = listas_unidas[ubi_1].split(" - ")
            f_final = listas_unidas[ubi_2].split(" - ")
            for i in listas_unidas[ubi_1:ubi_2+1]:
                fecha = i.split(" - ")
                df_filtro = df[(df['Anio_reportado'] == int(fecha[0])) & (df['Periodo_reportado'] == fecha[1])].copy()
                lista_fila = [grupo_vanti, fecha[1], int(fecha[0]), df_filtro['Numero_Facturas_Expedidas'].sum(), df_filtro['Numero_Reclamos_Facturacion'].sum()]
                df_filtro.loc[len(df_filtro)] = lista_fila
                df_filtro = df_filtro.reset_index(drop=True)
                lista_porcentaje = []
                for j in range(len(df_filtro)):
                    valor_f_1 = df_filtro['Numero_Facturas_Expedidas'][j]
                    valor_f_2 = df_filtro['Numero_Reclamos_Facturacion'][j]
                    if valor_f_2 and valor_f_1:
                        lista_porcentaje.append(str(round((valor_f_1/valor_f_2)*10000,2))+" %")
                    else:
                        lista_porcentaje.append("0.00 %")
                df_filtro["Porcentaje_reclamos_fact_10000"] = lista_porcentaje
                lista_df.append(df_filtro)
            df_total = pd.concat(lista_df, ignore_index=True)
            if not dashboard:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_reclamos_facturacion_10000_{f_inicial[0]}_{f_inicial[1]}_{f_final[0]}_{f_final[1]}")
                lista_nombre = nuevo_nombre.split("\\")
                ext = lista_nombre[-1]
                lista_nombre[-1] = "KPIs"
                nombre_carpeta = lista_a_texto(lista_nombre, "\\")
                crear_carpeta(nombre_carpeta)
                lista_nombre.append(ext)
                nuevo_nombre = lista_a_texto(lista_nombre, "\\")
                almacenar_df_csv_y_excel(df_total,nuevo_nombre,thread=thread)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_reclamos_facturacion_10000")
                almacenar_df_csv_y_excel(df_total,nuevo_nombre,thread=thread)
                return nuevo_nombre
        else:
            if thread:
                thread.message_sent.emit(f"No es posible acceder al archivo {archivo}.", "red")
            else:
                print(f"No es posible acceder al archivo {archivo}.")
            return None,None
    else:
        if thread:
            thread.message_sent.emit(f"No existe el archivo {archivo}. No es posible generar el reporte.", "red")
        else:
            print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None,None

def convertir_fecha_2(fecha):
    try:
        #return pd.to_datetime(fecha, errors='coerce', dayfirst=True)
        return pd.to_datetime(fecha, errors='coerce', dayfirst=False)
    except (ValueError, TypeError):
        return pd.NaT

def generar_porcentaje_matriz_requerimientos(dashboard=False, texto_fecha=None, thread=None):
    nombre = "Matriz requerimientos"
    hoja = "BD"
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsm"
    anio_actual_copia = fecha_actual.year
    mes_actual_copia = fecha_actual.month
    if mes_actual_copia <= 1:
        anio_actual_copia -= 1
    if os.path.exists(archivo):
        df, proceso = mod_5.lectura_hoja_xlsx(archivo, hoja)
        if proceso:
            columnas = list(df.columns)
            columnas = [(x.strip()).lower().replace(" ","_") for x in columnas]
            df.columns = columnas
            try:
                df = df[["fecha_de_recibido","entidad"]]
            except BaseException:
                texto = lista_a_texto(["Fecha de recibido","Entidad"],", ")
                if thread:
                    thread.message_sent.emit(f"Algunas de las columnas {texto} no se encunetran en el archivo.", "red")
                else:
                    print(f"Algunas de las columnas {texto} no se encunetran en el archivo.")
                return None
            df['fecha_de_recibido'] = (
                df['fecha_de_recibido'].fillna("").astype(str).apply(lambda x: x.replace(" 00:00:00", "").strip()))
            df['fecha_de_recibido'] = (
                df['fecha_de_recibido'].apply(convertir_fecha_2))
            df_filtrado = df[df['fecha_de_recibido'].dt.year == anio_actual_copia]
            largo = len(df_filtrado)
            lista_elementos = list(df["entidad"].unique())
            dic_entidad = {}
            dic = {"Categoria_entidad":[],
                    "Cantidad":[],
                    "Porcentaje_entidad":[],
                    "Anio":[]}
            for elemento in lista_elementos:
                cantidad = len(df_filtrado[df_filtrado["entidad"]==elemento])
                if elemento in categoria_matriz_requerimientos:
                    llave = categoria_matriz_requerimientos[elemento]
                else:
                    llave = "Otros"
                if llave not in dic_entidad:
                    dic_entidad[llave] = 0
                dic_entidad[llave] += cantidad
            for llave, valor in dic_entidad.items():
                porcentaje = round((valor/largo)*100,2)
                dic["Categoria_entidad"].append(llave)
                dic["Cantidad"].append(valor)
                dic["Porcentaje_entidad"].append(str(porcentaje)+" %")
                dic["Anio"].append(anio_actual_copia)
            df = pd.DataFrame(dic)
            if not dashboard:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_matriz_requerimientos")
                lista_nombre = nuevo_nombre.split("\\")
                ext = lista_nombre[-1]
                lista_nombre[-1] = "KPIs"
                nombre_carpeta = lista_a_texto(lista_nombre, "\\")
                crear_carpeta(nombre_carpeta)
                lista_nombre.append(ext)
                nuevo_nombre = lista_a_texto(lista_nombre, "\\")
                almacenar_df_csv_y_excel(df,nuevo_nombre, thread=thread)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_matriz_requerimientos")
                almacenar_df_csv_y_excel(df,nuevo_nombre, thread=thread)
                return nuevo_nombre
        else:
            if thread:
                thread.message_sent.emit(f"No es posible acceder al archivo {archivo}.", "red")
            else:
                print(f"No es posible acceder al archivo {archivo}.")
            return None
    else:
        if thread:
            thread.message_sent.emit(f"No existe el archivo {archivo}. No es posible generar el reporte.", "red")
        else:
            print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

def gastos_AOM(dashboard=False, texto_fecha=None, thread=None):
    nombre = "BD"
    anio_actual = fecha_actual.year
    archivo_csv = ruta_constantes+"\\"+f"{nombre}.csv"
    hoja = "BD"
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsx"
    if os.path.exists(archivo_csv):
        lista_df = lectura_dataframe_chunk(archivo_csv)
        if lista_df:
            df_prueba = lista_df[0].copy()
            columnas = list(df_prueba.columns)
            columnas = [(x.strip()).lower() for x in columnas]
            df_prueba.columns = columnas
            col_1 = "valorinde"
            for i in columnas:
                if col_1 in i:
                    col_1 = i
            columnas_AOM = ["año", "sociedad", col_1, "aom", "negocio"]
            try:
                df_prueba_2 = df_prueba[columnas_AOM]
            except BaseException:
                texto = lista_a_texto(columnas_AOM, ", ")
                if thread:
                    thread.message_sent.emit(f"Algunas de las columnas {texto} no se encuentran en el archivo {nombre}.csv", "red")
                else:
                    print(f"Algunas de las columnas {texto} no se encuentran en el archivo {nombre}.csv")
                return None
            dic = {}
            for df in lista_df:
                df_filtro = df.copy()
                df_filtro.columns = columnas
                df_filtro = df_filtro[columnas_AOM]
                df_filtro = df_filtro[(df_filtro["año"]>2020)&(df_filtro["aom"]=="AOM")]
                df_filtro['negocio'] = df_filtro['negocio'].apply(lambda x: x.strip().capitalize() if isinstance(x, str) else x)
                lista_anios = list(df_filtro["año"].unique())
                lista_filiales = list(df_filtro["sociedad"].unique())
                lista_negocios = list(df_filtro["negocio"].unique())
                for anio in lista_anios:
                    anio_str = str(anio)
                    if anio_str not in dic:
                        dic[anio_str] = {}
                    for filial in lista_filiales:
                        if filial not in dic[anio_str]:
                            dic[anio_str][filial] = {}
                        for negocio in lista_negocios:
                            if negocio not in dic[str(anio)][filial]:
                                dic[anio_str][filial][negocio] = 0
                            df_negocio = df_filtro[(df_filtro["año"]==anio)&(df_filtro["sociedad"]==filial)&(df_filtro["negocio"]==negocio)].reset_index(drop=True)
                            if len(df_negocio):
                                dic[anio_str][filial][negocio] += df_negocio[col_1].sum()
            dic_df = {"Año":[],
                        "Filial":[],
                        "Valor":[],
                        "Negocio":[]}
            for anio, dic_anio in dic.items():
                for filial, dic_filial in dic_anio.items():
                    for negocio, valor in dic_filial.items():
                        dic_df["Año"].append(anio)
                        dic_df["Filial"].append(dic_filiales[filial])
                        dic_df["Valor"].append(valor)
                        dic_df["Negocio"].append(negocio)
            df_AOM = pd.DataFrame(dic_df)
            lista_porcentaje = []
            lista_anios = list(df_AOM["Año"].unique())
            lista_filiales = list(df_AOM["Filial"].unique())
            for anio in lista_anios:
                for filial in lista_filiales:
                    df_total = df_AOM[(df_AOM["Año"]==anio)&(df_AOM["Filial"]==filial)].reset_index(drop=True)
                    v_total = df_total["Valor"].sum()
                    for pos in range(len(df_total)):
                        porcentaje = round((df_total["Valor"][pos]/v_total)*100,2)
                        lista_porcentaje.append(f"{porcentaje} %")
            df_AOM["Porcentaje gastos"] = lista_porcentaje
            lista_anios_df =  list(df_AOM["Año"].unique())
            lista_negocios = list(df_AOM["Negocio"].unique())
            for anio in lista_anios_df:
                df_anio = df_AOM[df_AOM["Año"]==anio].reset_index(drop=True)
                total = df_anio["Valor"].sum()
                for negocio in lista_negocios:
                    lista_fila = []
                    df_filtro = df_anio[df_anio["Negocio"]==negocio].reset_index(drop=True)
                    lista_fila.append(anio)
                    lista_fila.append(grupo_vanti)
                    valor = df_filtro["Valor"].sum()
                    lista_fila.append(valor)
                    lista_fila.append(negocio)
                    porcentaje = str(round((valor/total)*100,2)) + " %" 
                    lista_fila.append(porcentaje)
                    df_AOM.loc[len(df_AOM)] = lista_fila
            if not dashboard:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", str(anio_actual-1), "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"Gastos_AOM_{anio_actual-1}")
                lista_nombre = nuevo_nombre.split("\\")
                ext = lista_nombre[-1]
                lista_nombre[-1] = "KPIs"
                nombre_carpeta = lista_a_texto(lista_nombre, "\\")
                crear_carpeta(nombre_carpeta)
                lista_nombre.append(ext)
                nuevo_nombre = lista_a_texto(lista_nombre, "\\")
                almacenar_df_csv_y_excel(df_AOM,nuevo_nombre, thread=thread)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"Gastos_AOM")
                almacenar_df_csv_y_excel(df_AOM,nuevo_nombre, thread=thread)
                return nuevo_nombre
    elif os.path.exists(archivo):
        lista_hojas = mod_5.hojas_disponibles(archivo)
        proceso = False
        for i in lista_hojas:
            if hoja in i:
                hoja = i
                proceso = True
        if proceso:
            df, proceso = mod_5.lectura_hoja_xlsx(archivo, hoja)
            if proceso:
                almacenar_df_csv_y_excel(df, ruta_constantes+"\\"+f"{nombre}.csv", almacenar_excel=False, thread=thread)
                gastos_AOM()
            else:
                if thread:
                    thread.message_sent.emit(f"No se pudo leer la hoja {hoja} del archivo {nombre}.xlsx", "red")
                else:
                    print(f"No es posible a acceder al archivo {archivo}.")
                return None
        else:
            if thread:
                thread.message_sent.emit(f"No existe un hoja {hoja} en el archivo {nombre}.xlsx", "red")
            else:
                print(f"No existe un hoja {hoja} en el archivo {nombre}.xlsx")
            return None
    else:
        if thread:
            thread.message_sent.emit(f"No existe el archivo {archivo}. No es posible generar el reporte.", "red")
        else:
            print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

def contribuciones_MME(dashboard=False, texto_fecha=None, thread=None):
    nombre = "subsidios"
    anio_actual = fecha_actual.year
    mes_actual = lista_meses[fecha_actual.month-1]
    v_fecha_anterior = fecha_anterior(anio_actual,mes_actual)
    v_fecha_anterior = fecha_anterior(v_fecha_anterior[0], v_fecha_anterior[1])
    archivo_csv = ruta_constantes+"\\"+f"{nombre}.csv"
    if os.path.exists(archivo_csv):
        lista_df = lectura_dataframe_chunk(archivo_csv)
        if lista_df:
            df = pd.concat(lista_df, ignore_index=True)
            lista = ["Mes","Anio","Filial","Causado","Causado_acumulado","Pagado","Deuda","Promedio","KPI"]
            df.columns = lista
            df_filtro = df[(df["Filial"]=="GRUPO")]
            if len(df_filtro):
                mes = int(lista_meses.index(v_fecha_anterior[1])+1)
                anio = int(v_fecha_anterior[0])
                v_ultimos_12_meses = ultimos_12_meses(anio, mes)
                v_ultimos_12_meses.reverse()
                v_meses_anio_actual = meses_anio_actual(anio, mes)
                dic_df_12_meses = {"Filial":[],
                                    "Mes":[],
                                    "Anio":[],
                                    "Causado":[],
                                    "Pagado":[],
                                    "Promedio":[],
                                    "Deuda":[],
                                    "KPI":[]}
                for elemento in v_ultimos_12_meses:
                    df_periodo = df_filtro[(df_filtro["Anio"]==elemento[0]) & (df_filtro["Mes"]==elemento[1])]
                    if len(df_periodo):
                        dic_df_12_meses["Filial"].append(grupo_vanti)
                        dic_df_12_meses["Mes"].append(lista_meses[int(elemento[1])-1])
                        dic_df_12_meses["Anio"].append(elemento[0])
                        dic_df_12_meses["Causado"].append(df_periodo["Causado"].iloc[0])
                        dic_df_12_meses["Pagado"].append(df_periodo["Pagado"].iloc[0])
                        dic_df_12_meses["Promedio"].append(df_periodo["Promedio"].iloc[0])
                        dic_df_12_meses["Deuda"].append(df_periodo["Deuda"].iloc[0])
                        dic_df_12_meses["KPI"].append(df_periodo["KPI"].iloc[0])
                df_12_meses = pd.DataFrame(dic_df_12_meses)
                dic_df_meses_anio = {"Filial":[],
                                    "Mes":[],
                                    "Anio":[],
                                    "Causado":[],
                                    "Pagado":[],
                                    "Promedio":[],
                                    "Deuda":[],
                                    "KPI":[]}
                for elemento in v_meses_anio_actual:
                    df_periodo_1 = df_12_meses[(df_12_meses["Anio"]==elemento[0]) & (df_12_meses["Mes"]==lista_meses[int(elemento[1])-1])]
                    if len(df_periodo_1):
                        dic_df_meses_anio["Filial"].append(grupo_vanti)
                        dic_df_meses_anio["Mes"].append(lista_meses[int(elemento[1])-1])
                        dic_df_meses_anio["Anio"].append(elemento[0])
                        dic_df_meses_anio["Causado"].append(df_periodo_1["Causado"].iloc[0])
                        dic_df_meses_anio["Pagado"].append(df_periodo_1["Pagado"].iloc[0])
                        dic_df_meses_anio["Promedio"].append(df_periodo_1["Promedio"].iloc[0])
                        dic_df_meses_anio["Deuda"].append(df_periodo_1["Deuda"].iloc[0])
                        dic_df_meses_anio["KPI"].append(df_periodo_1["KPI"].iloc[0])
                df_meses_anio = pd.DataFrame(dic_df_meses_anio)
                if len(df_12_meses) and len(df_meses_anio):
                    if not dashboard:
                        lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                        nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"subsidios_KPI")
                        lista_nombre = nuevo_nombre.split("\\")
                        ext = lista_nombre[-1]
                        lista_nombre[-1] = "KPIs"
                        nombre_carpeta = lista_a_texto(lista_nombre, "\\")
                        crear_carpeta(nombre_carpeta)
                        lista_nombre.append(ext)
                        nuevo_nombre = lista_a_texto(lista_nombre, "\\")
                        almacenar_df_csv_y_excel(df_12_meses,nuevo_nombre, thread=thread)
                        lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", str(anio_actual), "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                        nuevo_nombre_1 = encontrar_ubi_archivo(lista_ubi, f"subsidios_KPI_anio")
                        lista_nombre = nuevo_nombre_1.split("\\")
                        ext = lista_nombre[-1]
                        lista_nombre[-1] = "KPIs"
                        nombre_carpeta = lista_a_texto(lista_nombre, "\\")
                        crear_carpeta(nombre_carpeta)
                        lista_nombre.append(ext)
                        nuevo_nombre_1 = lista_a_texto(lista_nombre, "\\")
                        almacenar_df_csv_y_excel(df_meses_anio,nuevo_nombre_1, thread=thread)
                        return nuevo_nombre, nuevo_nombre_1
                    else:
                        lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                        nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"subsidios_KPI")
                        almacenar_df_csv_y_excel(df_12_meses,nuevo_nombre, thread=thread)
                        lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", str(anio_actual), "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                        nuevo_nombre_1 = encontrar_ubi_archivo(lista_ubi, f"subsidios_KPI_anio")
                        almacenar_df_csv_y_excel(df_meses_anio,nuevo_nombre_1, thread=thread)
                        return nuevo_nombre, nuevo_nombre_1
                else:
                    return None, None
            else:
                if thread:
                    thread.message_sent.emit("\nNo hay datos disponibles para la filial GRUPO.\n", "red")
                else:
                    print("No hay datos disponibles para la filial GRUPO.")
                return None, None
        else:
            if thread:
                thread.message_sent.emit(f"No es posible a acceder al archivo {archivo_csv}, revisar la estructura del mismo.", "red")
            else:
                print(f"No es posible a acceder al archivo {archivo_csv}, revisar la estructura del mismo.")
            return None, None
    else:
        if thread:
            thread.message_sent.emit(f"No existe el archivo {archivo_csv}. No es posible generar el reporte.", "red")
        else:
            print(f"No existe el archivo {archivo_csv}. No es posible generar el reporte.")
        return None, None

def tarifas_distribuidoras_GN(thread=None):
    max_bola = 65
    nombre = "tarifas_nacionales"
    hoja = nombre
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsx"
    if os.path.exists(archivo):
        lista_hojas = mod_5.hojas_disponibles(archivo)
        proceso = False
        for i in lista_hojas:
            if hoja in i:
                hoja = i
                proceso = True
        if proceso:
            df, proceso = mod_5.lectura_hoja_xlsx(archivo, hoja)
            if proceso:
                dic_tarifas = {}
                df['Fecha'] = pd.to_datetime(df[['Anio', 'Mes']].rename(columns={'Anio': 'year', 'Mes': 'month'}).assign(day=1))
                fecha_max = df['Fecha'].max().strftime('%m-%Y')
                lista_fecha_max = fecha_max.split("-")
                mes_final = int(lista_fecha_max[0])
                anio_final = int(lista_fecha_max[1])
                mes = lista_meses[int(lista_fecha_max[0])-1]
                anio = lista_fecha_max[1]
                fecha_min = fecha_anterior(anio, mes)
                mes_inicial = lista_meses.index(fecha_min[1])+1
                anio_inicial = int(fecha_min[0])
                df_fecha_max = df[((df['Fecha'].dt.month == mes_final) & (df['Fecha'].dt.year == anio_inicial))]
                df_fecha_min = df[((df['Fecha'].dt.month == mes_inicial) & (df['Fecha'].dt.year == anio_final))]
                if len(df_fecha_max) and len(df_fecha_min):
                    lista_empresas = list(df_fecha_max['Empresa'].unique())
                    for empresa in lista_empresas:
                        df_empresa_max = df_fecha_max[df_fecha_max['Empresa'] == empresa].reset_index(drop=True)
                        df_empresa_min = df_fecha_min[df_fecha_min['Empresa'] == empresa].reset_index(drop=True)
                        if len(df_empresa_max) and len(df_empresa_min):
                            if empresa not in dic_tarifas:
                                dic_tarifas[empresa] = {}
                                valor = round(df_empresa_max["Cuv"][0])
                                if valor > 1000:
                                    valor = f"{valor/1e3:0.3f}"
                                valor = str(valor)
                                dic_tarifas[empresa]["Tarifa"] = valor
                                dic_tarifas[empresa]["Ciudad"] = dic_ciudades[empresa]
                                if df_empresa_min["Cuv"][0] < df_empresa_max["Cuv"][0]:
                                    cambio = "red"
                                elif df_empresa_min["Cuv"][0] > df_empresa_max["Cuv"][0]:
                                    cambio = "green"
                                else:
                                    cambio = "orange"
                                dic_tarifas[empresa]["Cambio"] = cambio
                    df_empresa_max = df_fecha_max.sort_values(by=['Cuv'], ascending=False).reset_index(drop=True)
                    v_max = df_empresa_max["Cuv"].max()
                    for i in range(len(df_empresa_max)):
                        bola = int((df_empresa_max["Cuv"][i]/v_max)*max_bola)
                        dic_tarifas[df_empresa_max["Empresa"][i]]["Bola"] = bola
                    dic_tarifas = dict(sorted(dic_tarifas.items(), key=lambda item: item[1]['Tarifa']))
                    return dic_tarifas
                else:
                    return None
            else:
                if thread:
                    thread.message_sent.emit(f"No es posible a acceder al archivo {archivo}.", "red")
                else:
                    print(f"No es posible a acceder al archivo {archivo}.")
                return None
        else:
            if thread:
                thread.message_sent.emit(f"No existe un hoja {hoja} en el archivo {nombre}.xlsx", "red")
            else:
                print(f"No existe un hoja {hoja} en el archivo {nombre}.xlsx")
            return None
    else:
        if thread:
            thread.message_sent.emit(f"No existe el archivo {archivo}. No es posible generar el reporte.", "red")
        else:
            print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

def cumplimientos_SUI_distribuidoras(thread=None):
    nombre = "Cumplimientos_SUI"
    hoja = nombre
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsx"
    if os.path.exists(archivo):
        lista_hojas = mod_5.hojas_disponibles(archivo)
        proceso = False
        for i in lista_hojas:
            if hoja in i:
                hoja = i
                proceso = True
        if proceso:
            df, proceso = mod_5.lectura_hoja_xlsx(archivo, hoja)
            if proceso:
                df["Fecha_act"] = pd.to_datetime(df['Fecha_act'])
                fecha_reciente = max(list(df["Fecha_act"].unique()))
                df_fecha_reciente = df[df["Fecha_act"] == fecha_reciente].reset_index(drop=True)
                lista_estado = list(df_fecha_reciente["Estado"].unique())
                dic = {grupo_vanti:{"Certificado":0,"Pendiente":0},
                        "Distribuidoras":{"Certificado":0,"Pendiente":0}}
                df_vanti = df_fecha_reciente[df_fecha_reciente['Distribuidora'].isin(lista_filiales)]
                for i in lista_estado:
                    llave = "Certificado"
                    if i == "Pendiente":
                        llave = "Pendiente"
                    dic["Distribuidoras"][llave] += df_fecha_reciente[df_fecha_reciente["Estado"]==i]["Cantidad"].sum()
                    dic[grupo_vanti][llave] += df_vanti[df_vanti["Estado"]==i]["Cantidad"].sum()
                return dic
            else:
                if thread:
                    thread.message_sent.emit(f"No es posible a acceder al archivo {archivo}.", "red")
                else:
                    print(f"No es posible a acceder al archivo {archivo}.")
                return None
        else:
            if thread:
                thread.message_sent.emit(f"No existe un hoja {hoja} en el archivo {nombre}.xlsx", "red")
            else:
                print(f"No existe un hoja {hoja} en el archivo {nombre}.xlsx")
            return None
    else:
        if thread:
            thread.message_sent.emit(f"No existe el archivo {archivo}. No es posible generar el reporte.", "red")
        else:
            print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

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

def apoyo_reporte_tarifas_mensual(lista_archivos,informar,filial,almacenar_excel=True,thread=None):
    for archivo in lista_archivos:
        lista_df = lectura_dataframe_chunk(archivo)
        if lista_df:
            anio_archivo = lista_df[0]["Anio_reportado"][0]
            mes_archivo = lista_df[0]["Mes_reportado"][0]
            for df in lista_df:
                df_filtro = df[(df["Tarifa_1"]>0)|(df["Tarifa_2"]>0)].reset_index(drop=True).copy()
                df_filtro["Filial"] = dic_filiales[filial]
                df_filtro = lista_porcentaje_df_tarifas(df_filtro)
                df_filtro["Anio_reportado"] = anio_archivo
                df_filtro["Mes_reportado"] = mes_archivo
            nombre = archivo.replace("_resumen.csv","_reporte_tarifario.csv")
            almacenar_df_csv_y_excel(df_filtro, nombre, informar, almacenar_excel, thread=thread)
            return df_filtro, nombre
        else:
            return None, None

def reporte_tarifas_mensual(dic_archivos, seleccionar_reporte, informar=True, almacenar_excel=True, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df,nombre = apoyo_reporte_tarifas_mensual(lista_archivos_filial,informar,filial,thread=thread)
                if nombre:
                    lista_df_filiales.append(df)
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales, ignore_index=True)
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel, thread=thread)

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Técnicos
# * -------------------------------------------------------------------------------------------------------

def apoyo_generar_reporte_indicadores_tecnicos_mensual(lista_archivos, informar, filial, almacenar_excel=True, thread=None):
    for archivo in lista_archivos:
        df = leer_dataframe_utf_8(archivo)
        anio_archivo = df["Anio_reportado"][0]
        mes_archivo = df["Mes_reportado"][0]
        df["Filial"] = dic_filiales[filial]
        df["NIT"] = dic_nit[dic_filiales[filial]]
        df = df[["NIT","Filial","Anio_reportado","Mes_reportado","IPLI","IO","IRST_EG","DES_NER","Suscriptores_DES_NER","Cantidad_eventos_DES_NER"]]
        df["IPLI"] = (df["IPLI"] * 100).round(2)
        df["IO"] = (df["IO"] * 100).round(2)
        df["IRST_EG"] = (df["IRST_EG"] * 100).round(2)
        df["Anio_reportado"] = anio_archivo
        df["Mes_reportado"] = mes_archivo
        nuevo_nombre = archivo.replace("_resumen.csv", "_indicador_tecnico.csv")
        almacenar_df_csv_y_excel(df, nuevo_nombre, informar, almacenar_excel, thread=thread)
        return df, nuevo_nombre

def generar_reporte_indicadores_tecnicos_mensual(dic_archivos, seleccionar_reporte, informar=True,almacenar_excel=True, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df,nombre = apoyo_generar_reporte_indicadores_tecnicos_mensual(lista_archivos_filial, informar, filial, thread=thread)
                if nombre:
                    lista_df_filiales.append(df)
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales, ignore_index=True)
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_")
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel, thread=thread)

def formato_fecha(fecha):
    fecha = str(fecha).replace("-","").replace(":","").replace("/","").zfill(8)
    return fecha

def formato_hora(hora):
    hora = str(hora).replace("-","").replace(":","").replace("/","").zfill(4)
    return hora

def diferencia_minutos_fechas(df, lista_dia_1, lista_hora_1, lista_dia_2, lista_hora_2):
    lista_dif_minutos = []
    for i in range(len(lista_dia_1)):
        try:
            fecha_1 = datetime.strptime(f"{formato_fecha(lista_dia_1[i])} {formato_hora(lista_hora_1[i])}", '%d%m%Y %H%M')
            fecha_2 = datetime.strptime(f"{formato_fecha(lista_dia_2[i])} {formato_hora(lista_hora_2[i])}", '%d%m%Y %H%M')
            diferencia = float(round((fecha_2-fecha_1).total_seconds() / 60))
        except BaseException:
            diferencia = float(0)
        lista_dif_minutos.append(diferencia)
    df["Cantidad_minutos"] = lista_dif_minutos
    return df

def porcentaje_tipo_evento_minutos(df, lista_eventos):
    lista_valores = []
    for evento in lista_eventos:
        df_filtro = df[df["Tipo_evento"] == evento].reset_index(drop=True)
        suma_evento = df_filtro["Cantidad_eventos"].sum()
        for clasif in list(df_filtro["Clasificacion"].unique()):
            valor = df_filtro[df_filtro["Clasificacion"] == clasif]["Cantidad_eventos"].sum()
            if suma_evento > 0:
                lista_valores.append(str(round((valor/suma_evento)*100,2))+" %")
            else:
                lista_valores.append("0 %")
    df["Porcentaje_cantidad_eventos"] = lista_valores
    return df

def porcentaje_tipo_evento(df):
    lista_valores = []
    suma = df["Cantidad_eventos"].sum()
    for evento in list(df["Tipo_evento"].unique()):
        if suma > 0:
            valor = df[df["Tipo_evento"] == evento]["Cantidad_eventos"].sum()
            lista_valores.append(str(round((valor/suma)*100,2))+" %")
        else:
            lista_valores.append("0 %")
    df["Porcentaje_cantidad_eventos"] = lista_valores
    return df

def apoyo_generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos, filial, informar=True, almacenar_excel=True, thread=None):
    for archivo in lista_archivos:
        df = leer_dataframe_utf_8(archivo)
        anio_archivo = df["Anio_reportado"][0]
        mes_archivo = df["Mes_reportado"][0]
        df['Observaciones'] = df['Observaciones'].str.replace("CONTROLADA", "CONTROLADO").astype(str)
        df['Observaciones'] = np.where(df['Observaciones'].str.contains('NO CONTR', case=False), 'NO CONTROLADO', df['Observaciones'])
        df['Observaciones'] = df['Observaciones'].str.strip().astype(str)
        df = diferencia_minutos_fechas(df, list(df["Fecha_solicitud"]), list(df["Hora_solicitud"]), list(df["Fecha_llegada_servicio_tecnico"]), list(df["Hora_llegada_servicio_tecnico"]))
        df['Hora_solicitud'] = df['Hora_solicitud'].apply(lambda x: int(str(x).replace(':', '').replace('/', '').replace('-', '').zfill(4)[:2]))
        lista_eventos = list(df["Observaciones"].unique())
        dic_df_evento = {"Tipo_evento":[],
                        "Cantidad_eventos":[],
                        "Tiempo_promedio_llegada (min)":[]}
        dic_minutos_evento = {}
        for evento in lista_eventos:
            df_filtro = df[df["Observaciones"] == evento].reset_index(drop=True)
            if "NO CONTROL" in evento:
                dic_minutos_evento[evento] = {"< 60 min":((0,60),[]),
                                            "> 1 hora":((60,float("inf")),[]),}
            else:
                dic_minutos_evento[evento] = {"< 12 horas":((0,int(60*12)),[]),
                                            "> 12 horas":((int(12*60),float("inf")),[]),}
            for i in range(len(df_filtro)):
                for llave, tupla in dic_minutos_evento[evento].items():
                    if tupla[0][0] < df_filtro["Cantidad_minutos"][i] <= tupla[0][1]:
                        dic_minutos_evento[evento][llave][1].append(float(df_filtro["Cantidad_minutos"][i]))
            dic_df_evento["Tipo_evento"].append(evento)
            dic_df_evento["Cantidad_eventos"].append(len(df_filtro))
            dic_df_evento["Tiempo_promedio_llegada (min)"].append(round(df_filtro["Cantidad_minutos"].mean()))
        nombre = archivo.replace("_resumen.csv","_indicador_tecnico_IRST.csv")
        nombre_1 = archivo.replace("_resumen.csv","_indicador_tecnico_IRST_minutos.csv")
        nombre_2 = archivo.replace("_resumen.csv","_indicador_tecnico_IRST_horas.csv")
        dic_df_evento_minutos = {"Tipo_evento":[],
                                "Clasificacion":[],
                                "Cantidad_eventos":[]}
        for evento in dic_minutos_evento:
            for llave, valor in dic_minutos_evento[evento].items():
                dic_df_evento_minutos["Tipo_evento"].append(evento)
                dic_df_evento_minutos["Clasificacion"].append(llave)
                dic_df_evento_minutos["Cantidad_eventos"].append(len(valor[1]))
        df2 = pd.DataFrame(dic_df_evento_minutos)
        df2 = porcentaje_tipo_evento_minutos(df2, lista_eventos)
        df2["Filial"] = dic_filiales[filial]
        df2["NIT"] = dic_nit[dic_filiales[filial]]
        df2["Anio_reportado"] = anio_archivo
        df2["Mes_reportado"] = mes_archivo
        almacenar_df_csv_y_excel(df2, nombre_1, informar, almacenar_excel, thread=thread)
        df1 = pd.DataFrame(dic_df_evento)
        df1 = porcentaje_tipo_evento(df1)
        df1["Filial"] = dic_filiales[filial]
        df1["NIT"] = dic_nit[dic_filiales[filial]]
        df1["Anio_reportado"] = anio_archivo
        df1["Mes_reportado"] = mes_archivo
        almacenar_df_csv_y_excel(df1, nombre, informar, almacenar_excel, thread=thread)
        dic_horas_evento = {}
        for evento in lista_eventos:
            df_filtro = df[df["Observaciones"] == evento].reset_index(drop=True)
            if "NO CONTROL" in evento:
                dic_horas_evento[evento] = {}
                for hora in range(24):
                    dic_horas_evento[evento][hora] = {"0 - 30 min":((0,30),[]),
                                                    "30 - 60 min":((30,60),[]),
                                                    "> 1 hora":((60,float("inf")),[])}
            else:
                dic_horas_evento[evento] = {}
                for hora in range(24):
                    dic_horas_evento[evento][hora] = {"< 1 día":((0,int(60*24)),[]),
                                                    "1 - 2 días":((int(60*24),int(60*24*2)),[]),
                                                    "> 2 dias":((int(60*24*2),float("inf")),[])}
            for i in range(len(df_filtro)):
                hora = int(df_filtro["Hora_solicitud"][i])
                for llave, tupla in dic_horas_evento[evento][hora].items():
                    if tupla[0][0] < df_filtro["Cantidad_minutos"][i] <= tupla[0][1]:
                        dic_horas_evento[evento][hora][llave][1].append(float(df_filtro["Cantidad_minutos"][i]))
        dic_df_evento_horas = {"Tipo_evento":[],
                                "Clasificacion":[],
                                "Hora_solicitud":[],
                                "Cantidad_eventos":[]}
        for evento in dic_horas_evento:
            for hora in dic_horas_evento[evento]:
                for llave, valor in dic_horas_evento[evento][hora].items():
                    dic_df_evento_horas["Tipo_evento"].append(evento)
                    dic_df_evento_horas["Clasificacion"].append(llave)
                    dic_df_evento_horas["Hora_solicitud"].append(hora)
                    dic_df_evento_horas["Cantidad_eventos"].append(len(valor[1]))
        df3 = pd.DataFrame(dic_df_evento_horas)
        df3["Filial"] = dic_filiales[filial]
        df3["NIT"] = dic_nit[dic_filiales[filial]]
        df3["Anio_reportado"] = anio_archivo
        df3["Mes_reportado"] = mes_archivo
        almacenar_df_csv_y_excel(df3, nombre_2, informar, almacenar_excel, thread=thread)
        return df1, nombre, df2, nombre_1, df3, nombre_2

def generar_reporte_indicadores_tecnicos_IRST_mensual(dic_archivos, seleccionar_reporte, informar=True,almacenar_excel=True,thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales_1 = []
        lista_df_filiales_2 = []
        lista_df_filiales_3 = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df1,nombre_1,df2,nombre_2,df3,nombre_3 = apoyo_generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos_filial,filial, informar, almacenar_excel,thread=thread)
                if nombre_1:
                    lista_df_filiales_1.append(df1)
                if nombre_2:
                    lista_df_filiales_2.append(df2)
                if nombre_3:
                    lista_df_filiales_3.append(df3)
        if len(lista_df_filiales_1) and len(lista_filiales_archivo) == 4:
            df_total, nuevo_nombre = generar_formato_almacenamiento_reportes(lista_df_filiales_1, nombre_1, informar,almacenar_excel,thread=thread)
        if len(lista_df_filiales_2) and len(lista_filiales_archivo) == 4:
            df_total_2, nuevo_nombre_2 = generar_formato_almacenamiento_reportes(lista_df_filiales_2, nombre_2, informar,almacenar_excel,thread=thread)
        if len(lista_df_filiales_3) and len(lista_filiales_archivo) == 4:
            df_total_3, nuevo_nombre_3 = generar_formato_almacenamiento_reportes(lista_df_filiales_3, nombre_3, informar,almacenar_excel,thread=thread)

def apoyo_generar_reporte_suspension_mensual(lista_archivos,informar,filial,thread=None):
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
                nombre = archivo.replace("_resumen.csv","_reporte_suspension.csv")
                almacenar_df_csv_y_excel(df1, nombre, thread=thread)
            return df1, nombre
        else:
            return None, None
    return None, None

def generar_reporte_suspension_mensual(dic_archivos, seleccionar_reporte, informar=True, almacenar_excel=True, thread=None):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df,nombre = apoyo_generar_reporte_suspension_mensual(lista_archivos_filial,informar,filial, thread=thread)
            if nombre:
                lista_df_filiales.append(df)
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales, ignore_index=True)
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, thread=thread)

# * -------------------------------------------------------------------------------------------------------
# *                                             Menú de Cumplimiento de Reportes Regulatorios
# * -------------------------------------------------------------------------------------------------------
def encontrar_ubi_archivo(lista, nombre):
    ruta_actual = lista[0]
    for ruta in lista[1:]:
        carpetas = buscar_carpetas(ruta_actual)
        for carpeta in carpetas:
            if carpeta.endswith((ruta)):
                ruta_actual = carpeta
    return ruta_actual+"\\"+nombre+".csv"

def generar_porcentaje_cumplimientos_regulatorios(dashboard=False, texto_fecha=None, thread=None):
    nombre = "Reporte SUI"
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsx"
    if os.path.exists(archivo):
        df, proceso = mod_5.lectura_hoja_xlsx(archivo, nombre)
        if proceso:
            anio_actual_copia = fecha_actual.year
            mes_actual_copia = fecha_actual.month
            if mes_actual_copia <= 1:
                anio_actual_copia -= 1
            df['Fecha_establecida'] = pd.to_datetime("1899-12-30") + pd.to_timedelta(df['Fecha establecida'], unit="D")
            df = df.loc[df['Fecha_establecida'].dt.year == int(anio_actual_copia)]
            lista_estado = list(df["Estado Certificado"].unique())
            lista_filiales = list(df["Empresa"].unique())
            largo = len(df)
            dic_df = {"Filial":[],
                        "Estado":[],
                        "Cantidad_reportes":[],
                        "Porcentaje_cumplimiento":[]}
            for filial in lista_filiales:
                df_filial = df[df["Empresa"]==filial]
                for estado in lista_estado:
                    df_estado = df_filial[df_filial["Estado Certificado"]==estado]
                    dic_df["Filial"].append(filial)
                    dic_df["Estado"].append(estado)
                    dic_df["Cantidad_reportes"].append(len(df_estado))
                    dic_df["Porcentaje_cumplimiento"].append(str(round((len(df_estado)/len(df_filial))*100,2))+" %")
            for estado in lista_estado:
                df_estado = df[df["Estado Certificado"]==estado]
                dic_df["Filial"].append(grupo_vanti)
                dic_df["Estado"].append(estado)
                dic_df["Cantidad_reportes"].append(len(df_estado))
                dic_df["Porcentaje_cumplimiento"].append(str(round((len(df_estado)/largo)*100,2))+" %")
            df_porcentaje = pd.DataFrame(dic_df)
            df_porcentaje["Anio"] = anio_actual_copia
            if not dashboard:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", str(anio_actual_copia), "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, "porcentaje_cumplimientos_regulatorios")
                lista_nombre = nuevo_nombre.split("\\")
                ext = lista_nombre[-1]
                lista_nombre[-1] = "KPIs"
                nombre_carpeta = lista_a_texto(lista_nombre, "\\")
                crear_carpeta(nombre_carpeta)
                lista_nombre.append(ext)
                nuevo_nombre = lista_a_texto(lista_nombre, "\\")
                almacenar_df_csv_y_excel(df_porcentaje,nuevo_nombre, thread=thread)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_cumplimientos_regulatorios")
                almacenar_df_csv_y_excel(df_porcentaje,nuevo_nombre, thread=thread)
                return nuevo_nombre
        else:
            if thread:
                thread.message_sent.emit(f"No es posible acceder al archivo {archivo}.", "red")
            else:
                print(f"No es posible acceder al archivo {archivo}.")
            return None
    else:
        if thread:
            thread.message_sent.emit(f"No existe el archivo {archivo}. No es posible generar el reporte.", "red")
        else:
            print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Anuales
# * -------------------------------------------------------------------------------------------------------

def union_archivos_mensuales_anual(dic_archivos, seleccionar_reporte, informar=True, almacenar_excel=True, thread=None):
    if not len(seleccionar_reporte["filial"]) == 4:
        return None
    fecha_nombre = (seleccionar_reporte["fecha_personalizada"][0][0]+"_"+seleccionar_reporte["fecha_personalizada"][0][1].upper()
                    +"_"+seleccionar_reporte["fecha_personalizada"][1][0]+"_"+seleccionar_reporte["fecha_personalizada"][1][1].upper())
    lista_anual = []
    for fecha, lista_archivos in dic_archivos.items():
        for archivo in lista_archivos:
            df = leer_dataframe_utf_8(archivo)
            nombre = archivo
            if len(df):
                lista_anual.append(df)
    if len(lista_anual):
        lista_nombre = nombre.split("\\")
        lista_nombre[-5] = "00. Compilado"
        lista_nombre[-3] = "00. Compilado"
        ext_nombre = lista_nombre[-1].split("_")
        if "DS" in ext_nombre and "metricas" in ext_nombre:
            ext_nombre.pop(0)
        ext_nombre.pop(0)
        ext_nombre[0] = fecha_nombre
        lista_nombre[-1] = lista_a_texto(ext_nombre, "_")
        crear_carpeta_anual(fecha_nombre, lista_nombre, thread=thread)
        lista_nombre.insert(-2, fecha_nombre)
        nombre = lista_a_texto(lista_nombre, "\\")
        df_anual = pd.concat(lista_anual)
        almacenar_df_csv_y_excel(df_anual, nombre, informar, almacenar_excel, thread=thread)
        return nombre
    else:
        return None

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

def unir_listas_anio_tri(lista_anios, lista_tri):
    lista_anio_tri = []
    for j in lista_anios:
        for i in lista_tri:
            lista_anio_tri.append(f"{j} - {i}")
    return lista_anio_tri

# * -------------------------------------------------------------------------------------------------------
# *                                             Búsqueda archivos
# * -------------------------------------------------------------------------------------------------------
def busqueda_archivos_tipo(ubi_archivo, tipo=None, lista_fallidos=[]):
    if tipo:
        archivos_tipo = glob.glob(os.path.join(ubi_archivo, "*"+tipo))
    else:
        archivos_tipo = glob.glob(os.path.join(ubi_archivo, "*"))
    return archivos_tipo

def busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra=[], thread=None, informar=True):
    tipo_evitar = tipo.replace(".csv","").replace(".CSV","").replace(".TXT","").replace(".txt","")
    lista_evitar_extra_copia = evitar_extra.copy()
    if len(tipo_evitar):
        lista_evitar_extra_copia.append(tipo_evitar)
    lista_evitar = especificar_lista_reportes_generados(lista_evitar_extra_copia)
    lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
    if not len(lista_archivos):
        if informar:
            if thread:
                thread.message_sent.emit(f"No se encontraron archivos con la extensión {tipo}", "red")
            else:
                print("\nNo se encontraron archivos con la extensión {tipo}\n")
        return False,lista_archivos
    else:
        return True,lista_archivos

def busqueda_archivos_tipo_reporte_anual(tipo, seleccionar_reporte, evitar_extra=[], informar=True, todos=False, thread=None):
    if todos:
        lista_evitar = []
    else:
        tipo_evitar = tipo.replace(".csv","").replace(".CSV","").replace(".TXT","").replace(".txt","")
        lista_evitar_extra_copia = evitar_extra.copy()
        if len(tipo_evitar):
            lista_evitar_extra_copia.append(tipo_evitar)
        lista_evitar = especificar_lista_reportes_generados(lista_evitar_extra_copia)
    lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte_anual(seleccionar_reporte, tipo, lista_evitar)
    if len(lista_archivos) == 0:
        if informar:
            if thread:
                thread.message_sent.emit(f"No se encontraron archivos con la extensión {tipo}", "red")
            else:
                print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
        return False,lista_archivos
    else:
        return True,lista_archivos

def especificar_lista_reportes_generados(lista_1):
    lista = lista_reportes_generados.copy()
    if len(lista_1):
        for i in lista_1:
            try:
                lista.remove(i)
            except ValueError:
                pass
    return lista


def mostrar_texto(texto, tipo="texto"):
    linea = 200
    if tipo == "salto":
        print("\n")
    elif tipo == "linea":
        print("-"*linea)
    elif tipo == "texto":
        n = (linea-len(texto))//2
        print("\n"+" "*n+" "+texto+" "+" "*n+"\n")

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

# * -------------------------------------------------------------------------------------------------------
# *                                            Aplicativo
# * -------------------------------------------------------------------------------------------------------

def obtener_reporte(info):
    dic_reportes = info["Reporte"]
    for llave, dic_llave in dic_reportes.items():
        for reporte, lista_reporte in dic_llave.items():
            if lista_reporte[0]:
                return reporte
    return None

def obtener_categoria(info):
    dic_categorias = info["Categoria"]
    dic_categorias_c = {"Reportes comercial":"Comercial",
                    "Reporte tarifario":"Tarifario",
                    "Reporte técnico":"Tecnico"}
    for llave, lista_llave in dic_categorias.items():
        if lista_llave[0]:
            if llave in dic_categorias_c:
                return dic_categorias_c[llave]
    return None

def almacenar_archivos_2(ruta_guardar_archivos, thread):
    archivos_aceptados_constantes(busqueda_archivos_tipo(ruta_guardar_archivos), thread=thread)
    lista_archivos = busqueda_archivos_tipo(ruta_guardar_archivos)
    lista_archivos = archivos_tipo_csv_txt(lista_archivos)
    lista_carpetas = buscar_carpetas(ruta_nuevo_sui)
    ubi = None
    for i in lista_carpetas:
        if dic_carpetas["carpeta_2"][0] in i:
            ubi = i
    lista_fallidos = []
    lista_fallidos = conversion_archivos_CSV(lista_archivos, lista_fallidos=lista_fallidos)
    lista_fallidos = conversion_archivos_lista(lista_archivos, "TXT", "txt", informar=False, lista_fallidos=lista_fallidos, thread=thread)
    lista_fallidos = conversion_archivos_lista(lista_archivos, "txt", "csv", informar=False, lista_fallidos=lista_fallidos, thread=thread)
    lista_fallidos = evaluar_archivos_prueba(lista_archivos, lista_fallidos=lista_fallidos)
    lista_fallidos = list(set(lista_fallidos))
    lista_archivos = busqueda_archivos_tipo(ruta_guardar_archivos, lista_fallidos=lista_fallidos)
    lista_archivos = retirar_archivos_fallidos(lista_archivos, lista_fallidos, thread=thread)
    lista_archivos = cantidad_minima_info_archivo(lista_archivos)
    for archivo in lista_archivos:
        bool_DS = False
        bool_GRTT2SAP = False
        try:
            nombre_archivo = archivo.split("\\")[-1].replace(" ", "_")
            for i in range(9):
                j = 10 - i
                nombre_archivo = nombre_archivo.replace("_" * j, "_")
            nombre_archivo_lista = nombre_archivo.split(".")
            nombre_archivo_lista[0] = nombre_archivo_lista[0].upper()
            lista_nombre_aux = nombre_archivo_lista[0].split("_")
            nombre_archivo_lista[0] = formato_ext_archivo(lista_nombre_aux, texto=True)
            nombre_archivo = lista_a_texto(nombre_archivo_lista, ".")
            ext_archivo = nombre_archivo.split("_")
            ext_archivo[-1] = ext_archivo[-1].split(".")[0]
            ext_archivo = formato_ext_archivo(ext_archivo)
            tipo = ext_archivo[0]
            if tipo == "GRTT2SAP":
                tipo = "GRTT2"
                bool_GRTT2SAP = True
            elif tipo in lista_archivo_desviaciones:
                tipo = "DS"
                ext_archivo[4] = ext_archivo[4].upper()
                bool_DS = True
            categoria = encontrar_categoria_reporte(tipo)
            ext_archivo[3] = ext_archivo[3].lower().capitalize()
            ext_archivo.append(categoria)
            if None not in ext_archivo:
                if comprobar_info_nombre_archivo(ext_archivo):
                    ubi_1 = encontrar_nueva_ubi_archivo(ubi, ext_archivo)
                    nueva_ubi = ubi_1 + "\\" + nombre_archivo
                    if bool_GRTT2SAP:
                        lista_nueva_ubi = nueva_ubi.split("\\")
                        valor = lista_nueva_ubi[-1]
                        lista_nueva_ubi[-1] = "00. GRTT2"
                        lista_nueva_ubi.append(valor)
                        nueva_ubi = lista_a_texto(lista_nueva_ubi, "\\")
                    if bool_DS:
                        lista_nueva_ubi = nueva_ubi.split("\\")
                        valor = lista_nueva_ubi[-1]
                        lista_nueva_ubi[-1] = "11. DS"
                        lista_nueva_ubi.append(valor)
                        nueva_ubi = lista_a_texto(lista_nueva_ubi, "\\")
                    shutil.move(archivo, nueva_ubi)
                    if thread:
                        thread.message_sent.emit(f"Archivo creado: {acortar_nombre(nueva_ubi)}", "white")
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
        except BaseException:
            pass

def conversion_archivos_txt(lista_reportes, eliminar=False, thread=None, tipo=".txt"):
    for reporte in lista_reportes:
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(reporte, tipo, [])
        lista_archivos.extend(mod_4.encontrar_archivos_seleccionar_reporte(reporte, tipo.upper(), []))
        if len(lista_archivos) == 0:
            if thread:
                thread.message_sent.emit(f"No se encontraron archivos con la extensión {tipo}", "red")
            else:
                print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
        else:
            if thread:
                thread.message_sent.emit(f"Inicio de procesamiento para: Conversión de archivos {tipo} a .csv", "green")
                conversion_archivos_lista(lista_archivos,"txt","csv")
                if eliminar:
                    eliminar_archivos(lista_archivos)

def reportes_disponibles_app(reporte, thread=None):
    v_fecha_siguiente = fecha_siguiente(reporte["fecha_personalizada"][0][0], reporte["fecha_personalizada"][0][1])
    v_fecha_siguiente = (v_fecha_siguiente[0], v_fecha_siguiente[1])
    reporte["fecha_personalizada"][0] = v_fecha_siguiente
    proceso, dic_archivos_mostrar = generar_archivos_extra_anual(reporte, thread=thread, evitar_extra=lista_reportes_generados, reportes_app=True)
    if proceso:
        thread.message_sent.emit("Archivos disponibles para la selección realizada: ", "green")
        for fecha, lista in dic_archivos_mostrar.items():
            thread.message_sent.emit(f"{fecha}", "white")
            for elemento in lista:
                    thread.message_sent.emit(f"\t{elemento}", "white")

def reportes_disponibles_Nuevo_SUI(lista_reportes, thread=None):
    for reporte in lista_reportes:
        busqueda_archivos_general(reporte, thread=thread)

def busqueda_archivos_general(seleccionar_reporte, tipo=None, evitar_extra=[],informar=True, thread=None):
    formato_app = False
    if thread:
        formato_app = True
    lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, evitar_extra)
    if not len(lista_archivos):
        if informar:
            if thread:
                thread.message_sent.emit(f"No se encontraron archivos con la extensión {tipo}", "red")
            else:
                print(f"\nNo se encontraron archivos en la ubicación seleccionada\n")
    else:
        lista_archivos_formato = []
        for archivo in lista_archivos:
            if archivo.endswith((".csv",".zip",".json",".xlsx")):
                lista_archivos_formato.append(archivo)
        proceso, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos_formato, formato_app=formato_app)
        if proceso:
            thread.message_sent.emit("Archivos disponibles para la selección realizada: ", "green")
            for fecha, dic_fecha in dic_archivos_mostrar.items():
                thread.message_sent.emit(f"{fecha}", "white")
                for filial, lista_archivos_filial in dic_fecha.items():
                    thread.message_sent.emit(f"\t{filial}", "white")
                    for elemento in lista_archivos_filial:
                        thread.message_sent.emit(f"\t\t{elemento}", "white")


def generar_archivos_base(lista_reportes, archivos_resumen=False, thread=None):
    for reporte in lista_reportes:
        generar_archivos_extra(reporte, regenerar=True, thread=thread, solo_crear_arc=True, v_archivos_resumen=archivos_resumen)

def generar_archivos_extra(seleccionar_reporte, regenerar=False, thread=None, evitar_extra=[], ext="_resumen.csv", solo_crear_arc=False, v_archivos_resumen=True):
    if regenerar:
        tipo = ".csv"
        proceso, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte,evitar_extra, thread=thread)
        if proceso:
            estandarizacion_archivos(lista_archivos,True, thread=thread)
            if v_archivos_resumen:
                tipo = "_form_estandar.csv"
                proceso, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte,evitar_extra, thread=thread)
                if proceso:
                    archivos_resumen(lista_archivos,True, thread=thread)
                    tipo = "_resumen.csv"
                    proceso, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte,evitar_extra, thread=thread)
                    comprimir_archivos_aux(seleccionar_reporte, evitar_extra, thread=thread)
    if not solo_crear_arc:
        tipo = ext
        proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, thread=thread)
        if proceso_resumen:
            proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
            dic_archivos_reporte = mod_4.agrupar_dic_archivos(dic_archivos)
            return True, dic_archivos_reporte
        return False, False
    else:
        return None, None

def generar_archivos_extra_anual(seleccionar_reporte, tipo=".csv", evitar_extra=[], continuar=False, informar=True, mostrar_dic=True, todos=False, thread=None, reportes_app=False):
    list_of_tuples = list(seleccionar_reporte.items())
    if len(seleccionar_reporte["filial"]) == 4:
        list_of_tuples.insert(3, ('carpeta', ["REPORTES_GENERADOS_APLICATIVO"]))
        seleccionar_reporte_1 = dict(list_of_tuples)
        del seleccionar_reporte_1["clasificacion"]
        del seleccionar_reporte_1["filial"]
    else:
        seleccionar_reporte_1 = seleccionar_reporte.copy()
    proceso, lista_archivos = busqueda_archivos_tipo_reporte_anual(tipo, seleccionar_reporte_1, evitar_extra, informar=informar, todos=todos, thread=thread)
    if proceso:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos_anual(seleccionar_reporte, lista_archivos, reportes_app=reportes_app)
        if proceso_agrupar:
            if reportes_app:
                return True, dic_archivos_mostrar
            else:
                return True, dic_archivos
        else:
            return False, False
    return False, False

def mostrar_info_reporte(reporte, thread):
    if reporte["fecha_personalizada"]:
        pass
    else:
        anios = lista_a_texto(reporte["anios"], ", ")
        meses = lista_a_texto(reporte["meses"], ", ")
        filial = lista_a_texto(reporte["filial"], ", ")
        tipo = lista_a_texto(reporte["tipo"], ", ")
        clasificacion = lista_a_texto(reporte["clasificacion"], ", ")
        texto = f"Año: {anios}, Mes: {meses}, Filial: {filial}, Tipo: {tipo}, Clasificación: {clasificacion}"
        if thread:
            thread.message_sent.emit(texto, "white")

def reportes_add_men_DB(dic_info, thread=None, regenerar_mensual=False, regenerar_anual=False):
    if regenerar_mensual:
        proceso, dic_archivos = generar_archivos_extra(dic_info["Reporte_add"]["mensual"], regenerar=True, thread=thread, evitar_extra=[], ext="_resumen.csv", solo_crear_arc=False)
        if proceso:
            generar_archivos_mensuales_dashboard(dic_info["Reporte_add"]["mensual"], evitar_extra=[], ext="_resumen.csv", thread=thread)
    elif regenerar_anual:
        proceso, dic_archivos = generar_archivos_extra(dic_info["Reporte_add"]["anual"], regenerar=True, thread=thread, evitar_extra=[], ext="_resumen.csv", solo_crear_arc=False)
        if proceso:
            generar_archivos_extra_dashboard(dic_info["Reporte_add"]["anual"], evitar_extra=[], ext="_resumen.csv", thread=thread)
    lista_dic = generar_archivos_anuales_dashboard(dic_info["Reporte"], thread=thread)
    return lista_dic

def cambio_diccionario_reportes(diccionario):
    nuevo_dic = {}
    for fecha, dic in diccionario.items():
        if fecha not in nuevo_dic:
            nuevo_dic[fecha] = []
            for llave, valor in dic.items():
                for elemento in valor:
                    nuevo_dic[fecha].append(elemento)
    return nuevo_dic

def generar_archivos_mensuales_dashboard(seleccionar_reporte, evitar_extra=[], ext="_resumen.csv", thread=None):
    tipo = ext
    lista_agrupar_archivos = []
    lista_agrupar_archivos_mostrar = []
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC1","GRC2","GRTT2"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Sector de consumo"])
            lista_agrupar_archivos_mostrar.append({"Sector de consumo":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC1","GRC2","GRTT2"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Sector de consumo subsidio"])
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC3"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Compensaciones"])
            lista_agrupar_archivos_mostrar.append({"Compensaciones":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["DS"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Desviaciones Significativas"])
            lista_agrupar_archivos_mostrar.append({"Desviaciones Significativas":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tarifario"]
    seleccionar_reporte["clasificacion"] = ["GRT1"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Tarifas"])
            lista_agrupar_archivos_mostrar.append({"Tarifas":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRS1"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Suspensiones"])
            lista_agrupar_archivos_mostrar.append({"Suspensiones":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRCS1"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Índices de Respuesta Servicio Ténico"])
            lista_agrupar_archivos_mostrar.append({"Índices de Respuesta Servicio Ténico":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRCS2"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Indicadores tecnicos"])
            lista_agrupar_archivos_mostrar.append({"Indicadores técnicos":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    nuevo_dic_mostrar = {}
    if len(lista_agrupar_archivos_mostrar):
        for elemento in lista_agrupar_archivos_mostrar:
            for llave, dic in elemento.items():
                for fecha, dic_filial in dic.items():
                    if fecha not in nuevo_dic_mostrar:
                        nuevo_dic_mostrar[fecha] = {}
                    nuevo_dic_mostrar[fecha][llave] = dic_filial
        for i in range(len(lista_agrupar_archivos)):
            elemento = lista_agrupar_archivos[i][0]
            seleccionar_reporte = lista_agrupar_archivos[i][1]
            nombre = lista_agrupar_archivos[i][2]
            if len(elemento):
                if thread:
                    thread.message_sent.emit(f"Inicio de procesamiento para: {nombre}\n\n", "green")
                else:
                    print(f"\nInicio de procesamiento para: {nombre}\n\n")
                if i == 0:
                    reporte_comercial_sector_consumo(cambio_diccionario_reportes(elemento), seleccionar_reporte, total=True, valor_facturado=True, thread=thread)
                elif i == 1:
                    reporte_comercial_sector_consumo(cambio_diccionario_reportes(elemento), seleccionar_reporte, total=True, valor_facturado=True, subsidio=True, thread=thread)
                elif i == 2:
                    generar_reporte_compensacion_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 3:
                    generar_reporte_desviaciones_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 4:
                    reporte_tarifas_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 5:
                    generar_reporte_suspension_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 6:
                    generar_reporte_indicadores_tecnicos_IRST_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 7:
                    generar_reporte_indicadores_tecnicos_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)

def generar_archivos_extra_dashboard(seleccionar_reporte, evitar_extra=[], ext="_resumen.csv", thread=None):
    tipo = ext
    lista_agrupar_archivos = []
    lista_agrupar_archivos_mostrar = []
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC1","GRC2","GRTT2"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Sector de consumo"])
            lista_agrupar_archivos_mostrar.append({"Sector de consumo":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC1","GRC2","GRTT2"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Sector de consumo subsidio"])
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC3"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Compensaciones"])
            lista_agrupar_archivos_mostrar.append({"Compensaciones":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["DS"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Desviaciones Significativas"])
            lista_agrupar_archivos_mostrar.append({"Desviaciones Significativas":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tarifario"]
    seleccionar_reporte["clasificacion"] = ["GRT1"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Tarifas"])
            lista_agrupar_archivos_mostrar.append({"Tarifas":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRS1"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Suspensiones"])
            lista_agrupar_archivos_mostrar.append({"Suspensiones":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRCS1"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Índices de Respuesta Servicio Ténico"])
            lista_agrupar_archivos_mostrar.append({"Índices de Respuesta Servicio Ténico":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRCS2"]
    proceso_resumen, lista_archivos = busqueda_archivos_tipo_reporte(tipo, seleccionar_reporte, evitar_extra, informar=False, thread=thread)
    if proceso_resumen:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
        if proceso_agrupar:
            lista_agrupar_archivos.append([dic_archivos,seleccionar_reporte,"Indicadores tecnicos"])
            lista_agrupar_archivos_mostrar.append({"Indicadores técnicos":dic_archivos_mostrar})
        else:
            lista_agrupar_archivos.append([{},None])
    nuevo_dic_mostrar = {}
    if len(lista_agrupar_archivos_mostrar):
        for elemento in lista_agrupar_archivos_mostrar:
            for llave, dic in elemento.items():
                for fecha, dic_filial in dic.items():
                    if fecha not in nuevo_dic_mostrar:
                        nuevo_dic_mostrar[fecha] = {}
                    nuevo_dic_mostrar[fecha][llave] = dic_filial
        for i in range(len(lista_agrupar_archivos)):
            elemento = lista_agrupar_archivos[i][0]
            seleccionar_reporte = lista_agrupar_archivos[i][1]
            nombre = lista_agrupar_archivos[i][2]
            if len(elemento):
                if thread:
                    thread.message_sent.emit(f"Inicio de procesamiento para: {nombre}\n\n", "green")
                else:
                    print(f"\nInicio de procesamiento para: {nombre}\n\n")
                if i == 0:
                    reporte_comercial_sector_consumo(cambio_diccionario_reportes(elemento), seleccionar_reporte, total=True, valor_facturado=True, thread=thread)
                elif i == 1:
                    reporte_comercial_sector_consumo(cambio_diccionario_reportes(elemento), seleccionar_reporte, total=True, valor_facturado=True, subsidio=True, thread=thread)
                elif i == 2:
                    generar_reporte_compensacion_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 3:
                    generar_reporte_desviaciones_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 4:
                    reporte_tarifas_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 5:
                    generar_reporte_suspension_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 6:
                    generar_reporte_indicadores_tecnicos_IRST_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)
                elif i == 7:
                    generar_reporte_indicadores_tecnicos_mensual(cambio_diccionario_reportes(elemento), seleccionar_reporte, thread=thread)

def fecha_anterior_rango(anio, mes):
    ubi_mes = lista_meses.index(mes)
    anio = int(anio)
    if ubi_mes == 0:
        return (str(anio-1), lista_meses[-1])
    else:
        anio = str(anio)
        mes = lista_meses[ubi_mes-1]
        return (anio,  mes)

def mostrar_dic_archivos_agrupados_dashboard(nuevo_dic_mostrar, thread=None):
    if thread:
        thread.message_sent.emit("Archivos disponibles para la selección realizada:", "green")
        for i,j in nuevo_dic_mostrar.items():
            thread.message_sent.emit(i, "orange")
            for a,b in j.items():
                thread.message_sent.emit("\t" + a, "white")
                thread.message_sent.emit("\t"*3 + b, "white")
                time.sleep(0.01)
    else:
        print("\nArchivos disponibles para la selección realizada: \n")
        for i,j in nuevo_dic_mostrar.items():
            print(i)
            for a,b in j.items():
                print(a,"\t"*3, b)

def generar_archivos_anuales_dashboard(seleccionar_reporte_dashboard, thread=None):
    lista_anual = []
    dic_anual = {}
    lista_dic = []
    v_max = 0
    seleccionar_reporte = seleccionar_reporte_dashboard.copy()
    seleccionar_reporte_consumo = seleccionar_reporte.copy()
    fi = seleccionar_reporte_consumo["fecha_personalizada"][0]
    ff = seleccionar_reporte_consumo["fecha_personalizada"][1]
    fi = fecha_anterior_rango(fi[0], fi[1])
    seleccionar_reporte_consumo["fecha_personalizada"] = [fi,ff]
    seleccionar_reporte_consumo["tipo"] = ["Comercial"]
    seleccionar_reporte_consumo["clasificacion"] = ["GRC1","GRC2","GRTT2"]
    reporte = "_reporte_consumo.csv"
    categoria = "Reporte de sector de consumo"
    reporte = reporte.replace(".csv", "_sumatoria.csv")
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte_consumo, reporte, ["_reporte_consumo", reporte.replace(".csv","")], continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual, categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC1","GRC2","GRTT2"]
    reporte = "_reporte_consumo_subsidio.csv"
    categoria = "Reporte de sector de consumo subsidiado"
    reporte = reporte.replace(".csv", "_sumatoria.csv")
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte, ["_reporte_consumo", reporte.replace(".csv",""), "_subsidio"], continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["GRC3"]
    reporte = "_compilado_compensacion.csv"
    categoria = "Reporte de compensaciones"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte, continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    seleccionar_reporte["tipo"] = ["Comercial"]
    seleccionar_reporte["clasificacion"] = ["DS57"]
    reporte = "_compilado_DS_metricas_categorias.csv"
    categoria = "Reporte de desviaciones significativas"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte, evitar_extra=["_compilado_desviaciones","_compilado_DS_metricas"], continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    seleccionar_reporte["tipo"] = ["Tarifario"]
    seleccionar_reporte["clasificacion"] = ["GRT1"]
    reporte = "_reporte_tarifario.csv"
    categoria = "Reporte de tarifas"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte, continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRS1"]
    reporte = "_reporte_suspension.csv"
    categoria = "Reporte de suspensiones"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte, continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRCS1"]
    reporte_1 = "_indicador_tecnico_IRST.csv"
    reporte_2 = "_indicador_tecnico_IRST_minutos.csv"
    reporte_3 = "_indicador_tecnico_IRST_horas.csv"
    categoria = "Reporte de IRST"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte_1, evitar_extra=["_indicador_tecnico_IRST", "_indicador_tecnico"], continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    categoria = "Reporte de IRST (minutos)"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte_2, evitar_extra=["_indicador_tecnico_IRST_minutos","_indicador_tecnico","_indicador_tecnico_IRST"], continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    categoria = "Reporte de IRST (horas)"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte_3, evitar_extra=["_indicador_tecnico_IRST_horas","_indicador_tecnico","_indicador_tecnico_IRST"], continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    seleccionar_reporte["tipo"] = ["Tecnico"]
    seleccionar_reporte["clasificacion"] = ["GRCS2"]
    reporte = "_indicador_tecnico.csv"
    categoria = "Reporte de indicadores técnicos"
    proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte, continuar=True, mostrar_dic=False)
    if proceso:
        lista_dic.append((dic_archivos_anual,categoria))
        if len(categoria) > v_max:
            v_max = len(categoria)
    else:
        lista_dic.append(({},None))
    v_max += 5
    nuevo_dic_mostrar = {}
    if len(lista_dic):
        for elemento in lista_dic:
            dic = elemento[0]
            if len(dic):
                categoria = elemento[1]
                for fecha, lista_fecha in dic.items():
                    if len(lista_fecha):
                        if fecha not in nuevo_dic_mostrar:
                            nuevo_dic_mostrar[fecha] = {}
                        if categoria not in nuevo_dic_mostrar[fecha]:
                            nuevo_dic_mostrar[fecha][categoria] = None
                        nuevo_dic_mostrar[fecha][categoria] = lista_fecha[0].split("\\")[-1]
        mostrar_dic_archivos_agrupados_dashboard(nuevo_dic_mostrar, thread=thread)
        return lista_dic
    else:
        return {}

def archivos_dashboard(lista_dic, reporte, thread=None):
    lista_anual = []
    for pos in range(len(lista_dic)):
        elemento = lista_dic[pos]
        dic_archivos_anual = elemento[0]
        categoria = elemento[1]
        if categoria:
            if pos == 0:
                archivo = union_archivos_mensuales_anual_reporte_consumo(dic_archivos_anual, reporte, True, subsidio=False, thread=thread)
            elif pos == 1:
                archivo = union_archivos_mensuales_anual_reporte_consumo(dic_archivos_anual, reporte, True, thread=thread)
            else:
                archivo = union_archivos_mensuales_anual(dic_archivos_anual, reporte, True, thread=thread)
            lista_anual.append(archivo)
        else:
            lista_anual.append(None)
    return lista_anual

def eleccion_rango_trimestral(fecha=[]):
    listas_unidas = unir_listas_anio_tri(lista_anios, lista_trimestres)
    if len(fecha):
        mes_i = fecha[0][1]
        anio_i = int(fecha[0][0])
        mes_f = fecha[1][1]
        anio_f = fecha[1][0]
        pos_mes = lista_meses.index(mes_i)
        tri_i = trimestre_mes[fecha[0][1]]
        tri_f = trimestre_mes[fecha[1][1]]
        if pos_mes <= 3:
            anio_i -=1
        anio_i = str(anio_i)
        fi = (anio_i,tri_i)
        ff = (anio_f,tri_f)
        return fi,ff,listas_unidas

def generar_grafias_DB(lista_anual, reporte, thread=None):
    fi_1 = reporte["fecha_personalizada"][0][0]
    fi_2 = reporte["fecha_personalizada"][0][1]
    ff_1 = reporte["fecha_personalizada"][1][0]
    ff_2 = reporte["fecha_personalizada"][1][1]
    texto_fecha = f"{fi_1}_{fi_2.upper()}_{ff_1}_{ff_2.upper()}"
    fecha = ((fi_1, fi_2),(ff_1, ff_2))
    texto_fecha_completo = f"{fi_2}/{fi_1} - {ff_2}/{ff_1}"
    v_fecha_anterior = fecha_anterior(ff_1, ff_2)
    v_fecha_inicial = fecha_anterior(fi_1, fi_2)
    periodo = f"{fi_1}/{fi_2} - {ff_1}/{ff_2}"
    periodo = f"{fi_2[:3]}/{fi_1} - {ff_2[:3]}/{ff_1}"
    if len(lista_anual):
        dic_metricas = {}
        for i in range(len(lista_anual)):
            archivo = lista_anual[i]
            if archivo:
                if i == 0:
                    thread.message_sent.emit("Gráficas sectores de consumo", "orange")
                    mod_6.grafica_pie_tipo_usuario(archivo, v_fecha_anterior, thread=thread)
                    dic_metricas = mod_6.grafico_barras_consumo(archivo, dic_metricas, thread=thread)
                    mod_6.grafico_usuarios(archivo, thread=thread)
                    dic_metricas = mod_6.grafica_pie_usuarios(archivo, v_fecha_anterior, dic_metricas, thread=thread)
                    dic_metricas = mod_6.grafica_tabla_sector_consumo(archivo, v_fecha_anterior, dic_metricas, thread=thread)
                    dic_metricas = mod_6.metricas_sector_consumo(archivo, v_fecha_inicial, v_fecha_anterior, dic_metricas, thread=thread)
                elif i == 1:
                    thread.message_sent.emit("Gráficas sectores de consumo subsidiados", "orange")
                    mod_6.grafica_pie_subsidios(archivo, v_fecha_anterior, thread=thread)
                    dic_metricas = mod_6.grafica_barras_subsidios(archivo, dic_metricas, thread=thread)
                elif i == 2:
                    thread.message_sent.emit("Gráficas compensaciones", "orange")
                    mod_6.grafica_compensacion(archivo, thread=thread)
                    dic_metricas = mod_6.metricas_compensacines(archivo, v_fecha_anterior, dic_metricas)
                elif i == 3:
                    thread.message_sent.emit("Gráficas desviaciones significativas", "orange")
                    dic_metricas = mod_6.grafica_DS(archivo, dic_metricas, thread=thread)
                elif i == 4:
                    thread.message_sent.emit(f"Gráficas tarifas {grupo_vanti}", "orange")
                    dic_metricas = mod_6.fun_tarifas(archivo, v_fecha_anterior, dic_metricas, thread=thread)
                elif i == 5:
                    #thread.message_sent.emit("Gráficas suspensiones", "orange")
                    dic_metricas = mod_6.metricas_suspensiones(archivo, v_fecha_anterior, dic_metricas)
                elif i == 6:
                    dic_metricas = mod_6.metricas_indicadores(archivo, v_fecha_anterior, dic_metricas)
                elif i == 7:
                    thread.message_sent.emit("Gráficas indicador IRST-EG", "orange")
                    mod_6.grafica_barras_indicador_tecnico_minutos(archivo, thread=thread)
                elif i == 8:
                    mod_6.grafica_barras_indicador_tecnico_horas(archivo, fecha, thread=thread)
                elif i == 9:
                    thread.message_sent.emit("Gráficas indicadores técnicos (IPLI, IO, IRST-EG)", "orange")
                    dic_metricas = mod_6.grafica_barras_indicador_tecnico(archivo, dic_metricas, thread=thread)
        thread.message_sent.emit("Gráficas reclamos por facturación", "orange")
        fi,ff,listas_unidas = eleccion_rango_trimestral([(fi_1, fi_2),(ff_1, ff_2)])
        archivo = reporte_info_reclamos(fi,ff,listas_unidas, dashboard=True, texto_fecha=texto_fecha, thread=thread)
        if archivo:
            mod_6.grafica_barras_trimestre_reclamos(archivo, thread=thread)
        thread.message_sent.emit("Gráficas gastos AOM", "orange")
        archivo = gastos_AOM(dashboard=True, texto_fecha=texto_fecha, thread=thread)
        if archivo:
            mod_6.grafica_gastos_AOM(archivo, anio_actual-1, thread=thread)
        thread.message_sent.emit("Gráficas porcentaje cumplimientos regulatorios", "orange")
        archivo = generar_porcentaje_cumplimientos_regulatorios(dashboard=True, texto_fecha=texto_fecha, thread=thread)
        if archivo:
            mod_6.velocimetro_cumplimientos_regulatorios(archivo, v_fecha_anterior, thread=thread)
        thread.message_sent.emit("Gráficas pagos de contribuciones MME", "orange")
        archivo, archivo_1 = contribuciones_MME(dashboard=True, texto_fecha=texto_fecha, thread=thread)
        if archivo and archivo_1:
            dic_metricas = mod_6.grafica_deuda_subsidios(archivo, archivo_1, dic_metricas, thread=thread)
        dic_tarifas = tarifas_distribuidoras_GN(thread=thread)
        if dic_tarifas:
            dic_metricas["Tarifas_nacionales"] = dic_tarifas
        dic_distribuidoras = cumplimientos_SUI_distribuidoras(thread=thread)
        if dic_distribuidoras:
            dic_metricas["Cumplimientos_SUI"] = dic_distribuidoras
        thread.message_sent.emit("Gráficas matriz de requerimientos", "orange")
        archivo = generar_porcentaje_matriz_requerimientos(dashboard=True, texto_fecha=texto_fecha, thread=thread)
        if archivo:
            mod_6.grafica_matriz_requerimientos(archivo, thread=thread)
        fecha_corte = f"{fecha_corte_tupla[0]} de {lista_meses[int(fecha_corte_tupla[1])-1]} del {fecha_corte_tupla[2]}"
        fecha_corte_anterior = f"{fecha_anio_anterior_tupla[0]} de {lista_meses[int(fecha_anio_anterior_tupla[1])-1]} del {fecha_anio_anterior_tupla[2]}"
        mes_corte = f"{lista_meses[int(fecha_corte_tupla[1])-1]}-{fecha_corte_tupla[2]}"
        t = " "*17+"\t"*6
        thread.message_sent.emit(f"{t} Inicio generación slides", "orange")
        time.sleep(0.1)
        mod_7.crear_slides(lista_a_texto(archivo.split("\\")[:-2],"\\"),v_fecha_anterior,texto_fecha_completo,
                        fecha_corte, texto_fecha, dic_metricas, mes_corte, fecha_corte_anterior,periodo,
                        thread=thread)
    return dic_metricas

def generar_archivos_reporte(reporte, info, thread):
    lista_generar = []
    opciones = {}
    match reporte:
        #Reportes comerciales
        case "reporte_comercial_sector_consumo_mensual":
            nombre = "Reporte comercial mensual por sector de consumo"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_comercial_sector_consumo_anual":
            nombre = "Reporte comercial mensual por sector de consumo anual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_comercial_sector_consumo_subsidio_mensual":
            nombre = "Reporte comercial mensual por sector de consumo con subsidiados o contribuciones"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_comercial_sector_consumo_subsidio_anual":
            nombre = "Reporte comercial mensual por sector de consumo con subsidiados o contribuciones anual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_compensaciones_mensual":
            nombre = "Reporte compensaciones mensual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_compensaciones_anual":
            nombre = "Reporte compensaciones anual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "generar_reporte_compensaciones_anual":
            nombre = "Reporte compensaciones anual"
            thread.message_sent.emit(f" ", "white")
            thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
        case "desviaciones_significativas_mensual":
            nombre = "Reporte desviaciones significativas mensual"
            regenerar = False
            opciones = info["Opciones"]
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "desviaciones_significativas_anual":
            nombre = "Reporte desviaciones significativas anual"
            regenerar = False
            opciones = info["Opciones"]
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_DANE_mensual":
            nombre = "Reporte DANE mensual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_SH":
            nombre = "Reporte Secretaria de Hacienda de Bogotá D.C."
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "comparacion_CER_CLD_PRD":
            nombre = "Comparación CER-CLD-PRD"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread, evitar_extra=["_CLD","_PRD"])
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "comparacion_CER_CLD":
            nombre = "Comparación CER-CLD"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread, evitar_extra=["_CLD"])
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "comparacion_CER_PRD":
            nombre = "Comparación CER-PRD"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread, evitar_extra=["_PRD"])
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "comparacion_CLD_PRD":
            nombre = "Comparación CLD-PRD"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread, evitar_extra=["_CLD","_PRD"])
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "comprobar_info_GRTT2":
            nombre = "Comprobar de calidad de la información para el reporte GRTT2"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(agregar_meses_anteriores(i), regenerar, thread, evitar_extra=["SAP"])
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "corregir_errores_GRTT2":
            nombre = "Corregir errores en la información para el reporte GRTT2"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(agregar_meses_anteriores(i), regenerar, thread, evitar_extra=["SAP"])
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "generar_info_GRTT2":
            nombre = "Generar información para el reporte GRTT2"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "generar_info_usuarios_R_NR":
            nombre = "Generar información adicional de usuarios regulados / no regulados"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        #Reportes tarifarios
        case "reportes_tarifarios_mensual":
            nombre = "Reporte tarifario mensual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reportes_tarifarios_anual":
            nombre = "Reporte tarifario anual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "generar_reportes_tarifarios_anual":
            nombre = "Reporte tarifario anual unión"
            thread.message_sent.emit(f" ", "white")
            thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
        #Reportes técnicos
        case "reporte_indicadores_mensual":
            nombre = "Reporte indicadores técnicos mensual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_indicadores_anual":
            nombre = "Reporte indicadores técnicos anual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "generar_reporte_indicadores_anual":
            nombre = "Reporte indicadores técnicos anual unión"
            thread.message_sent.emit(f" ", "white")
            thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
        case "reporte_suspensiones_mensual":
            nombre = "Reporte suspensiones mensual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_suspensiones_anual":
            nombre = "Reporte suspensiones anual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "generar_reporte_suspensiones_anual":
            nombre = "Reporte suspensiones anual unión"
            thread.message_sent.emit(f" ", "white")
            thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
        case "reporte_IRST_mensual":
            nombre = "Reporte IRST-EG mensual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread, evitar_extra=["_indicador_tecnico"])
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "reporte_IRST_anual":
            nombre = "Reporte IRST-EG anual"
            opciones = info["Opciones"]
            regenerar = False
            if "regenerar" in opciones:
                if opciones["regenerar"]:
                    regenerar = True
            for i in info["Reportes"]:
                mostrar_info_reporte(i, thread)
                proceso,dic_archivos_reporte = generar_archivos_extra(i, regenerar, thread)
                if proceso:
                    for llave, valor in dic_archivos_reporte.items():
                        lista_generar.append([llave, i, valor])
            if thread and len(lista_generar):
                thread.message_sent.emit(f" ", "white")
                thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
                for elemento in lista_generar:
                    thread.message_sent.emit(elemento[0], "white")
                    for elemento_1 in elemento[2]:
                        thread.message_sent.emit(acortar_nombre(elemento_1), "white")
        case "generar_reporte_IRST_anual":
            nombre = "Reporte IRST-EG anual unión"
            thread.message_sent.emit(f" ", "white")
            thread.message_sent.emit(f"Archivos disponibles para: {nombre} ", "white")
        case _:
            pass
    return lista_generar, opciones

def generar_reporte(reporte, info, thread, opciones_add=None):
    info_reporte = None
    opciones_apoyo = None
    match reporte:
        #Reportes comerciales
        case "generar_reporte_comercial_sector_consumo_mensual":
            opciones = info["Opciones"]
            sumatoria = False
            if "sumatoria" in opciones:
                sumatoria = opciones["sumatoria"]
            valor_facturado = False
            if "valor_facturado" in opciones:
                valor_facturado = opciones["valor_facturado"]
            facturas = False
            if "facturas" in opciones:
                facturas = opciones["facturas"]
            codigo_DANE = None
            if "codigo_DANE" in opciones:
                codigo_DANE = opciones["codigo_DANE"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_comercial_sector_consumo(dic, valor[1], informar=True, codigo_DANE=codigo_DANE, total=sumatoria, valor_facturado=valor_facturado, facturas=facturas, thread=thread)
        case "generar_reporte_comercial_sector_consumo_anual":
            opciones = info["Opciones"]
            sumatoria = False
            if "sumatoria" in opciones:
                sumatoria = opciones["sumatoria"]
            valor_facturado = False
            if "valor_facturado" in opciones:
                valor_facturado = opciones["valor_facturado"]
            facturas = False
            if "facturas" in opciones:
                facturas = opciones["facturas"]
            codigo_DANE = None
            if "codigo_DANE" in opciones:
                codigo_DANE = opciones["codigo_DANE"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                opciones_apoyo = opciones
                reporte_comercial_sector_consumo(dic, valor[1], informar=True, codigo_DANE=codigo_DANE, total=sumatoria, valor_facturado=valor_facturado, facturas=facturas, thread=thread)
        case "generar_reporte_comercial_sector_consumo_anual_union":
            reporte = "_reporte_consumo.csv"
            if "sumatoria" in opciones_add:
                reporte = reporte.replace(".csv", "_sumatoria.csv")
            if "codigo_DANE" in opciones_add:
                v_codigo_DANE_texto = codigo_DANE_texto(opciones_add["codigo_DANE"])
                if len(v_codigo_DANE_texto):
                    v_codigo_DANE_texto = v_codigo_DANE_texto+".csv"
                    reporte = reporte.replace(".csv", "_"+v_codigo_DANE_texto)
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte, ["_reporte_consumo", reporte.replace(".csv","")])
            if proceso:
                v_fecha_anterior = fecha_siguiente(info["fecha_personalizada"][0][0], info["fecha_personalizada"][0][1])
                info["fecha_personalizada"][0] = v_fecha_anterior
                union_archivos_mensuales_anual_reporte_consumo(dic_archivos_anual, info, informar=True, thread=thread, subsidio=False)
        case "generar_reporte_comercial_sector_consumo_subsidio_mensual":
            opciones = info["Opciones"]
            sumatoria = False
            if "sumatoria" in opciones:
                sumatoria = opciones["sumatoria"]
            valor_facturado = False
            if "valor_facturado" in opciones:
                valor_facturado = opciones["valor_facturado"]
            facturas = False
            if "facturas" in opciones:
                facturas = opciones["facturas"]
            codigo_DANE = None
            if "codigo_DANE" in opciones:
                codigo_DANE = opciones["codigo_DANE"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_comercial_sector_consumo(dic, valor[1], informar=True, codigo_DANE=codigo_DANE, total=sumatoria, valor_facturado=valor_facturado, facturas=facturas, thread=thread, subsidio=True)
        case "generar_reporte_comercial_sector_consumo_subsidio_anual":
            opciones = info["Opciones"]
            sumatoria = False
            if "sumatoria" in opciones:
                sumatoria = opciones["sumatoria"]
            valor_facturado = False
            if "valor_facturado" in opciones:
                valor_facturado = opciones["valor_facturado"]
            facturas = False
            if "facturas" in opciones:
                facturas = opciones["facturas"]
            codigo_DANE = None
            if "codigo_DANE" in opciones:
                codigo_DANE = opciones["codigo_DANE"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                opciones_apoyo = opciones
                reporte_comercial_sector_consumo(dic, valor[1], informar=True, codigo_DANE=codigo_DANE, total=sumatoria, valor_facturado=valor_facturado, facturas=facturas, thread=thread, subsidio=True)
        case "generar_reporte_comercial_sector_consumo_subsidio_anual_union":
            reporte = "_reporte_consumo_subsidio.csv"
            if "sumatoria" in opciones_add:
                reporte = reporte.replace(".csv", "_sumatoria.csv")
            if "codigo_DANE" in opciones_add:
                v_codigo_DANE_texto = codigo_DANE_texto(opciones_add["codigo_DANE"])
                if len(v_codigo_DANE_texto):
                    v_codigo_DANE_texto = v_codigo_DANE_texto+".csv"
                    reporte = reporte.replace(".csv", "_"+v_codigo_DANE_texto)
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte, ["_reporte_consumo", reporte.replace(".csv",""), "_subsidio"])
            if proceso:
                union_archivos_mensuales_anual_reporte_consumo(dic_archivos_anual, info, informar=True, thread=thread, subsidio=True)
        case "generar_reporte_compensaciones_mensual":
            opciones = info["Opciones"]
            inventario = False
            if "inventario" in opciones:
                inventario = opciones["inventario"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                generar_reporte_compensacion_mensual(dic, valor[1], informar=True, inventario=inventario, thread=thread)
        case "generar_reporte_compensaciones_anual":
            opciones = info["Opciones"]
            inventario = False
            if "inventario" in opciones:
                inventario = opciones["inventario"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                generar_reporte_compensacion_mensual(dic, valor[1], informar=True, inventario=inventario, thread=thread)
        case "generar_reporte_compensaciones_anual_union":
            reporte = "_compilado_compensacion.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte)
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
        case "generar_desviaciones_significativas_mensual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                generar_reporte_desviaciones_mensual(dic, valor[1], thread=thread)
        case "generar_desviaciones_significativas_anual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                generar_reporte_desviaciones_mensual(dic, valor[1], thread=thread)
        case "generar_desviaciones_significativas_anual_union":
            reporte = "_compilado_DS_metricas.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte)
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
        case "generar_reporte_DANE_mensual":
            opciones = info["Opciones"]
            codigo_DANE = None
            if "codigo_DANE" in opciones:
                codigo_DANE = opciones["codigo_DANE"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_comercial_sector_consumo(dic, valor[1], informar=True, codigo_DANE=codigo_DANE, valor_facturado=True, reporte_DANE=True, thread=thread)
        case "generar_reporte_SH":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_SH(dic, valor[1], informar=True, codigo_DANE=[11001000], thread=thread)
        case "generar_comparacion_CER_CLD_PRD":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_comparacion_prd_cld_cer(dic, valor[1], informar=True, thread=thread)
        case "generar_comparacion_CER_CLD":
            opciones = info["Opciones"]
            cantidad_filas = cantidad_datos_estilo_excel
            if "cantidad_filas" in opciones:
                cantidad_filas = opciones["cantidad_filas"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_comparacion_SAP(dic, valor[1], True, cantidad_filas, "GRC1_", "_CLD", thread=thread)
        case "generar_comparacion_CER_PRD":
            opciones = info["Opciones"]
            cantidad_filas = cantidad_datos_estilo_excel
            if "cantidad_filas" in opciones:
                cantidad_filas = opciones["cantidad_filas"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_comparacion_SAP(dic, valor[1], True, cantidad_filas, "GRC1_", "_PRD", thread=thread)
        case "generar_comparacion_CLD_PRD":
            opciones = info["Opciones"]
            cantidad_filas = cantidad_datos_estilo_excel
            if "cantidad_filas" in opciones:
                cantidad_filas = opciones["cantidad_filas"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_comparacion_SAP(dic, valor[1], True, cantidad_filas, "_PRD", "_CLD", thread=thread)
        case "generar_comprobar_info_GRTT2":
            for i in range(0, len(info["Archivos"]), 2):
                valor_1 = info["Archivos"][i]
                valor_2 = info["Archivos"][i+1]
                dic = {valor_1[0]:valor_1[2],
                        valor_2[0]:valor_2[2]}
                encontrar_errores_inventario_suscriptores(dic, valor_1[1], thread=thread)
        case "generar_corregir_errores_GRTT2":
            for i in range(0, len(info["Archivos"]), 2):
                valor_1 = info["Archivos"][i]
                valor_2 = info["Archivos"][i+1]
                dic = {valor_1[0]:valor_1[2],
                        valor_2[0]:valor_2[2]}
                corregir_errores_inventario_suscriptores(dic, valor_1[1], thread=thread)
        case "generar_generar_info_GRTT2":
            opciones = info["Opciones"]
            usuarios_unicos = False
            if "usuarios_activos" in opciones:
                usuarios_unicos = opciones["usuarios_activos"]
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_usuarios_filial(dic, valor[1], True, usuarios_unicos=usuarios_unicos, thread=thread)
        case "generar_generar_info_usuarios_R_NR":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_usuarios_unicos_mensual(dic, valor[1], True, thread=thread)
        #Reportes tarifarios
        case "generar_reportes_tarifarios_mensual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                reporte_tarifas_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reportes_tarifarios_anual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                reporte_tarifas_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reportes_tarifarios_anual_union":
            reporte = "_reporte_tarifario.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte)
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
        #Reportes técnicos
        case "generar_reporte_indicadores_mensual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                generar_reporte_indicadores_tecnicos_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reporte_indicadores_anual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                generar_reporte_indicadores_tecnicos_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reporte_indicadores_anual_union":
            reporte = "_indicador_tecnico.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte)
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
        case "generar_reporte_suspensiones_mensual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                generar_reporte_suspension_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reporte_suspensiones_anual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                generar_reporte_suspension_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reporte_suspensiones_anual_union":
            reporte = "_reporte_suspension.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte)
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
        case "generar_reporte_IRST_mensual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                generar_reporte_indicadores_tecnicos_IRST_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reporte_IRST_anual":
            for valor in info["Archivos"]:
                dic = {valor[0]:valor[2]}
                info_reporte = valor[1]
                generar_reporte_indicadores_tecnicos_IRST_mensual(dic, valor[1], informar=True, thread=thread)
        case "generar_reporte_IRST_anual_union":
            reporte = "_indicador_tecnico_IRST.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte, evitar_extra=["_indicador_tecnico_IRST", "_indicador_tecnico"])
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
            reporte = "_indicador_tecnico_IRST_minutos.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte, evitar_extra=["_indicador_tecnico_IRST_minutos","_indicador_tecnico","_indicador_tecnico_IRST"])
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
            reporte = "_indicador_tecnico_IRST_horas.csv"
            proceso,dic_archivos_anual = generar_archivos_extra_anual(info, reporte, evitar_extra=["_indicador_tecnico_IRST_minutos","_indicador_tecnico","_indicador_tecnico_IRST"])
            if proceso:
                union_archivos_mensuales_anual(dic_archivos_anual, info, informar=True, thread=thread)
        case _:
            pass
    return info_reporte, opciones_apoyo

class Envio_mensajes(QThread):
    message_sent = pyqtSignal(str, str)
    finished = pyqtSignal(bool, dict)
    def __init__(self, estado, info):
        super().__init__()
        self.ruta_guardar_archivos = ruta_guardar_archivos
        self.estado = estado
        self.info = info
    def run(self):
        try:
            dashboard = False
            dic_info = {}
            valor = False
            self.message_sent.emit("Inicio de procesamiento de archivos\n", "green")
            t_i = time.time()
            match self.estado:
                #Edición de archivos
                case "almacenar_archivos":
                    almacenar_archivos_2(self.ruta_guardar_archivos, self)
                case "crear_carpetas":
                    mod_3.configuracion_inicial()
                    self.message_sent.emit("\nConfiguración inicial completa\n", "green")
                    self.message_sent.emit("\nSe recomienda recargar el aplicativo para almacenar los cambios\n", "yellow")
                case "agregar_anio":
                    anio = str(anio_actual)
                    mod_2.cambiar_diccionario(str(anio))
                    mod_3.configuracion_inicial()
                    self.message_sent.emit(f"\nAño {anio_actual} ingresado correctamente\n", "green")
                    self.message_sent.emit("\nConfiguración inicial completa\n", "green")
                    self.message_sent.emit("\nSe recomienda recargar el aplicativo para almacenar los cambios\n", "yellow")
                case "editar_reporte":
                    if self.info:
                        reporte = obtener_reporte(self.info)
                        if reporte:
                            op, info = editar_json_reporte(reporte+"_json")
                            if op == "no_complete":
                                self.message_sent.emit("\nEl archivo .xlsx no posee las hojas necesarias\n", "red")
                                self.message_sent.emit(f"\nLas hojas aceptadas son: {lista_a_texto(info, ', ')}\n", "red")
                            elif op == "no_exist":
                                self.message_sent.emit(f"\nNo existe el archivo {info}\n", "red")
                            else:
                                self.message_sent.emit(f"\n{info}\n", "green")
                case "agregar_reporte":
                    if self.info:
                        reporte = self.info["Nuevo_reporte"]
                        categoria = obtener_categoria(self.info)
                        if categoria:
                            op, info = agregar_json_reporte(categoria, reporte+"_json")
                            if op == "no_complete":
                                self.message_sent.emit("\nEl archivo .xlsx no posee las hojas necesarias\n", "red")
                                self.message_sent.emit(f"\nLas hojas aceptadas son: {lista_a_texto(info, ', ')}\n", "red")
                            elif op == "no_exist":
                                self.message_sent.emit(f"\nNo existe el archivo {info}\n", "red")
                            else:
                                self.message_sent.emit(f"\n{info}\n", "green")
                case "convertir_archivos":
                    if self.info:
                        eliminar = False
                        if "Opciones" in self.info:
                            if "conservar_archivos" in self.info["Opciones"]:
                                if not self.info["Opciones"]["conservar_archivos"]:
                                    eliminar = True
                        conversion_archivos_txt(self.info["Reportes"], eliminar, self)
                case "archivos_estandar":
                    generar_archivos_base(self.info["Reportes"], archivos_resumen=False, thread=self)
                case "archivos_resumen":
                    generar_archivos_base(self.info["Reportes"], archivos_resumen=True, thread=self)
                case "archivos_existentes":
                    reportes_disponibles_Nuevo_SUI(self.info["Reportes"], thread=self)
                case "reportes_existentes":
                    reportes_disponibles_app(self.info["Reporte_anual"], thread=self)
                #Reportes comerciales
                case "reporte_comercial_sector_consumo_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_comercial_sector_consumo_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reporte_comercial_sector_consumo_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_comercial_sector_consumo_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            dic_info["Opciones"] = opciones_apoyo
                            valor = True
                case "generar_reporte_comercial_sector_consumo_anual_union":
                    if self.info and self.info["Reporte"]:
                        generar_reporte(self.estado, self.info["Reporte"], self, self.info["Opciones"])
                case "reporte_comercial_sector_consumo_subsidio_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_comercial_sector_consumo_subsidio_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reporte_comercial_sector_consumo_subsidio_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_comercial_sector_consumo_subsidio_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            dic_info["Opciones"] = opciones_apoyo
                            valor = True
                case "generar_reporte_comercial_sector_consumo_subsidio_anual_union":
                    if self.info and self.info["Reporte"]:
                        generar_reporte(self.estado, self.info["Reporte"], self, self.info["Opciones"])
                case "reporte_compensaciones_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_compensaciones_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reporte_compensaciones_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_compensaciones_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            valor = True
                case "generar_reporte_compensaciones_anual_union":
                    generar_reporte(self.estado, self.info["Reporte"], self)
                case "desviaciones_significativas_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                case "generar_desviaciones_significativas_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "desviaciones_significativas_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                case "generar_desviaciones_significativas_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            valor = True
                case "generar_desviaciones_significativas_anual_union":
                    if self.info and self.info["Reporte"]:
                        generar_reporte(self.estado, self.info["Reporte"], self)
                case "reporte_DANE_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_DANE_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reporte_SH":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_SH":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "comparacion_CER_CLD_PRD":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_comparacion_CER_CLD_PRD":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "comparacion_CER_CLD":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_comparacion_CER_CLD":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "comparacion_CER_PRD":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_comparacion_CER_PRD":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "comparacion_CLD_PRD":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_comparacion_CLD_PRD":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "comprobar_info_GRTT2":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_comprobar_info_GRTT2":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "corregir_errores_GRTT2":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_corregir_errores_GRTT2":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "generar_info_GRTT2":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_generar_info_GRTT2":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "generar_info_usuarios_R_NR":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_generar_info_usuarios_R_NR":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                #Reportes tarifarios
                case "reportes_tarifarios_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reportes_tarifarios_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reportes_tarifarios_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reportes_tarifarios_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            valor = True
                case "generar_reportes_tarifarios_anual_union":
                    if self.info and self.info["Reporte"]:
                        generar_reporte(self.estado, self.info["Reporte"], self)
                #Reportes técnicos
                case "reporte_indicadores_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_indicadores_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reporte_indicadores_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_indicadores_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            valor = True
                case "generar_reporte_indicadores_anual_union":
                    if self.info and self.info["Reporte"]:
                        generar_reporte(self.estado, self.info["Reporte"], self)
                case "reporte_suspensiones_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_suspensiones_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reporte_suspensiones_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_suspensiones_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            valor = True
                case "generar_reporte_suspensiones_anual_union":
                    if self.info and self.info["Reporte"]:
                        generar_reporte(self.estado, self.info["Reporte"], self)
                case "reporte_IRST_mensual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_IRST_mensual":
                    if self.info:
                        generar_reporte(self.estado, self.info, self)
                case "reporte_IRST_anual":
                    if self.info:
                        lista_generar, opciones = generar_archivos_reporte(self.estado, self.info, self)
                        if len(lista_generar):
                            valor = True
                            dic_info["Archivos"] = lista_generar
                            dic_info["Opciones"] = opciones
                case "generar_reporte_IRST_anual":
                    if self.info:
                        info_reporte, opciones_apoyo = generar_reporte(self.estado, self.info, self)
                        if info_reporte:
                            dic_info["Reporte"] = info_reporte
                            valor = True
                case "generar_reporte_IRST_anual_union":
                    if self.info and self.info["Reporte"]:
                        generar_reporte(self.estado, self.info["Reporte"], self)
                #KPIs
                case "cumplimientos_regulatorios":
                    generar_porcentaje_cumplimientos_regulatorios(thread=self)
                case "matriz_requerimientos":
                    generar_porcentaje_matriz_requerimientos(thread=self)
                case "gastos_AOM":
                    gastos_AOM(thread=self)
                case "contribuciones_MME":
                    contribuciones_MME(thread=self)
                case "reclamos_facturas":
                    if self.info:
                        reporte_info_reclamos(self.info["fi"], self.info["ff"], self.info["listas_unidas"], thread=self)
                case "dashboard":
                    if self.info:
                        regenerar_mensual = False
                        regenerar_anual = False
                        if self.info["Opciones"]["regenerar_mensual"][0]:
                            regenerar_mensual = True
                        if self.info["Opciones"]["regenerar_anual"][0]:
                            regenerar_anual = True
                        lista_dic = reportes_add_men_DB(self.info, thread=self, regenerar_mensual=regenerar_mensual, regenerar_anual=regenerar_anual)
                        dic_info["archivos"] = lista_dic
                        dic_info["Reporte"] = self.info["Reporte"]
                        valor = True
                case "generar_dashboard":
                    v_fecha_anterior = fecha_siguiente(self.info["Reporte"]["fecha_personalizada"][0][0], self.info["Reporte"]["fecha_personalizada"][0][1])
                    self.info["Reporte"]["fecha_personalizada"][0] = (v_fecha_anterior[0], v_fecha_anterior[1])
                    t = " "*17+"\t"*4
                    self.message_sent.emit(f"{t} Inicio generación compilado anual de reportes regulatorios", "orange")
                    lista_anual = archivos_dashboard(self.info["archivos"], self.info["Reporte"], thread=self)
                    dashboard = True
                    t = " "*17+"\t"*6
                    self.message_sent.emit(f"{t} Inicio generación gráficas", "orange")
                    generar_grafias_DB(lista_anual, self.info["Reporte"], thread=self)
                case _:
                    print("Estado no activo")
            self.message_sent.emit("\nFin de procesamiento de archivos\n", "green")
            t_f = time.time()
            tiempo = mostrar_tiempo(t_f, t_i)
            self.message_sent.emit(f"{tiempo}\n", "white")
            if valor:
                if dashboard:
                    t = " "*10+"\t"*3
                    self.message_sent.emit(f"{t} ¿Desea continuar con la creación del DB con los archivos disponibles?", "white")
                else:
                    t = " "*17+"\t"*6
                    self.message_sent.emit(f"{t} ¿Desea continuar con el procesamiento?", "white")
            self.finished.emit(valor, dic_info)
        except BaseException as e:
            self.message_sent.emit(f"\nError en el proceso: {e}\n", "red")
            self.finished.emit(False, {})

class Crear_ventana_texto(QDialog):
    def __init__(self,texto, estado, info, parent=None):
        super().__init__(parent)
        self.result = None
        self.dic_info = {}
        self.initUI(texto, estado, info)
    def initUI(self, texto, estado, info):
        self.setGeometry(round(50*val_res), round(50*val_res), round(1700*val_res), round(1030*val_res))
        #self.setGeometry(50, 50, 1700, 1030)
        self.setStyleSheet("""QWidget { background-color: #030918; border: 5px solid #030918; }""")
        self.setWindowTitle(texto)
        main_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""QScrollArea { border: 5px solid white; }
            QScrollBar:vertical {background-color: #030918;width: 25px;border-radius: 6px;}
            QScrollBar::handle:vertical {background-color: white;border-radius: 12px;}""")
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)
        self.start_generation(estado, info)
    def start_generation(self, estado, info):
        self.thread = Envio_mensajes(estado, info)
        self.thread.message_sent.connect(self.add_message)
        self.thread.finished.connect(self.show_buttons)
        self.thread.start()
    def add_message(self, message, color):
        label = QLabel(message)
        label.setStyleSheet(f"color: {color};font-size: 22px;")
        label.setWordWrap(True)
        self.content_layout.addWidget(label)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
    def show_buttons(self, valor=False, info={}):
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        if valor:
            cancel_button = QPushButton("Cancelar")
            cancel_button.setStyleSheet("""QPushButton {color: #030918;padding: 2px;
                font-size: 22px;border: 0.5px solid white;border-radius: 5px;background-color: #ffffff;}""")
            cancel_button.clicked.connect(lambda: self.close_dialog(False, {}))
            button_layout.addWidget(cancel_button)
        continue_button = QPushButton("Continuar")
        continue_button.setStyleSheet("""QPushButton {color: #030918;padding: 2px;
                font-size: 22px;border: 0.5px solid white;border-radius: 5px;background-color: #ffffff;}""")
        continue_button.clicked.connect(lambda: self.close_dialog(True, info))
        button_layout.addWidget(continue_button)
        self.content_layout.addWidget(button_widget)
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
    def close_dialog(self, choice, info):
        self.result = choice
        self.dic_info = info
        self.accept()

def run_app(texto, estado, info=None):
    dialog = Crear_ventana_texto(texto, estado, info)
    result = dialog.exec_()
    eleccion = dialog.result
    info_add = dialog.dic_info
    if eleccion and len(info_add):
        estado = "generar_"+estado
        dialog = Crear_ventana_texto(texto, estado, info_add)
        result = dialog.exec_()
        if "anual" in estado:
            estado = estado+"_union"
            eleccion = dialog.result
            info_add = dialog.dic_info
            dialog = Crear_ventana_texto(texto, estado, info_add)
            result = dialog.exec_()
    return dialog.result