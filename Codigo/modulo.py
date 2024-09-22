# ---------------------------------------------------------------------------------------------------------
# Python: 3.10.11 64-bit
# & Código Versión 1 - VANTI
import os
import sys
import time
import json
import zipfile
import glob
from datetime import datetime
import pandas as pd
import numpy as np
import chardet
import math
import csv
import googlemaps
import shutil
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

global lista_meses, lista_empresas, lista_anios, dic_reportes, lista_reportes_generales, reportes_generados, lista_reportes_totales,chunksize,llaves_dic_reporte, dic_carpetas, dic_filiales,antidad_datos_excel, dic_nit, cantidad_datos_estilo_excel,grupo_vanti,mercado_relevante,mercado_relevante_resumen,tabla_3,tabla_11,fecha_actual,lista_trimestres
grupo_vanti = "Grupo Vanti"
dic_carpetas = leer_archivos_json(ruta_constantes+"carpetas.json")
lista_anios = list(leer_archivos_json(ruta_constantes+"anios.json")["datos"].values())
lista_meses = list(leer_archivos_json(ruta_constantes+"tabla_18.json")["datos"].values())
lista_trimestres = list(leer_archivos_json(ruta_constantes+"trimestres.json")["datos"].values())
dic_filiales = leer_archivos_json(ruta_constantes+"tabla_empresa.json")["datos"]
dic_nit = leer_archivos_json(ruta_constantes+"tabla_nit.json")["datos"]
lista_filiales = list(dic_filiales.keys())
dic_reportes = dic_carpetas["carpeta_6"]
lista_reportes_generales = leer_archivos_json(ruta_constantes+"carpetas_1.json")["carpeta_2"]
reportes_generados = leer_archivos_json(ruta_constantes+"carpetas_1.json")["carpeta_4"]
mercado_relevante = leer_archivos_json(ruta_constantes+"mercado_relevante.json")
mercado_relevante_resumen = leer_archivos_json(ruta_constantes+"mercado_relevante_resumen.json")
chunksize = 60000
cantidad_datos_excel = chunksize
cantidad_datos_estilo_excel = 120000
llaves_dic_reporte = ["generales_no_float","generales_float","generales_fecha","generales_hora"]
tabla_3 = leer_archivos_json(ruta_constantes+"tabla_3.json")
tabla_11 = leer_archivos_json(ruta_constantes+"/tabla_11.json")
def crear_lista_reportes_totales():
    dic = leer_archivos_json(ruta_constantes+"reportes_disponibles.json")["datos"]
    lista = []
    for i in dic:
        lista.extend(dic[i])
    return lista
lista_reportes_totales = crear_lista_reportes_totales()
fecha_actual = datetime.now()

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
# *                                             Manejo DataFrames
# * -------------------------------------------------------------------------------------------------------
def leer_dataframe(archivo):
    encoding_1 = elegir_codificacion(archivo)
    df = pd.read_csv(archivo, encoding=encoding_1)
    return df

def leer_dataframe_utf_8(archivo):
    df = pd.read_csv(archivo, encoding="utf-8-sig").reset_index(drop=True)
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
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','utf-16','utf-16-be','utf-32','ascii',
                                'windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
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
        except ValueError:
            pass
    return None

def lectura_dataframe_chunk_prueba(archivo, valor_chunksize=40000,separador=","):
    lista_codificaciones = [elegir_codificacion(archivo)]
    lista_codificaciones.extend(['utf-8-sig','utf-8','iso-8859-1','latin-1','utf-16','utf-16-be','utf-32','ascii',
                                'windows-1252','iso-8859-2','iso-8859-5','koi8-r','big5','gb2312',
                                'shift-jis','euc-jp','mac_roman','utf-7','cp437','cp850','ibm866','tis-620'])
    for elemento in lista_codificaciones:
        try:
            for i, chunk in enumerate(pd.read_csv(archivo, chunksize=valor_chunksize, encoding=elemento, sep=separador,low_memory=False)):
                df_prueba = chunk.reset_index(drop=True).copy()
                return True
        except pd.errors.ParserError:
            pass
        except UnicodeDecodeError:
            pass
        except UnicodeError:
            pass
        except ValueError:
            pass
    return False

def generar_suma_df_filiales(df, lista_total, lista_suma):
    df = df.reset_index(drop=True)
    columnas = list(df.columns)
    lista_df = []
    lista_filiales = list(df["Filial"].unique())
    for filial in lista_filiales:
        df_filial = df[df["Filial"]==filial].reset_index(drop=True)
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
    for columna in columnas:
        if columna in ["Filial","NIT"]:
            lista_fila.append(grupo_vanti)
        elif columna in lista_total:
            lista_fila.append("Total")
        elif columna in lista_suma:
            lista_fila.append(df_filial[columna].sum())
        else:
            lista_fila.append(df_filial[columna][0])
    df_final.loc[len(df_filial)] = lista_fila
    return df_final

# * -------------------------------------------------------------------------------------------------------
# *                                             Información horaria
# * -------------------------------------------------------------------------------------------------------

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

def lista_a_texto(lista, separador, salto=False):
    lista = [str(elemento) for elemento in lista]
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

def ciclo_creacion_carpetas(ubicacion, carpeta):
    for i in range(len(carpeta)):
        numeros_c = listado_numeros_lista(carpeta)
        ubi = ubicacion+"/"+numeros_c[i]+carpeta[i]
        os.makedirs(ubi, exist_ok=True)

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

def conversion_archivos_lista(lista_archivos, ext_original, ext_final, informar=False, lista_fallidos=[]):
    for archivo in lista_archivos:
        op = conversion_archivos(archivo, ext_original, ext_final)
        if op == True:
            if informar:
                informar_archivo_creado(archivo.replace(ext_original, ext_final), informar)
        elif op == False:
            lista_fallidos.append(archivo)
    return lista_fallidos

def conversion_archivos(archivo, ext_original, ext_final):
    if ext_original in archivo:
        archivo = cambio_archivo(archivo, ext_original, ext_final)
        if archivo:
            return True
        else:
            return False
    return None

def cambiar_formato_dataframe(df, dic_reporte):
    df.columns = list(dic_reporte["generales"].keys())
    return df

def acortar_nombre(nombre):
    lista_nombre = nombre.split("\\")
    largo = len(lista_nombre)
    if largo > 6:
        texto = ("...\\"+lista_a_texto(lista_nombre[largo-6:], "\\", False)).replace("\\\\","\\")
    else: 
        texto = texto.replace("\\\\","\\")
    return texto

def informar_archivo_creado(nombre,valor):
    texto = acortar_nombre(nombre)
    if valor:
        print(f"\nArchivo {texto} creado\n")

def estandarizacion_archivos(lista_archivos, informar):
    dic_reporte = None
    for archivo in lista_archivos:
        conversion_archivos(archivo, ".csv", ".csv")
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

def evaluar_archivos_prueba(lista_archivos, lista_fallidos):
    for archivo in lista_archivos:
        op = lectura_dataframe_chunk_prueba(archivo)
        if not op:
            lista_fallidos.append(archivo)
    return lista_fallidos

def retirar_archivos_fallidos(lista_archivos, lista_fallidos):
    lista_archivos_final = []
    for archivo in lista_archivos:
        if archivo not in lista_fallidos:
            lista_archivos_final.append(archivo)
        else:
            print(f"\nArchivo {acortar_nombre(archivo)} posee errores en la lectura de información. Revisar el archivo\n")
    return lista_archivos_final

def cantidad_minima_info_archivo(lista_archivos):
    lista_archivos_info_min = []
    for archivo in lista_archivos:
        lista_archivo = archivo.split("\\")
        if len(lista_archivo[-1].split("_")) >= 4:
            lista_archivos_info_min.append(archivo)
    return lista_archivos_info_min

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

def archivos_aceptados_constantes(lista_archivos, informar=True):
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
                        informar_archivo_creado(ruta_constantes+"\\"+nombre_archivo, informar)
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
    lista_fallidos = conversion_archivos_lista(lista_archivos,"CSV","csv",informar=True, lista_fallidos=lista_fallidos)
    lista_fallidos = evaluar_archivos_prueba(lista_archivos, lista_fallidos=lista_fallidos)
    lista_fallidos = list(set(lista_fallidos))
    lista_archivos = busqueda_archivos_tipo(ruta_guardar_archivos, lista_fallidos=lista_fallidos)
    lista_archivos = retirar_archivos_fallidos(lista_archivos, lista_fallidos)
    lista_archivos = cantidad_minima_info_archivo(lista_archivos)
    for archivo in lista_archivos:
        try:
            nombre_archivo = archivo.split("\\")[-1]
            nombre_archivo_lista = nombre_archivo.split(".")
            nombre_archivo_lista[0] = nombre_archivo_lista[0].upper()
            nombre_archivo = lista_a_texto(nombre_archivo_lista, ".")
            ext_archivo = nombre_archivo.split("_")
            ext_archivo[-1] = ext_archivo[-1].split(".")[0]
            categoria = encontrar_categoria_reporte(ext_archivo[0])
            ext_archivo[3] = ext_archivo[3].lower().capitalize()
            ext_archivo.append(categoria)
            if None not in ext_archivo:
                ubi_1 = encontrar_nueva_ubi_archivo(ubi, ext_archivo)
                if comprobar_info_nombre_archivo(ext_archivo):
                    nueva_ubi = ubi_1+"\\"+nombre_archivo
                    shutil.move(archivo, nueva_ubi)
                    if informar:
                        informar_archivo_creado(nueva_ubi, informar)
        except FileNotFoundError:
            pass
        except PermissionError:
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

def tamanio_archivos(lista_archivos):
    suma = 0
    for archivo in lista_archivos:
        file_size_bytes = os.path.getsize(archivo)
        suma += float(round(file_size_bytes/(1024*1024),2))
    texto = f"{round(suma,2)} MB"
    return texto

def comprimir_archivos(lista_archivos, informar=True):
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
        with zipfile.ZipFile(tupla[1], 'w') as zipf:
            v_tamanio_archivos = tamanio_archivos(tupla[0])
            for file in tupla[0]:
                zipf.write(file, os.path.basename(file))
            if informar:
                print(f"\nSe recomienda almacenar la carpeta {llave} en un ubicación externa. \nLos archivos de la carpeta comprimida pesan {v_tamanio_archivos}\n")
            eliminar_archivos(tupla[0])

def almacenar_df_csv_y_excel(df, nombre, informar=True, almacenar_excel=True):
    df.to_csv(nombre, index=False, encoding="utf-8-sig")
    if informar:
        informar_archivo_creado(nombre, True)
    if almacenar_excel:
        df = leer_dataframe_utf_8(nombre)
        almacenar = mod_5.almacenar_csv_en_excel(df, nombre.replace(".csv",".xlsx"),"Datos")
        if informar and almacenar:
            informar_archivo_creado(nombre.replace(".csv",".xlsx"), True)

def generar_formato_almacenamiento_reportes(lista_df, nombre, informar=True,almacenar_excel=True):
    df_total = pd.concat(lista_df, ignore_index=True)
    lista_nombre = nombre.split("\\")
    lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
    lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
    lista_nombre.pop(-2)
    nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
    almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel)
    return lista_df, nombre

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Comerciales
# * -------------------------------------------------------------------------------------------------------

def codigo_DANE_texto(codigo_DANE):
    if len(codigo_DANE) > 0:
        lista_texto_codigo_DANE = []
        for elemento in codigo_DANE:
            lista_texto_codigo_DANE.append(str(elemento)[:5])
        return lista_a_texto(lista_texto_codigo_DANE,"_")
    else:
        return str(codigo_DANE[0])[:5]

#(lista_archivos, codigo_DANE, reporte, informar, valor_facturado,filial, subsidio=False, almacenar_excel=True):

def apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos, codigo_DANE, reporte, filial, valor_facturado=True):
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
                            df_codigo_DANE = df[df["Codigo_DANE"] == ele_codigo_DANE].reset_index(drop=True)
                            if len(df_codigo_DANE) > 0:
                                if ele_codigo_DANE not in dic_codigo_DANE:
                                    dic_codigo_DANE[ele_codigo_DANE] = {}
                                lista_sectores = list(df_codigo_DANE["Sector_consumo"].unique())
                                for sector in lista_sectores:
                                    try:
                                        s1 = int(sector)
                                        if s1 > 0:
                                            df_sector = df_codigo_DANE[df_codigo_DANE["Sector_consumo"] == s1].reset_index(drop=True)
                                            if s1 not in dic_codigo_DANE[ele_codigo_DANE]:
                                                dic_codigo_DANE[ele_codigo_DANE][s1] = [0,0,0] # cantidad_usuario, volumen, valor_total_facturado
                                            cantidad_usuario = len(list(df_sector["ID_Factura"].unique()))
                                            volumen = df_sector["Volumen"].sum()
                                            valor_total_facturado = df_sector["Valor_total_facturado"].sum()
                                            dic_codigo_DANE[ele_codigo_DANE][s1][0] += cantidad_usuario
                                            dic_codigo_DANE[ele_codigo_DANE][s1][1] += volumen
                                            dic_codigo_DANE[ele_codigo_DANE][s1][2] += valor_total_facturado
                                    except TypeError:
                                        pass
                                    except ValueError:
                                        pass
                    if len(dic_codigo_DANE) > 0:
                        lista_df_codigo_DANE = []
                        for ele_codigo_DANE, dic_dataframe in dic_codigo_DANE.items():
                            dic_dataframe = dict(sorted(dic_dataframe.items()))
                            dic_dataframe_2 = {"Tipo de usuario":[],
                                                "Sector de consumo":[],
                                                "Cantidad de usuarios":[],
                                                "Consumo m3":[]}
                            if valor_facturado:
                                dic_dataframe_2["Valor total facturado"] = []
                            for llave, valor in dic_dataframe.items():
                                try:
                                    valor_1 = tabla_11["datos"][str(llave)]
                                    dic_dataframe_2["Tipo de usuario"].append("No regulados")
                                    dic_dataframe_2["Sector de consumo"].append(valor_1)
                                    dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                                    dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                                    if valor_facturado:
                                        dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                                except KeyError:
                                    pass
                            lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3", "Codigo DANE"]
                            if valor_facturado:
                                lista_columnas.append("Valor total facturado")
                            df_codigo_DANE_gen = pd.DataFrame(dic_dataframe_2)
                            df_codigo_DANE_gen["Codigo DANE"] = ele_codigo_DANE
                            df_codigo_DANE_gen["Anio reportado"] = anio_reportado
                            df_codigo_DANE_gen["Mes reportado"] = mes_reportado
                            df_codigo_DANE_gen["Filial"] = dic_filiales[filial]
                            df_codigo_DANE_gen["NIT"] = dic_nit[dic_filiales[filial]]
                            df_codigo_DANE_gen = df_codigo_DANE_gen[lista_columnas]
                            lista_df_codigo_DANE.append(df_codigo_DANE_gen)
                        if len(lista_df_codigo_DANE) > 0:
                            df_codigo_DANE_gen_tot = pd.concat(lista_df_codigo_DANE, ignore_index=True)
                            v_codigo_DANE_texto = codigo_DANE_texto(codigo_DANE)
                            lista_nombre = archivo.split("\\")
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
                    if valor_facturado:
                        dic_dataframe_2["Valor total facturado"] = []
                    for llave, valor in dic_dataframe.items():
                        try:
                            valor_1 = tabla_11["datos"][str(llave)]
                            dic_dataframe_2["Tipo de usuario"].append("No regulados")
                            dic_dataframe_2["Sector de consumo"].append(valor_1)
                            dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                            dic_dataframe_2["Consumo m3"].append(round(valor[1]))
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
                    lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo.csv")
                    nombre = lista_a_texto(lista_nombre, "\\")
                    if len(df1) > 0:
                        lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3"]
                        if valor_facturado:
                            lista_columnas.append("Valor total facturado")
                        df1 = df1[lista_columnas]
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
    for elemento in lista_NIU:
        try:
            valor = dic_2[elemento] #consumo, valor_total_facturado
            if subsidio:
                if valor[0] > 0:
                    cantidad_usuario += 1
                if valor[0] > rango:
                    volumen += rango
                elif valor[0] <= rango:
                    volumen += valor[0]
                valor_total_facturado += valor[1]
            else:
                volumen += valor[0]
                valor_total_facturado += valor[1]
                cantidad_usuario += 1
        except KeyError:
            pass
    return cantidad_usuario, volumen, valor_total_facturado

def busqueda_sector_GRTT2(lista_archivos, dic_NIU, codigo_DANE, reporte, filial, nombre, valor_facturado=True, subsidio=False, rango=20):
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
                                                    dic_codigo_DANE[ele_codigo_DANE][s1] = [0,0,0] # cantidad_usuario, volumen, valor_total_facturado
                                                cantidad_usuario, volumen, valor_total_facturado = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                                dic_codigo_DANE[ele_codigo_DANE][s1][0] += cantidad_usuario
                                                dic_codigo_DANE[ele_codigo_DANE][s1][1] += volumen
                                                dic_codigo_DANE[ele_codigo_DANE][s1][2] += valor_total_facturado
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
                                                    dic_codigo_DANE[ele_codigo_DANE][s1] = [0,0,0] # cantidad_usuario, volumen, valor_total_facturado
                                                cantidad_usuario, volumen, valor_total_facturado = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
                                                dic_codigo_DANE[ele_codigo_DANE][s1][0] += cantidad_usuario
                                                dic_codigo_DANE[ele_codigo_DANE][s1][1] += volumen
                                                dic_codigo_DANE[ele_codigo_DANE][s1][2] += valor_total_facturado
                                        except TypeError:
                                            pass
                                        except ValueError:
                                            pass
                    if len(dic_codigo_DANE) > 0:
                        lista_df_codigo_DANE = []
                        for ele_codigo_DANE, dic_dataframe in dic_codigo_DANE.items():
                            dic_dataframe = dict(sorted(dic_dataframe.items()))
                            dic_dataframe_2 = {"Tipo de usuario":[],
                                                "Sector de consumo":[],
                                                "Cantidad de usuarios":[],
                                                "Consumo m3":[]}
                            if valor_facturado:
                                dic_dataframe_2["Valor total facturado"] = []
                            for llave, valor in dic_dataframe.items():
                                try:
                                    valor_1 = tabla_3["datos"][str(llave)]
                                    dic_dataframe_2["Tipo de usuario"].append("Regulados")
                                    dic_dataframe_2["Sector de consumo"].append(valor_1)
                                    dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                                    dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                                    if valor_facturado:
                                        dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                                except KeyError:
                                    pass
                            lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3", "Codigo DANE"]
                            if valor_facturado:
                                lista_columnas.append("Valor total facturado")
                            df_codigo_DANE_gen = pd.DataFrame(dic_dataframe_2)
                            df_codigo_DANE_gen["Codigo DANE"] = ele_codigo_DANE
                            df_codigo_DANE_gen["Anio reportado"] = anio_reportado
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
                        lista_sectores = list(df["Estrato"].unique())
                        for sector in lista_sectores:
                            if subsidio:
                                if str(sector) in ["1","2"]:
                                    try:
                                        s1 = int(sector)
                                        df_sector = df[df["Estrato"] == s1].reset_index(drop=True)
                                        lista_NIU_sector = list(df_sector["NIU"].unique())
                                        if s1 not in dic_dataframe:
                                            dic_dataframe[s1] = [0,0,0] # cantidad_usuario, volumen, valor_total_facturado
                                        cantidad_usuario, volumen, valor_total_facturado = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
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
                                    if s1 > 0:
                                        df_sector = df[df["Estrato"] == s1].reset_index(drop=True)
                                        lista_NIU_sector = list(df_sector["NIU"].unique())
                                        if s1 not in dic_dataframe:
                                            dic_dataframe[s1] = [0,0,0] # cantidad_usuario, volumen, valor_total_facturado
                                        cantidad_usuario, volumen, valor_total_facturado = buscar_NIU(lista_NIU_sector, dic_NIU, subsidio, rango)
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
                    if valor_facturado:
                        dic_dataframe_2["Valor total facturado"] = []
                    for llave, valor in dic_dataframe.items():
                        try:
                            valor_1 = tabla_3["datos"][str(llave)]
                            dic_dataframe_2["Tipo de usuario"].append("Regulados")
                            dic_dataframe_2["Sector de consumo"].append(valor_1)
                            dic_dataframe_2["Cantidad de usuarios"].append(valor[0])
                            dic_dataframe_2["Consumo m3"].append(round(valor[1]))
                            if valor_facturado:
                                dic_dataframe_2["Valor total facturado"].append(round(valor[2]))
                        except KeyError:
                            pass
                    lista_columnas = ["NIT","Filial","Anio reportado","Mes reportado","Tipo de usuario","Sector de consumo","Cantidad de usuarios","Consumo m3"]
                    if valor_facturado:
                        lista_columnas.append("Valor total facturado")
                    df1 = pd.DataFrame(dic_dataframe_2)
                    df1["Anio reportado"] = anio_reportado
                    df1["Mes reportado"] = mes_reportado
                    df1["Filial"] = dic_filiales[filial]
                    df1["NIT"] = dic_nit[dic_filiales[filial]]
                    df1 = df1[lista_columnas]
                    lista_nombre = nombre.split("\\")
                    if subsidio:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo_subsidio.csv")
                    else:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo.csv")
                    nombre = lista_a_texto(lista_nombre,"\\")
                    return df1, nombre
            return None, None
    return None, None

def apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos, codigo_DANE, reporte, valor_facturado,filial, subsidio=False):
    for archivo in lista_archivos:
        if reporte in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                dic_1 = {}
                for i in range(len(lista_df)):
                    df = lista_df[i].copy().reset_index()
                    for pos in range(len(df)):
                        try:
                            elemento = df["NIU"][pos]
                            consumo = float(df["Consumo"][pos])
                            valor_total_facturado = float(df["Valor_total_facturado"][pos])
                            if not math.isnan(consumo) and consumo > 0 and not math.isnan(valor_total_facturado) and valor_total_facturado > 0:
                                if elemento not in dic_1:
                                    dic_1[elemento] = [0,0] #consumo, valor_total_facturado
                                dic_1[elemento][0] += consumo
                                dic_1[elemento][1] += valor_total_facturado
                        except ValueError:
                            pass
                        except TypeError:
                            pass
                df1, nombre = busqueda_sector_GRTT2(lista_archivos, dic_1, codigo_DANE, "GRTT2", filial, archivo, valor_facturado, subsidio)
                if nombre:
                    return df1, nombre
                else:
                    return None, None
            else:
                return None, None
    return None, None

def apoyo_reporte_comercial_sector_consumo(df1, n1, df2, n2, informar=True, subsidio=False):
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
        almacenar_df_csv_y_excel(df3, n1, informar, subsidio)
        almacenar_df_csv_y_excel(df3, n2, informar, subsidio)
        return df3, n1
    elif n1:
        lista_n1 = n1.split("\\")
        nombre_1 = lista_n1[-1].split("_")[1:]
        lista_n1[-1] = lista_a_texto(nombre_1, "_", False)
        n1 = lista_a_texto(lista_n1, "\\", False)
        df3 = df1.copy()
        almacenar_df_csv_y_excel(df3, n1, informar, subsidio)
        return df3, n1
    elif n2:
        lista_n2 = n2.split("\\")
        nombre_2 = lista_n2[-1].split("_")[1:]
        lista_n2[-1] = lista_a_texto(nombre_2, "_", False)
        n2 = lista_a_texto(lista_n2, "\\", False)
        df3 = df2.copy()
        almacenar_df_csv_y_excel(df3, n2, informar, subsidio)
        return df3, n2
    return None, None

def reporte_comercial_sector_consumo(lista_archivos, seleccionar_reporte, codigo_DANE=None, valor_facturado=True, informar=True, subsidio=False, almacenar_excel=True, total=False):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    n1 = None
    n2 = None
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    nombre_compilado = None
    for filial in lista_filiales_archivo:
        proceso = None
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df1, n1 = apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos_filial, codigo_DANE, "GRC1", valor_facturado, filial, subsidio)
            if not subsidio:
                df2, n2 = apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos_filial, codigo_DANE, "GRC2", filial, valor_facturado)
            df,nombre = apoyo_reporte_comercial_sector_consumo(df1, n1, df2, n2, informar, subsidio)
            if nombre:
                lista_df_filiales.append(df)
                nombre_compilado = nombre
    if len(lista_df_filiales) > 0 and len(lista_filiales_archivo) == 4 and nombre_compilado:
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        lista_nombre = nombre_compilado.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        lista_nombre.pop(-2)
        nuevo_nombre = lista_a_texto(lista_nombre,"\\")
        if total:
            df_total_suma, proceso = generar_sumatoria_df(df_total)
            if proceso:
                df_total = df_total_suma.copy()
                nuevo_nombre = nuevo_nombre.replace(".csv","_sumatoria.csv")
        almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel)
        return df_total, nuevo_nombre
    else:
        return None, None

def apoyo_reporte_comparacion_prd_cld_cer(lista_archivos, informar, filial):
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
    suma_NIU_GRC1 = df_porcentaje[df_porcentaje["Archivo"] == "GRC1"]["Usuarios NIU Unicos"].sum()
    if proceso_CLD:
        df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_CLD', 'Nuevos NIU'] = suma_NIU_GRC1-df_porcentaje[df_porcentaje["Archivo"] == "GRC1_SAP_CLD"]["Usuarios NIU Unicos"].sum()
    if proceso_PRD:
        df_porcentaje.loc[df_porcentaje['Archivo'] == 'GRC1_SAP_PRD', 'Nuevos NIU'] = suma_NIU_GRC1-df_porcentaje[df_porcentaje["Archivo"] == "GRC1_SAP_PRD"]["Usuarios NIU Unicos"].sum()
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
    almacenar_df_csv_y_excel(df_porcentaje, nombre)
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
        almacenar_df_csv_y_excel(df_total, nombre_final)
    except ValueError:
        pass

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

def apoyo_reporte_comparacion_p1_p2(lista_archivos, informar, cantidad_filas, p1, p2):
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
        nombre = nombre_archivo.replace("_resumen", f"_comparacion_iguales{p1}{p2}")
        almacenar_df_csv_y_excel(df_iguales, nombre)
        for dic in lista_diferentes:
            for lista in dic.values():
                for i in range(len(lista)):
                    lista_df_diferentes[i].append((lista[i][0],lista[i][1]))
        dic_df_diferentes = {}
        for i in range(largo):
            dic_df_diferentes[lista_1[i]] = lista_df_diferentes[i]
        df_diferentes = pd.DataFrame(dic_df_diferentes)
        nombre = nombre_archivo.replace("_resumen", f"_comparacion_diferentes{p1}{p2}")
        almacenar_df_csv_y_excel(df_diferentes, nombre, almacenar_excel=False)
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
            informar_archivo_creado(nombre, True)
    else:
        print(f"\nDeben existir los archivos {p1} y {p2} para el proceso de comparacion\n")

def reporte_comparacion_SAP(lista_archivos, seleccionar_reporte, informar, cantidad_filas, p1, p2):
    for filial in seleccionar_reporte["filial"]:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            apoyo_reporte_comparacion_p1_p2(lista_archivos_filial, informar, cantidad_filas, p1, p2) #Colocar SIEMPRE primero GRC1, PRD / GRC1, PRD / PRD, CLD

def generar_sumatoria_df(df):
    columnas = list(df.columns)
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
    pass
    """lista_df_anual = []
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
            informar_archivo_creado(nombre, True)"""

def apoyo_reporte_usuarios_filial(lista_archivos,informar,filial,almacenar_excel=True):
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
                        valor = df["NIU"][j]
                        if valor not in dic_dataframe_NIU:
                            dic_dataframe_NIU[valor] = 1 #Cantidad de apariciones de NIU, existencia en el GRC1 (2=No)
                        else:
                            dic_dataframe_NIU[valor] += 1
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
        dic_df_NIU_GRTT2_GRC1 = {"NIU":[],
                                    "Apariciones_GRTT2":[],
                                    "Existe_GRC1":[]}
        for llave, valor in dic_dataframe_NIU.items():
            dic_df_NIU_GRTT2_GRC1["NIU"].append(llave)
            dic_df_NIU_GRTT2_GRC1["Apariciones_GRTT2"].append(valor)
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
        df_NIU_GRTT2_GRC1.to_csv(nombre.replace("_resumen","_inventario_suscriptores_activos"), index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nombre.replace("_resumen","_inventario_suscriptores_activos"), True)
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
        df_filial_resumen.to_csv(nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nombre, True)
        df_filial_resumen = leer_dataframe_utf_8(nombre)
        almacenar = mod_5.almacenar_csv_en_excel(df_filial_resumen, nombre.replace(".csv",".xlsx"),"Datos")
        if informar and almacenar and almacenar_excel:
            informar_archivo_creado(nombre.replace(".csv",".xlsx"), True)
        return df_filial_resumen, nombre

def reporte_usuarios_filial(lista_archivos, informar, seleccionar_reporte, almacenar_excel=True):
    lista_df_filiales = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df,nombre = apoyo_reporte_usuarios_filial(lista_archivos_filial,informar,filial)
            if nombre:
                lista_df_filiales.append(df)
    if len(lista_archivos_filial) > 0 and len(lista_filiales_archivo) == 4:
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        lista_nombre = nombre.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        lista_nombre.pop(-2)
        lista_nombre[-4] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\")
        df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        if informar:
            informar_archivo_creado(nuevo_nombre, True)
        df1 = leer_dataframe_utf_8(nuevo_nombre)
        if almacenar_excel:
            almacenar = mod_5.almacenar_csv_en_excel(df1,nuevo_nombre.replace(".csv",".xlsx"),"Datos")
            if informar and almacenar:
                informar_archivo_creado(nuevo_nombre.replace(".csv",".xlsx"), True)
        return df1, nuevo_nombre

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

def apoyo_reporte_usuarios_unicos_mensual(lista_archivos, informar, filial, almacenar_excel=True):
    proceso_GRC1 = False
    proceso_GRC2 = False
    proceso_GRTT2 = False
    nombre_1 = None
    nombre_2 = None
    lista_archivos_exitosos = []
    for archivo in lista_archivos:
        if "GRC1" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                proceso_GRC1 = True
                lista_archivos_exitosos.append(archivo)
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                dic_reg = {}
                lista_reg = [0,0,0] #m3, Valor_total_facturado, Valor_consumo_facturado
                dic_reg_factura = {}
                for df in lista_df:
                    for i in range(len(df)):
                        try:
                            valor = int(df["NIU"][i])
                            if valor not in dic_reg:
                                dic_reg[valor] = [valor,0,0,0,0,None,None] #NIU,Cantidad_facturas,Consumo,Valor_consumo_facturado,Valor_total_facturado,Codigo_DANE,Sector_consumo
                            dic_reg[valor][1] += 1
                            factura = str(df["ID_factura"][i]).upper().strip()
                            if factura[0] == "F":
                                if factura not in dic_reg_factura:
                                    dic_reg_factura[factura] = True
                            try:
                                valor_1 = float(df["Consumo"][i])
                                if not math.isnan(valor_1) and valor_1 > 0:
                                    lista_reg[0] += valor_1
                                    dic_reg[valor][2] += valor_1
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                            try:
                                valor_1 = float(df["Valor_total_facturado"][i])
                                if not math.isnan(valor_1) and valor_1 > 0:
                                    lista_reg[1] += valor_1
                                    dic_reg[valor][4] += valor_1
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                            try:
                                valor_1 = float(df["Facturacion_consumo"][i])
                                if not math.isnan(valor_1) and valor_1 > 0:
                                    lista_reg[2] += valor_1
                                    dic_reg[valor][3] += valor_1
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                        except ValueError:
                            pass
                        except TypeError:
                            pass
        elif "GRC2" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                proceso_GRC2 = True
                mes_reportado = lista_df[0]["Mes_reportado"][0]
                anio_reportado = lista_df[0]["Anio_reportado"][0]
                lista_archivos_exitosos.append(archivo)
                dic_no_reg = {}
                lista_no_reg = [0,0,0] #m3, Valor_total_facturado, Valor_consumo_facturado
                dic_no_reg_factura = {}
                for df in lista_df:
                    for i in range(len(df)):
                        try:
                            valor = int(df["NIU"][i])
                            if valor not in dic_no_reg:
                                dic_no_reg[valor] = [valor,0,0,0,0,None,None] #NIU,Cantidad_facturas,Consumo,Valor_consumo_facturado,Valor_total_facturado,Codigo_DANE,Sector_consumo
                            dic_no_reg[valor][1] += 1
                            dic_no_reg[valor][5] = df["Codigo_DANE"][i]
                            try:
                                valor_1 = int(df["Sector_consumo"][i])
                                try:
                                    valor_1 = tabla_11["datos"][str(valor_1)]
                                    dic_no_reg[valor][6] =valor_1
                                except KeyError:
                                    dic_no_reg[valor][6] = ""
                            except ValueError:
                                dic_no_reg[valor][6] = ""
                            except TypeError:
                                dic_no_reg[valor][6] = ""
                            factura = str(df["ID_Factura"][i]).upper().strip()
                            if factura[0] == "F":
                                if factura not in dic_no_reg_factura:
                                    dic_no_reg_factura[factura] = True
                            try:
                                valor_1 = float(df["Volumen"][i])
                                if not math.isnan(valor_1) and valor_1 > 0:
                                    lista_no_reg[0] += valor_1
                                    dic_no_reg[valor][2] += valor_1
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                            try:
                                valor_1 = float(df["Valor_total_facturado"][i])
                                if not math.isnan(valor_1) and valor_1 > 0:
                                    lista_no_reg[1] += valor_1
                                    dic_no_reg[valor][4] += valor_1
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                            try:
                                valor_1 = float(df["Facturacion_por_demanda_volumen"][i])
                                if not math.isnan(valor_1) and valor_1 > 0:
                                    lista_no_reg[2] += valor_1
                                    dic_no_reg[valor][3] += valor_1
                            except ValueError:
                                pass
                            except TypeError:
                                pass
                        except ValueError:
                            pass
                        except TypeError:
                            pass
        elif "GRTT2" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                dic_GRTT2 = {}
                for df in lista_df:
                    for i in range(len(df)):
                        try:
                            valor = int(df["NIU"][i])
                            if valor not in dic_GRTT2:
                                dic_GRTT2[valor] = [df["Codigo_DANE"][i],
                                                df["Estrato"][i]]
                        except ValueError:
                            pass
                        except TypeError:
                            pass
                proceso_GRTT2 = True
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
                    except KeyError:
                        dic_reg[v_NIU][6] = ""
                except ValueError:
                    dic_reg[v_NIU][6] = ""
                except TypeError:
                    dic_reg[v_NIU][6] = ""
            else:
                dic_reg[v_NIU][5] = ""
                dic_reg[v_NIU][6] = ""
        for lista_NIU in dic_reg.values():
            dic_NIU_factura["Clasificacion_usuario"].append("Regulado")
            dic_NIU_factura["NIU"].append(lista_NIU[0])
            dic_NIU_factura["Consumo_m3"].append(lista_NIU[1])
            dic_NIU_factura["Cantidad_facturas_emitidas"].append(lista_NIU[2])
            dic_NIU_factura["Valor_consumo_facturado"].append(lista_NIU[3])
            dic_NIU_factura["Valor_total_facturado"].append(lista_NIU[4])
            dic_NIU_factura["Codigo_DANE"].append(lista_NIU[5])
            dic_NIU_factura["Sector_consumo"].append(lista_NIU[6])
    if proceso_GRC2:
        for lista_NIU in dic_no_reg.values():
            dic_NIU_factura["Clasificacion_usuario"].append("No Regulado")
            dic_NIU_factura["NIU"].append(lista_NIU[0])
            dic_NIU_factura["Consumo_m3"].append(lista_NIU[1])
            dic_NIU_factura["Cantidad_facturas_emitidas"].append(lista_NIU[2])
            dic_NIU_factura["Valor_consumo_facturado"].append(lista_NIU[3])
            dic_NIU_factura["Valor_total_facturado"].append(lista_NIU[4])
            dic_NIU_factura["Codigo_DANE"].append(lista_NIU[5])
            dic_NIU_factura["Sector_consumo"].append(lista_NIU[6])
    df1 = pd.DataFrame(dic_NIU_factura)
    if len(df1):
        lista_nombre = archivo.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        nombre = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_usuarios_unicos_facturacion")
        almacenar_df_csv_y_excel(df1, nombre, almacenar_excel=False)
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
        for archivo in lista_archivos_exitosos:
            lista_nombre = archivo.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            nombre_2 = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_reporte_facturacion")
            almacenar_df_csv_y_excel(df, nombre_2)
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
        dic_df["Valor_consumo_facturado"].append(lista_reg[1])
        dic_df["Valor_total_facturado"].append(lista_reg[1])
    if proceso_GRC2:
        dic_df["Clasificacion_usuarios"].append("No Regulados")
        dic_df["Cantidad_usuarios_unicos"].append(len(dic_no_reg))
        dic_df["Cantidad_facturas_emitidas"].append(len(dic_no_reg_factura))
        dic_df["Consumo_m3"].append(lista_no_reg[0])
        dic_df["Valor_consumo_facturado"].append(lista_no_reg[1])
        dic_df["Valor_total_facturado"].append(lista_no_reg[1])
    df = pd.DataFrame(dic_df)
    if len(df):
        df["Filial"] = dic_filiales[filial]
        df["NIT"] = dic_nit[dic_filiales[filial]]
        df["Mes_reportado"] = mes_reportado
        df["Anio_reportado"] = anio_reportado
        df = df[["Filial","NIT","Anio_reportado","Mes_reportado","Clasificacion_usuarios","Cantidad_usuarios_unicos",
                "Cantidad_facturas_emitidas","Consumo_m3","Valor_consumo_facturado","Valor_total_facturado"]]
        for archivo in lista_archivos_exitosos:
            lista_nombre = archivo.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            nombre_2 = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_usuarios_unicos")
            almacenar_df_csv_y_excel(df, nombre_2)
    return df, nombre_2, df2, nombre_1

def reporte_usuarios_unicos_mensual(lista_archivos, informar, seleccionar_reporte, almacenar_excel=True):
    lista_df_filiales_1 = []
    lista_df_filiales_2 = []
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df1,nombre_1,df2,nombre_2 = apoyo_reporte_usuarios_unicos_mensual(lista_archivos_filial,informar,filial, almacenar_excel)
            if nombre_1:
                lista_df_filiales_1.append(df1)
            if nombre_2:
                lista_df_filiales_2.append(df2)
    if len(lista_df_filiales_2) > 0 and len(lista_filiales_archivo) == 4:
        df_total = pd.concat(lista_df_filiales_2, ignore_index=True)
        df_total = generar_suma_df_filiales(df_total, ["Clasificacion_usuarios"],["Sector_consumo",
                                                        "Cantidad_facturas_emitidas","Consumo_m3","Valor_consumo_facturado","Valor_total_facturado"])
        lista_nombre = nombre_2.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        lista_nombre.pop(-2)
        lista_nombre[-4] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\")
        almacenar_df_csv_y_excel(df_total, nuevo_nombre)
    if len(lista_df_filiales_1) > 0 and len(lista_filiales_archivo) == 4:
        df_total = pd.concat(lista_df_filiales_1, ignore_index=True)
        df_total = generar_suma_df_filiales(df_total,["Clasificacion_usuarios"],["Cantidad_facturas_emitidas",
                                                        "Consumo_m3","Valor_consumo_facturado","Valor_total_facturado"])
        lista_nombre = nombre_1.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        lista_nombre.pop(-2)
        lista_nombre[-4] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\")
        almacenar_df_csv_y_excel(df_total, nuevo_nombre)
        return df_total, nuevo_nombre

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
            lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Comercial"]
            nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_patrimonial_{f_inicial[0]}_{f_inicial[1]}_{f_inicial[0]}_{f_inicial[1]}")
            almacenar_df_csv_y_excel(df_total,nuevo_nombre)

        else:
            print(f"No es posible acceder al archivo {archivo}.")
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")

def reporte_info_reclamos(fi,ff,listas_unidas):
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
                    lista_porcentaje.append(str(round((df_filtro['Numero_Facturas_Expedidas'][j]/df_filtro['Numero_Reclamos_Facturacion'][j])*10000,2))+" %")
                df_filtro["Porcentaje_reclamos_fact_10000"] = lista_porcentaje
                lista_df.append(df_filtro)
            df_total = pd.concat(lista_df, ignore_index=True)
            lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Comercial"]
            nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_reclamos_facturacion_10000_{f_inicial[0]}_{f_inicial[1]}_{f_final[0]}_{f_final[1]}")
            almacenar_df_csv_y_excel(df_total,nuevo_nombre)
        else:
            print(f"No es posible acceder al archivo {archivo}.")
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")

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

def apoyo_reporte_tarifas_mensual(lista_archivos,informar,filial,almacenar_excel=True):
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
            almacenar_df_csv_y_excel(df_filtro, nombre, informar, almacenar_excel)
            return df_filtro, nombre
        else:
            return None, None

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
                lista_df_filiales.append(df)
    if len(lista_df_filiales) > 0 and len(lista_filiales_archivo) == 4:
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        lista_nombre = nombre.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        lista_nombre.pop(-2)
        nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
        df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel)
        return df_total,nuevo_nombre

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Técnicos
# * -------------------------------------------------------------------------------------------------------

def apoyo_generar_reporte_indicadores_tecnicos_mensual(lista_archivos, informar, filial, almacenar_excel=True):
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
        almacenar_df_csv_y_excel(df, nuevo_nombre, informar, almacenar_excel)
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
                lista_df_filiales.append(df)
    if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
        df_total = pd.concat(lista_df_filiales, ignore_index=True)
        lista_nombre = nombre.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
        lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
        nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
        df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
        almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel)
        return df_total,nuevo_nombre

def diferencia_minutos_fechas(df, lista_dia_1, lista_hora_1, lista_dia_2, lista_hora_2):
    lista_dif_minutos = []
    for i in range(len(lista_dia_1)):
        try:
            fecha_1 = datetime.strptime(str(lista_dia_1[i])+" "+str(lista_hora_1[i]), '%d-%m-%Y %H:%M')
            fecha_2 = datetime.strptime(str(lista_dia_2[i])+" "+str(lista_hora_2[i]), '%d-%m-%Y %H:%M')
            lista_dif_minutos.append(float(round((fecha_2-fecha_1).total_seconds() / 60)))
        except ValueError:
            lista_dif_minutos.append(np.nan)
        except TypeError:
            lista_dif_minutos.append(np.nan)
        except AttributeError:
            lista_dif_minutos.append(np.nan)
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

def apoyo_generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos, filial, informar=True, almacenar_excel=True):
    for archivo in lista_archivos:
        df = leer_dataframe_utf_8(archivo)
        anio_archivo = df["Anio_reportado"][0]
        mes_archivo = df["Mes_reportado"][0]
        df = diferencia_minutos_fechas(df, list(df["Fecha_solicitud"]), list(df["Hora_solicitud"]), list(df["Fecha_llegada_servicio_tecnico"]), list(df["Hora_llegada_servicio_tecnico"]))
        lista_eventos = list(df["Observaciones"].unique())
        dic_df_evento = {"Tipo_evento":[],
                        "Cantidad_eventos":[],
                        "Tiempo_promedio_llegada (min)":[]}
        dic_minutos_evento_no_contr = {"0 - 15 min":((0,15),[]),
                                            "15 - 30 min":((15,30),[]),
                                            "30 - 45 min":((30,45),[]),
                                            "45 - 60 min":((45,60),[]),
                                            "> 1 hora":((60,float("inf")),[])}
        dic_minutos_evento_contr = {"0 - 15 min":((0,15),[]),
                                            "15 - 30 min":((15,30),[]),
                                            "30 - 45 min":((30,45),[]),
                                            "45 - 60 min":((45,60),[]),
                                            "1 hora - 4 horas":((60,240),[]),
                                            "4 hora - 8 horas":((240,480),[]),
                                            "> 8 horas":((480,float("inf")),[]),}
        dic_minutos_evento = {}
        for evento in lista_eventos:
            df_filtro = df[df["Observaciones"] == evento].reset_index(drop=True)
            if "NO CONTROL" in evento:
                dic_minutos_evento[evento] = dic_minutos_evento_no_contr.copy()
            else:
                dic_minutos_evento[evento] = dic_minutos_evento_contr.copy()
            for i in range(len(df_filtro)):
                for llave, tupla in dic_minutos_evento[evento].items():
                    if tupla[0][0] < df_filtro["Cantidad_minutos"][i] <= tupla[0][1]:
                        dic_minutos_evento[evento][llave][1].append(float(df_filtro["Cantidad_minutos"][i]))
            dic_df_evento["Tipo_evento"].append(evento)
            dic_df_evento["Cantidad_eventos"].append(len(df_filtro))
            dic_df_evento["Tiempo_promedio_llegada (min)"].append(round(df_filtro["Cantidad_minutos"].mean()))
        nombre = archivo.replace("_resumen.csv","_indicador_tecnico_IRST.csv")
        nombre_1 = archivo.replace("_resumen.csv","_indicador_tecnico_IRST_minutos.csv")
        dic_df_evento_minutos = {"Tipo_evento":[],
                                "Clasificacion":[],
                                "Cantidad_eventos":[]}
        for evento, dic_minuto in dic_minutos_evento.items():
            for llave, valor in dic_minuto.items():
                dic_df_evento_minutos["Tipo_evento"].append(evento)
                dic_df_evento_minutos["Clasificacion"].append(llave)
                dic_df_evento_minutos["Cantidad_eventos"].append(len(valor[1]))
        df2 = pd.DataFrame(dic_df_evento_minutos)
        df2 = porcentaje_tipo_evento_minutos(df2, lista_eventos)
        df2["Filial"] = dic_filiales[filial]
        df2["NIT"] = dic_nit[dic_filiales[filial]]
        df2["Anio_reportado"] = anio_archivo
        df2["Mes_reportado"] = mes_archivo
        almacenar_df_csv_y_excel(df2, nombre_1, informar, almacenar_excel)
        df1 = pd.DataFrame(dic_df_evento)
        df1 = porcentaje_tipo_evento(df1)
        df1["Filial"] = dic_filiales[filial]
        df1["NIT"] = dic_nit[dic_filiales[filial]]
        df1["Anio_reportado"] = anio_archivo
        df1["Mes_reportado"] = mes_archivo
        almacenar_df_csv_y_excel(df1, nombre, informar, almacenar_excel)
        return df1, nombre, df2, nombre_1

def generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos, seleccionar_reporte, informar=True,almacenar_excel=True):
    lista_df_filiales_1 = []
    lista_df_filiales_2 = []
    df_total = None
    df_total_2 = None
    nuevo_nombre = None
    nuevo_nombre_2 = None
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for filial in lista_filiales_archivo:
        lista_archivos_filial = []
        for archivo in lista_archivos:
            if filial in archivo:
                lista_archivos_filial.append(archivo)
        if len(lista_archivos_filial) > 0:
            df1,n1,df2,n2 = apoyo_generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos_filial,filial, informar,almacenar_excel)
            if n1:
                lista_df_filiales_1.append(df1)
            if n2:
                lista_df_filiales_2.append(df2)
    if len(lista_df_filiales_1) and len(lista_filiales_archivo) == 4:
        df_total, nuevo_nombre = generar_formato_almacenamiento_reportes(lista_df_filiales_1, n1, informar,almacenar_excel)
    if len(lista_df_filiales_2) and len(lista_filiales_archivo) == 4:
        df_total_2, nuevo_nombre_2 = generar_formato_almacenamiento_reportes(lista_df_filiales_2, n2, informar,almacenar_excel)
    return df_total, df_total_2, nuevo_nombre, nuevo_nombre_2

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

def generar_porcentaje_cumplimientos_regulatorios():
    nombre = "Reporte SUI"
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsx"
    if os.path.exists(archivo):
        df, proceso = mod_5.lectura_hoja_xlsx(archivo, nombre)
        if proceso:
            anio_actual = fecha_actual.year
            df['Fecha_establecida'] = pd.to_datetime(df['Fecha establecida'], errors='coerce')
            df = df.loc[df['Fecha_establecida'].dt.year == int(anio_actual)]
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
            df_porcentaje["Anio"] = anio_actual
            lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", str(anio_actual), "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
            nuevo_nombre = encontrar_ubi_archivo(lista_ubi, "porcentaje_cumplimientos_regulatorios")
            almacenar_df_csv_y_excel(df_porcentaje,nuevo_nombre)
        else:
            print(f"No es posible acceder al archivo {archivo}.")
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")

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
def busqueda_archivos_tipo(ubi_archivo,tipo=None, lista_fallidos=[]):
    if tipo:
        archivos_tipo = glob.glob(os.path.join(ubi_archivo, "*"+tipo))
    else:
        archivos_tipo = glob.glob(os.path.join(ubi_archivo, "*"))
    return archivos_tipo


def mostrar_texto(texto, tipo="texto"):
    linea = 160
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
