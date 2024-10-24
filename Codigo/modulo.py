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

global lista_meses, lista_empresas, lista_anios, dic_reportes, lista_reportes_generales, reportes_generados, lista_reportes_totales,chunksize,llaves_dic_reporte, dic_carpetas, dic_filiales,antidad_datos_excel, dic_nit, cantidad_datos_estilo_excel,grupo_vanti,mercado_relevante,mercado_relevante_resumen,tabla_3,tabla_11,fecha_actual,lista_trimestres, dic_meses_abre,lista_clasi_reportes,categoria_matriz_requerimientos
grupo_vanti = "Grupo Vanti"
dic_carpetas = leer_archivos_json(ruta_constantes+"carpetas.json")
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
chunksize = 60000
cantidad_datos_excel = chunksize
cantidad_datos_estilo_excel = 120000
llaves_dic_reporte = ["generales_no_float","generales_float","generales_fecha","generales_hora"]
tabla_3 = leer_archivos_json(ruta_constantes+"tabla_3.json")
tabla_11 = leer_archivos_json(ruta_constantes+"/tabla_11.json")
categoria_matriz_requerimientos = leer_archivos_json(ruta_constantes+"categoria_matriz_requerimientos.json")["datos"]
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
                    lista_df.append(chunk.reset_index(drop=True).copy())
                return lista_df
            except Exception:
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

def crear_carpeta_anual(fecha, lista_archivo):
    lista_archivo = lista_archivo[:-2]
    lista_archivo.append(fecha)
    nombre = lista_a_texto(lista_archivo, "\\")
    crear_carpeta(nombre)
    if not os.path.exists(nombre):
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

def acortar_nombre(nombre, cantidad=6):
    lista_nombre = nombre.split("\\")
    largo = len(lista_nombre)
    if largo > cantidad:
        texto = ("...\\"+lista_a_texto(lista_nombre[largo-cantidad:], "\\", False)).replace("\\\\","\\")
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
                    almacenar_df_csv_y_excel(df, nuevo_nombre, almacenar_excel=False)
                else:
                    v_nombre_archivo_json_reporte = nombre_archivo_json_reporte(archivo)
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
        print(archivo)
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
            categoria = encontrar_categoria_reporte(ext_archivo[0])
            ext_archivo[3] = ext_archivo[3].lower().capitalize()
            ext_archivo.append(categoria)
            if None not in ext_archivo:
                if comprobar_info_nombre_archivo(ext_archivo):
                    ubi_1 = encontrar_nueva_ubi_archivo(ubi, ext_archivo)
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

def almacenar_2_archivos(lista_archivos):
    conteo = 0
    for archivo in lista_archivos:
        if archivo.endswith((".csv")):
            conteo += 1
        if conteo >= 2:
            return True
    else:
        return False

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
        if almacenar_2_archivos(tupla[0]):
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
            lista_texto_codigo_DANE.append(int(str(elemento)[:5]))
        lista_texto_codigo_DANE.sort()
        lista_texto_codigo_DANE_str = [str(x) for x in lista_texto_codigo_DANE]
        return lista_a_texto(lista_texto_codigo_DANE_str,"_")
    else:
        return str(codigo_DANE[0])[:5]

def apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos, codigo_DANE, reporte, filial, valor_facturado=True, total=False, subsidio=False,facturas=False):
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
                                            df_sector = df_codigo_DANE[df_codigo_DANE["Sector_consumo"] == s1].reset_index(drop=True)
                                            if len(df_sector):
                                                if s1 not in dic_codigo_DANE[ele_codigo_DANE]:
                                                    dic_codigo_DANE[ele_codigo_DANE][s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                                df_sector['Composicion_usuario'] = df_sector['ID_Factura'].astype(str)+'_'+df_sector['Concepto_general_factura'].astype(str)+'_'+df_sector['Sector_consumo'].astype(str)
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
                                    dic_dataframe[s1] = [0,0,0,0,0,0,0].copy()#cantidad_usuarios,consumo,valor_total_facturado,valor_consumo_facturado,cantidad_facturas,subsidios,contribuciones
                                df_sector['Composicion_usuario'] = df_sector['ID_Factura'].astype(str)+'_'+df_sector['Concepto_general_factura'].astype(str)+'_'+df_sector['Sector_consumo'].astype(str)
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
                                dic_dataframe[s1][3] += valor_consumo_facturado
                                dic_dataframe[s1][4] += cantidad_facturas
                                dic_dataframe[s1][6] += contribuciones
                                dic["Cantidad de usuarios"] += cantidad
                                dic["Consumo m3"] += volumen
                                dic["Valor total facturado"] += valor_total
                                dic["Valor consumo facturado"] += valor_consumo_facturado
                                dic["Cantidad de facturas"] += cantidad_facturas
                                dic["Contribuciones"] += contribuciones
                            except ValueError:
                                pass
                            except TypeError:
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
                    df1["Mes reportado"] = mes_reportado
                    lista_nombre = archivo.split("\\")
                    if subsidio:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo_subsidio.csv")
                    else:
                        lista_nombre[-1] = lista_nombre[-1].replace("_resumen.csv", "_reporte_consumo.csv")
                    nombre = lista_a_texto(lista_nombre, "\\")
                    if len(df1) > 0:
                        df1 = df1[lista_columnas]
                        if total and not codigo_DANE:
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

def busqueda_sector_GRTT2(lista_archivos, dic_NIU, codigo_DANE, reporte, filial, nombre, valor_facturado=True, subsidio=False, facturas=False, rango=20):
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
                            df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['Codigo_DANE'])
                            df["Codigo_DANE"] = df["Codigo_DANE"].astype(int)
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

def apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos, codigo_DANE, reporte, valor_facturado,filial, subsidio=False, total=False, facturas=False):
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
                df1, nombre = busqueda_sector_GRTT2(lista_archivos, dic_1, codigo_DANE, "GRTT2", filial, archivo, valor_facturado, subsidio, facturas)
                if total and not codigo_DANE:
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

def apoyo_reporte_comercial_sector_consumo(df1, n1, df2, n2, informar=True):
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
        almacenar_df_csv_y_excel(df3, n1, informar)
        almacenar_df_csv_y_excel(df3, n2, informar)
        return df3, n1
    elif n1:
        lista_n1 = n1.split("\\")
        nombre_1 = lista_n1[-1].split("_")[1:]
        lista_n1[-1] = lista_a_texto(nombre_1, "_", False)
        n1 = lista_a_texto(lista_n1, "\\", False)
        df3 = df1.copy()
        almacenar_df_csv_y_excel(df3, n1, informar)
        return df3, n1
    elif n2:
        lista_n2 = n2.split("\\")
        nombre_2 = lista_n2[-1].split("_")[1:]
        lista_n2[-1] = lista_a_texto(nombre_2, "_", False)
        n2 = lista_a_texto(lista_n2, "\\", False)
        df3 = df2.copy()
        almacenar_df_csv_y_excel(df3, n2, informar)
        return df3, n2
    return None, None

def reporte_comercial_sector_consumo(dic_archivos, seleccionar_reporte, informar=True, codigo_DANE=None, valor_facturado=True, subsidio=False, almacenar_excel=True, total=False, facturas=False):
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
                df1, n1 = apoyo_reporte_comercial_sector_consumo_regulados(lista_archivos_filial, codigo_DANE, "GRC1", valor_facturado, filial, subsidio, total, facturas)
                df2, n2 = apoyo_reporte_comercial_sector_consumo_no_regulados(lista_archivos_filial, codigo_DANE, "GRC2", filial, valor_facturado, total, subsidio, facturas)
                df,nombre = apoyo_reporte_comercial_sector_consumo(df1, n1, df2, n2, informar)
                if nombre:
                    lista_df_filiales.append(df)
                    nombre_compilado = nombre
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales)
            lista_nombre = nombre_compilado.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            if total:
                df_total_suma, proceso = generar_sumatoria_df(df_total, subsidio, codigo_DANE)
                if proceso:
                    df_total = df_total_suma.copy()
                    nuevo_nombre = nuevo_nombre.replace(".csv","_sumatoria.csv")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel)

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

def union_archivos_mensuales_anual_reporte_consumo(dic_archivos, seleccionar_reporte, informar, almacenar_excel=True, subsidio=True):
    v_fecha_siguiente = fecha_siguiente(seleccionar_reporte["fecha_personalizada"][0][0],seleccionar_reporte["fecha_personalizada"][0][1])
    v_fecha_anterior = fecha_anterior(seleccionar_reporte["fecha_personalizada"][1][0],seleccionar_reporte["fecha_personalizada"][1][1])
    lista_anual = []
    lista_df_anual_dif = []
    for fecha, lista_archivos in dic_archivos.items():
        for archivo in lista_archivos:
            df = leer_dataframe_utf_8(archivo)
            nombre = archivo
            if len(df):
                lista_anual.append(df)
    if subsidio:
        fecha_nombre = (seleccionar_reporte["fecha_personalizada"][0][0]+"_"+seleccionar_reporte["fecha_personalizada"][0][1].upper()
                    +"_"+seleccionar_reporte["fecha_personalizada"][1][0]+"_"+seleccionar_reporte["fecha_personalizada"][1][1].upper())
        if len(lista_anual) == 12:
            lista_df_anual_dif = lista_anual.copy()
        else:
            lista_df_anual_dif = lista_anual[1:]
    else:
        fecha_nombre = (v_fecha_siguiente[0]+"_"+v_fecha_siguiente[1].upper()
                    +"_"+seleccionar_reporte["fecha_personalizada"][1][0]+"_"+seleccionar_reporte["fecha_personalizada"][1][1].upper())
        if len(seleccionar_reporte["filial"]) == 4:
            for i in range(1,len(lista_anual)):
                df = lista_anual[i]
                df_actual = diferencia_columnas_dataframe(lista_anual[i], lista_anual[i-1])
                lista_df_anual_dif.append(df_actual)
        else:
            if len(lista_anual) == 12:
                lista_df_anual_dif = lista_anual.copy()
            else:
                lista_df_anual_dif = lista_anual.copy()[1:]
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
            almacenar_df_csv_y_excel(df_anual, nombre, informar, almacenar_excel)
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
            almacenar_df_csv_y_excel(df_anual, nombre, informar, almacenar_excel)
            return None
    else:
        return None

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

def reporte_comparacion_prd_cld_cer(dic_archivos, seleccionar_reporte, informar):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                if len(lista_archivos_filial) > 1:
                    apoyo_reporte_comparacion_prd_cld_cer(lista_archivos_filial, informar, filial)
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

def reporte_comparacion_SAP(dic_archivos, seleccionar_reporte, informar, cantidad_filas, p1, p2):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                if len(lista_archivos_filial) > 1:
                    apoyo_reporte_comparacion_p1_p2(lista_archivos_filial, informar, cantidad_filas, p1, p2) #Colocar SIEMPRE primero GRC1, PRD / GRC1, PRD / PRD, CLD
                else:
                    print(f"Se necesitan al menos 2 archivos para generar la comparación entre reportes comerciales GRC1")

def generar_sumatoria_df(df, subsidio, codigo_DANE):
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

def apoyo_reporte_usuarios_filial(lista_archivos,informar,filial,almacenar_excel=True, usuarios_unicos=True):
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
        if usuarios_unicos:
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
            almacenar_df_csv_y_excel(df_NIU_GRTT2_GRC1, nombre.replace("_resumen","_inventario_suscriptores_activos"), almacenar_excel=False)
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
        almacenar_df_csv_y_excel(df_filial_resumen, nombre)
        return df_filial_resumen, nombre
    else:
        return None,None

def reporte_usuarios_filial(dic_archivos, seleccionar_reporte, informar, almacenar_excel=True, usuarios_unicos=True):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df1,nombre = apoyo_reporte_usuarios_filial(lista_archivos_filial,informar,filial, usuarios_unicos=usuarios_unicos)
                if nombre:
                    lista_df_filiales.append(df1)
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

def apoyo_generar_reporte_compensacion_mensual(lista_archivos,informar,filial,inventario):
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
                almacenar_df_csv_y_excel(df1, nombre.replace("_resumen","_compilado_compensacion"))
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
                    almacenar_df_csv_y_excel(df_compensacion_info, nombre.replace("_resumen","_reporte_compensacion"))
    return df1, nombre

def generar_reporte_compensacion_mensual(dic_archivos, seleccionar_reporte, informar=True, inventario=False):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df1,nombre = apoyo_generar_reporte_compensacion_mensual(lista_archivos_filial,informar,filial,inventario)
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
            almacenar_df_csv_y_excel(df_total_compilado,nuevo_nombre, informar)

def apoyo_reporte_usuarios_unicos_mensual(lista_archivos, informar, filial, almacenar_excel=True):
    proceso_GRC1 = False
    proceso_GRC2 = False
    proceso_GRTT2 = False
    nombre_1 = None
    nombre_2 = None
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    lista_archivos_exitosos = []
    for archivo in lista_archivos:
        if "GRC1" in archivo:
            lista_df = lectura_dataframe_chunk(archivo)
            if lista_df:
                proceso_GRC1 = True
                nombre_GRC1 = archivo
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
                nombre_GRC2 = archivo
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
    if proceso_GRC1:
        nombre_arc = nombre_GRC1
    else:
        nombre_arc = nombre_GRC2
    if len(df1):
        lista_nombre = nombre_arc.split("\\")
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
        lista_nombre = nombre_arc.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        nombre_1 = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_reporte_facturacion")
        almacenar_df_csv_y_excel(df2, nombre_1)
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
        lista_nombre = nombre_arc.split("\\")
        lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
        nombre_2 = lista_a_texto(lista_nombre,"\\",False).replace("_resumen","_usuarios_unicos")
        almacenar_df_csv_y_excel(df, nombre_2)
    return df, nombre_2, df2, nombre_1

def reporte_usuarios_unicos_mensual(dic_archivos, seleccionar_reporte, informar, almacenar_excel=True):
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
                df1,nombre_1,df2,nombre_2 = apoyo_reporte_usuarios_unicos_mensual(lista_archivos_filial,informar,filial, almacenar_excel)
                if nombre_1:
                    lista_df_filiales_1.append(df1)
                if nombre_2:
                    lista_df_filiales_2.append(df2)
        if len(lista_df_filiales_2) > 0 and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales_2, ignore_index=True)
            df_total = generar_suma_df_filiales(df_total, ["Clasificacion_usuarios","Sector_consumo"],["Cantidad_facturas_emitidas","Consumo_m3",
                                                            "Valor_consumo_facturado","Valor_total_facturado"])
            lista_nombre = nombre_2.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre)
        if len(lista_df_filiales_1) > 0 and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales_1, ignore_index=True)
            df_total = generar_suma_df_filiales(df_total,["Clasificacion_usuarios"],["Cantidad_facturas_emitidas",
                                                            "Consumo_m3","Valor_consumo_facturado","Valor_total_facturado", "Cantidad_usuarios_unicos"])
            lista_nombre = nombre_1.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[1:],"_")
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre)

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
            almacenar_df_csv_y_excel(df_total,nuevo_nombre)
            return nuevo_nombre
        else:
            print(f"No es posible acceder al archivo {archivo}.")
            return None
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

def reporte_info_reclamos(fi,ff,listas_unidas, dashboard=False, texto_fecha=None):
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
            if not dashboard:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_reclamos_facturacion_10000_{f_inicial[0]}_{f_inicial[1]}_{f_final[0]}_{f_final[1]}")
                almacenar_df_csv_y_excel(df_total,nuevo_nombre)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_reclamos_facturacion_10000")
                almacenar_df_csv_y_excel(df_total,nuevo_nombre)
                return nuevo_nombre
        else:
            print(f"No es posible acceder al archivo {archivo}.")
            return None,None
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None,None

def generar_porcentaje_matriz_requerimientos(dashboard=False, texto_fecha=None):
    nombre = "Matriz requerimientos"
    hoja = "BD"
    archivo = ruta_constantes+"\\"+f"{nombre}.xlsm"
    anio_actual = fecha_actual.year
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
                print(f"Algunas de las columnas {texto} no se encunetran en el archivo.")
                return None
            df['fecha_de_recibido'] = pd.to_datetime(df['fecha_de_recibido'], dayfirst=True)
            df_filtrado = df[df['fecha_de_recibido'].dt.year == anio_actual]
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
                dic["Anio"].append(anio_actual)
            df = pd.DataFrame(dic)
            if not dashboard:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_matriz_requerimientos")
                almacenar_df_csv_y_excel(df,nuevo_nombre)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_matriz_requerimientos")
                almacenar_df_csv_y_excel(df,nuevo_nombre)
                return nuevo_nombre
        else:
            print(f"No es posible acceder al archivo {archivo}.")
            return None
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

def gastos_AOM(dashboard=False, texto_fecha=None):
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
                almacenar_df_csv_y_excel(df_AOM,nuevo_nombre)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"Gastos_AOM")
                almacenar_df_csv_y_excel(df_AOM,nuevo_nombre)
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
                almacenar_df_csv_y_excel(df, ruta_constantes+"\\"+f"{nombre}.csv", almacenar_excel=False)
                gastos_AOM()
            else:
                print(f"No es posible a acceder al archivo {archivo}.")
                return None
        else:
            print(f"No existe un hoja {hoja} en el archivo {nombre}.xlsx")
            return None
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

def reporte_tarifas_mensual(dic_archivos, seleccionar_reporte, informar=True, almacenar_excel=True):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df,nombre = apoyo_reporte_tarifas_mensual(lista_archivos_filial,informar,filial)
                if nombre:
                    lista_df_filiales.append(df)
        if len(lista_df_filiales) > 0 and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales, ignore_index=True)
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            df_total.to_csv(nuevo_nombre, index=False, encoding="utf-8-sig")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel)

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

def generar_reporte_indicadores_tecnicos_mensual(dic_archivos, seleccionar_reporte, informar=True,almacenar_excel=True):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df,nombre = apoyo_generar_reporte_indicadores_tecnicos_mensual(lista_archivos_filial,informar,filial)
                if nombre:
                    lista_df_filiales.append(df)
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales, ignore_index=True)
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_")
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\")
            almacenar_df_csv_y_excel(df_total, nuevo_nombre, informar, almacenar_excel)

def diferencia_minutos_fechas(df, lista_dia_1, lista_hora_1, lista_dia_2, lista_hora_2):
    lista_dif_minutos = []
    for i in range(len(lista_dia_1)):
        try:
            fecha_1 = datetime.strptime(str(lista_dia_1[i])+" "+str(lista_hora_1[i]), '%d-%m-%Y %H:%M')
            fecha_2 = datetime.strptime(str(lista_dia_2[i])+" "+str(lista_hora_2[i]), '%d-%m-%Y %H:%M')
            diferencia = float(round((fecha_2-fecha_1).total_seconds() / 60))
        except Exception:
            try:
                fecha_1 = datetime.strptime(str(lista_dia_1[i])+" "+str(lista_hora_1[i]), '%d/%m/%Y %H:%M')
                fecha_2 = datetime.strptime(str(lista_dia_2[i])+" "+str(lista_hora_2[i]), '%d/%m/%Y %H:%M')
                diferencia = float(round((fecha_2-fecha_1).total_seconds() / 60))
            except Exception:
                diferencia = float("inf")
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

def apoyo_generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos, filial, informar=True, almacenar_excel=True):
    for archivo in lista_archivos:
        df = leer_dataframe_utf_8(archivo)
        anio_archivo = df["Anio_reportado"][0]
        mes_archivo = df["Mes_reportado"][0]
        df['Observaciones'] = df['Observaciones'].str.replace("CONTROLADA", "CONTROLADO").astype(str)
        df['Observaciones'] = np.where(df['Observaciones'].str.contains('NO CONTR', case=False), 'NO CONTROLADO', df['Observaciones'])
        df['Observaciones'] = df['Observaciones'].str.strip().astype(str)
        df = diferencia_minutos_fechas(df, list(df["Fecha_solicitud"]), list(df["Hora_solicitud"]), list(df["Fecha_llegada_servicio_tecnico"]), list(df["Hora_llegada_servicio_tecnico"]))
        df['Hora_solicitud'] = df['Hora_solicitud'].str.split(':').str[0].astype(int)
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
        almacenar_df_csv_y_excel(df2, nombre_1, informar, almacenar_excel)
        df1 = pd.DataFrame(dic_df_evento)
        df1 = porcentaje_tipo_evento(df1)
        df1["Filial"] = dic_filiales[filial]
        df1["NIT"] = dic_nit[dic_filiales[filial]]
        df1["Anio_reportado"] = anio_archivo
        df1["Mes_reportado"] = mes_archivo
        almacenar_df_csv_y_excel(df1, nombre, informar, almacenar_excel)
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
        almacenar_df_csv_y_excel(df3, nombre_2, informar, almacenar_excel)
        return df1, nombre, df2, nombre_1, df3, nombre_2

def generar_reporte_indicadores_tecnicos_IRST_mensual(dic_archivos, seleccionar_reporte, informar=True,almacenar_excel=True):
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
                df1,nombre_1,df2,nombre_2,df3,nombre_3 = apoyo_generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos_filial,filial, informar, almacenar_excel)
                if nombre_1:
                    lista_df_filiales_1.append(df1)
                if nombre_2:
                    lista_df_filiales_2.append(df2)
                if nombre_3:
                    lista_df_filiales_3.append(df3)
        if len(lista_df_filiales_1) and len(lista_filiales_archivo) == 4:
            df_total, nuevo_nombre = generar_formato_almacenamiento_reportes(lista_df_filiales_1, nombre_1, informar,almacenar_excel)
        if len(lista_df_filiales_2) and len(lista_filiales_archivo) == 4:
            df_total_2, nuevo_nombre_2 = generar_formato_almacenamiento_reportes(lista_df_filiales_2, nombre_2, informar,almacenar_excel)
        if len(lista_df_filiales_3) and len(lista_filiales_archivo) == 4:
            df_total_3, nuevo_nombre_3 = generar_formato_almacenamiento_reportes(lista_df_filiales_3, nombre_3, informar,almacenar_excel)

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
                nombre = archivo.replace("_resumen.csv","_reporte_suspension.csv")
                almacenar_df_csv_y_excel(df1, nombre)
            return df1, nombre
        else:
            return None, None
    return None, None

def generar_reporte_suspension_mensual(dic_archivos, seleccionar_reporte, informar=True, almacenar_excel=True):
    lista_filiales_archivo = seleccionar_reporte["filial"]
    for fecha, lista_archivos in dic_archivos.items():
        lista_df_filiales = []
        for filial in lista_filiales_archivo:
            lista_archivos_filial = []
            for archivo in lista_archivos:
                if filial in archivo:
                    lista_archivos_filial.append(archivo)
            if len(lista_archivos_filial):
                df,nombre = apoyo_generar_reporte_suspension_mensual(lista_archivos_filial,informar,filial)
            if nombre:
                lista_df_filiales.append(df)
        if len(lista_df_filiales) and len(lista_filiales_archivo) == 4:
            df_total = pd.concat(lista_df_filiales, ignore_index=True)
            lista_nombre = nombre.split("\\")
            lista_nombre[-1] = lista_a_texto(lista_nombre[-1].split("_")[2:],"_",False)
            lista_nombre[-5] = "05. REPORTES_GENERADOS_APLICATIVO"
            lista_nombre.pop(-2)
            nuevo_nombre = lista_a_texto(lista_nombre,"\\",False)
            almacenar_df_csv_y_excel(df_total, nuevo_nombre)

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

def generar_porcentaje_cumplimientos_regulatorios(dashboard=False, texto_fecha=None):
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
            if not dashboard:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", str(anio_actual), "REPORTES_GENERADOS_APLICATIVO", "Compilado", "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, "porcentaje_cumplimientos_regulatorios")
                almacenar_df_csv_y_excel(df_porcentaje,nuevo_nombre)
                return nuevo_nombre
            else:
                lista_ubi = [ruta_nuevo_sui, "Reportes Nuevo SUI", "Compilado", "REPORTES_GENERADOS_APLICATIVO", "Compilado", texto_fecha, "Cumplimientos_Regulatorios"]
                nuevo_nombre = encontrar_ubi_archivo(lista_ubi, f"porcentaje_cumplimientos_regulatorios")
                almacenar_df_csv_y_excel(df_porcentaje,nuevo_nombre)
                return nuevo_nombre
        else:
            print(f"No es posible acceder al archivo {archivo}.")
            return None
    else:
        print(f"No existe el archivo {archivo}. No es posible generar el reporte.")
        return None

# * -------------------------------------------------------------------------------------------------------
# *                                             Reportes Anuales
# * -------------------------------------------------------------------------------------------------------

def union_archivos_mensuales_anual(dic_archivos, seleccionar_reporte, informar=True, almacenar_excel=True):
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
        ext_nombre.pop(0)
        ext_nombre[0] = fecha_nombre
        lista_nombre[-1] = lista_a_texto(ext_nombre, "_")
        crear_carpeta_anual(fecha_nombre, lista_nombre)
        lista_nombre.insert(-2, fecha_nombre)
        nombre = lista_a_texto(lista_nombre, "\\")
        df_anual = pd.concat(lista_anual)
        almacenar_df_csv_y_excel(df_anual, nombre, informar, almacenar_excel)
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
def busqueda_archivos_tipo(ubi_archivo,tipo=None, lista_fallidos=[]):
    if tipo:
        archivos_tipo = glob.glob(os.path.join(ubi_archivo, "*"+tipo))
    else:
        archivos_tipo = glob.glob(os.path.join(ubi_archivo, "*"))
    return archivos_tipo

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
