import os
import sys
import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
import modulo as mod_1
import archivo_creacion_json as mod_2
global version, lista_meses, lista_anios, dic_reportes, lista_reportes_generales, reportes_generados
version = "1.0"
lista = []
lista_anios = list(mod_2.leer_archivos_json(ruta_constantes+"anios.json")["datos"].values())
lista_meses = list(mod_2.leer_archivos_json(ruta_constantes+"tabla_18.json")["datos"].values())
lista_filiales = list(mod_2.leer_archivos_json(ruta_constantes+"tabla_empresa.json")["datos"].keys())
dic_reportes = mod_2.leer_archivos_json(ruta_constantes+"carpetas.json")["carpeta_6"]
lista_reportes_generales = mod_2.leer_archivos_json(ruta_constantes+"carpetas_1.json")["carpeta_2"]
reportes_generados = mod_2.leer_archivos_json(ruta_constantes+"carpetas_1.json")["carpeta_4"]

def busqueda_archivos_lista_ubicaciones(lista_archivos, lista_busqueda, tipo):
    for carpeta in lista_busqueda:
        lista_archivos.extend(mod_1.busqueda_archivos_tipo(carpeta,tipo))
    return lista_archivos

def lista_a_texto(lista, separador, salto=False):
    lista = [str(elemento) for elemento in lista]
    texto = separador.join(lista)
    if salto:
        texto += "\n"
    return texto

def tamanio_archivos(archivo):
    try:
        file_size_bytes = os.path.getsize(archivo)
        suma_B = float(round(file_size_bytes,2))
        suma_KB = float(round(suma_B/1024,2))
        suma_MB = float(round(suma_KB/1024,2))
        suma_GB = float(round(suma_MB/1024,2))
        if suma_GB > 1:
            texto = f" ({round(suma_GB,2)}) GB"
        elif suma_KB < 0.1:
            texto = f" ({round(suma_B,2)}) B"
        elif suma_MB < 0.1:
            texto = f" ({round(suma_KB,2)}) KB"
        else:
            texto = f" ({round(suma_MB,2)}) MB"
        return texto
    except FileNotFoundError:
        return ""
    except PermissionError:
        return ""


def formato_nombre(nombre):
    nombre = nombre.replace("\\\\","\\")
    lista_nombre = nombre.split("\\")[-1]
    largo = 80
    v_tamanio_archivos = tamanio_archivos(nombre)
    sepa = largo - len(lista_nombre)- len(v_tamanio_archivos)
    sepa = " "*sepa
    texto = f"{lista_nombre}{sepa}{tamanio_archivos(nombre)}"
    return texto

def encontrar_meses(tipo, mes_1, mes_2):
    ubi_mes = lista_meses.index(mes_1)
    if tipo == "inicio":
        lista_meses_aux = lista_meses[:ubi_mes+1]
        return lista_meses_aux
    elif tipo == "fin":
        lista_meses_aux = lista_meses[ubi_mes:]
        return lista_meses_aux
    elif tipo == "personalizado":
        ubi_mes_2 = lista_meses.index(mes_2)
        lista_meses_aux = lista_meses[ubi_mes:ubi_mes_2+1]
        return lista_meses_aux

def cambiar_formato_fecha_seleccionar_reporte(seleccionar_reporte):
    lista_fechas = []
    fecha_1 = seleccionar_reporte["fecha_personalizada"][0]
    fecha_2 = seleccionar_reporte["fecha_personalizada"][1]
    if fecha_1 == fecha_2:
        lista_fechas.append(fecha_1)
        return lista_fechas, [fecha_1[0]]
    elif fecha_1[0] == fecha_2[0]:
        lista_anios_1 =[fecha_1[0]]
        lista_meses_1 = encontrar_meses("personalizado", fecha_1[1], fecha_2[1])
        listas_unidas = mod_1.unir_listas_formato(lista_anios_1, lista_meses_1)
        return listas_unidas, lista_anios_1
    else:
        listas_unidas = []
        lista_anios_1 = mod_1.elementos_lista_a_str(list(range(int(fecha_1[0]), int(fecha_2[0])+1)))
        lista_meses_2 = encontrar_meses("inicio", fecha_2[1], None)
        lista_meses_1 = encontrar_meses("fin", fecha_1[1], None)
        largo = len(lista_anios_1)
        for i in range(largo):
            if i == 0:
                listas_unidas.extend(mod_1.unir_listas_formato([lista_anios_1[i]], lista_meses_1))
            elif i == largo-1:
                listas_unidas.extend(mod_1.unir_listas_formato([lista_anios_1[i]], lista_meses_2))
            else:
                listas_unidas.extend(mod_1.unir_listas_formato([lista_anios_1[i]], lista_meses))
        return listas_unidas, lista_anios

def aplicar_evitar(lista_archivos, evitar):
    if len(evitar) > 0:
        lista_1 = lista_archivos.copy()
        for archivo in lista_archivos:
            l_archivo = archivo.split("\\")
            for elemento in evitar:
                valor = elemento in l_archivo[-1]
                if valor:
                    try:
                        lista_1.remove(archivo)
                    except ValueError:
                        pass
        return lista_1
    else:
        return lista_archivos

def agrupar_dic_archivos(dic_archivos):
    dic_archivos_agrupados = {}
    for llave, valor in dic_archivos.items():
        dic_archivos_agrupados[llave] = []
        for filial, lista_archivos_filial in valor.items():
            dic_archivos_agrupados[llave].extend(lista_archivos_filial)
    return dic_archivos_agrupados

def agrupar_archivos(seleccionar_reporte, lista_archivos):
    dic_archivos = {}
    dic_archivos_tamanio = {}
    dic_archivos_3 = {}
    if seleccionar_reporte["fecha_personalizada"]:
        lista_fechas, lista_fechas_anios = cambiar_formato_fecha_seleccionar_reporte(seleccionar_reporte)
        for elemento in lista_fechas:
            anio = elemento[0]
            mes = elemento[1]
            fecha = anio+" - "+mes
            dic_archivos[fecha] = {}
            dic_archivos_tamanio[fecha] = {}
            for llave in seleccionar_reporte:
                if llave not in ["ubicacion","anios","meses"]:
                    if llave == "filial":
                        for filial in seleccionar_reporte["filial"]:
                            dic_archivos[fecha][filial] = []
                            dic_archivos_tamanio[fecha][filial] = []
                            for archivo in lista_archivos:
                                if anio in archivo and mes in archivo and filial in archivo:
                                    dic_archivos[fecha][filial].append(archivo)
                                    dic_archivos_tamanio[fecha][filial].append(formato_nombre(archivo))
    else:
        anio = seleccionar_reporte["anios"][0]
        mes = seleccionar_reporte["meses"][0]
        fecha = anio+" - "+mes
        dic_archivos[fecha] = {}
        dic_archivos_tamanio[fecha] = {}
        for llave in seleccionar_reporte:
            if llave not in ["ubicacion","anios","meses"]:
                if llave == "filial":
                    for filial in seleccionar_reporte["filial"]:
                        dic_archivos[fecha][filial] = []
                        dic_archivos_tamanio[fecha][filial] = []
                        for archivo in lista_archivos:
                            if anio in archivo and mes in archivo and filial in archivo:
                                dic_archivos[fecha][filial].append(archivo)
                                dic_archivos_tamanio[fecha][filial].append(formato_nombre(archivo))
    if len(dic_archivos) > 0:
        for llave, valor in dic_archivos_tamanio.items():
            dic_archivos_3[llave] = {}
            for filial, lista_archivos_filial in valor.items():
                dic_archivos_3[llave][filial] = []
                for i in range(0, len(lista_archivos_filial), 2):
                    elementos = lista_archivos_filial[i:i+2]
                    dic_archivos_3[llave][filial].append(lista_a_texto(elementos,",    "))
        return True, dic_archivos,dic_archivos_3
    else:
        return False, False, False

def agrupar_archivos_anual(seleccionar_reporte, lista_archivos):
    dic_archivos = {}
    dic_archivos_tamanio = {}
    dic_archivos_3 = {}
    lista_fechas, lista_fechas_anios = cambiar_formato_fecha_seleccionar_reporte(seleccionar_reporte)
    for elemento in lista_fechas:
        anio = elemento[0]
        mes = elemento[1]
        fecha = anio+" - "+mes
        dic_archivos[fecha] = []
        dic_archivos_tamanio[fecha] = []
        for archivo in lista_archivos:
            if anio in archivo and mes in archivo:
                dic_archivos[fecha].append(archivo)
                dic_archivos_tamanio[fecha].append(formato_nombre(archivo))
    if len(dic_archivos) > 0:
        for llave, valor in dic_archivos_tamanio.items():
            dic_archivos_3[llave] = []
            for i in range(0, len(valor), 2):
                elementos = valor[i:i+2]
                dic_archivos_3[llave].append(lista_a_texto(elementos,",    "))
        return True, dic_archivos,dic_archivos_3
    else:
        return False, False, False

def encontrar_archivos_seleccionar_reporte(seleccionar_reporte,tipo, evitar):
    lista_archivos = []
    if seleccionar_reporte["fecha_personalizada"]:
        lista_fechas, lista_fechas_anios = cambiar_formato_fecha_seleccionar_reporte(seleccionar_reporte)
        for llave in seleccionar_reporte:
            if llave != "fecha_personalizada":
                if llave == "ubicacion":
                    lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas([ruta_nuevo_sui])
                else:
                    lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas(lista_ubicaciones)
                if llave == "anios":
                    lista_ubicaciones = mod_1.filtrar_carpetas(lista_ubicaciones, lista_fechas_anios)
                elif llave == "meses":
                    lista_ubicaciones = mod_1.filtrar_carpetas_mes_anio(lista_ubicaciones, lista_fechas)
                else:
                    lista_ubicaciones = mod_1.filtrar_carpetas(lista_ubicaciones, seleccionar_reporte[llave])
                lista_archivos = busqueda_archivos_lista_ubicaciones(lista_archivos, lista_ubicaciones, tipo)
        lista_1 = aplicar_evitar(lista_archivos, evitar)
        return lista_1
    else:
        for llave in seleccionar_reporte:
            if seleccionar_reporte[llave]:
                if llave == "ubicacion":
                    lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas([ruta_nuevo_sui])
                else:
                    lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas(lista_ubicaciones)
                lista_ubicaciones = mod_1.filtrar_carpetas(lista_ubicaciones, seleccionar_reporte[llave])
                lista_archivos = busqueda_archivos_lista_ubicaciones(lista_archivos, lista_ubicaciones, tipo)
        lista_1 = aplicar_evitar(lista_archivos, evitar)
        return lista_1

def encontrar_archivos_seleccionar_reporte_anual(seleccionar_reporte,tipo, evitar):
    lista_archivos = []
    lista_fechas, lista_fechas_anios = cambiar_formato_fecha_seleccionar_reporte(seleccionar_reporte)
    for llave in seleccionar_reporte:
        if llave != "fecha_personalizada":
            if llave == "ubicacion":
                lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas([ruta_nuevo_sui])
            else:
                lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas(lista_ubicaciones)
            if llave == "anios":
                lista_ubicaciones = mod_1.filtrar_carpetas(lista_ubicaciones, lista_fechas_anios)
            elif llave == "meses":
                lista_ubicaciones = mod_1.filtrar_carpetas_mes_anio(lista_ubicaciones, lista_fechas)
            else:
                lista_ubicaciones = mod_1.filtrar_carpetas(lista_ubicaciones, seleccionar_reporte[llave])
            lista_archivos = busqueda_archivos_lista_ubicaciones(lista_archivos, lista_ubicaciones, tipo)
    lista_1 = aplicar_evitar(lista_archivos, evitar)
    return lista_1

def apoyo_archivos_esperados(lista_ubicaciones,tipo):
    for i in range(len(lista_ubicaciones)):
        ubicacion = lista_ubicaciones[i]
        lista_ubicacion = ubicacion.split("\\")
        texto = lista_ubicacion[-1][4:]+"_"+lista_ubicacion[-4][4:]+"_"+lista_ubicacion[-5][4:]+"_"+lista_ubicacion[-3][4:].upper()+tipo
        lista_ubicaciones[i] += "\\"+texto
    return lista_ubicaciones

def archivos_esperados(seleccionar_reporte, tipo):
    lista_archivos_esperados = []
    lista_fechas = []
    lista_fechas_anios = []
    if seleccionar_reporte["fecha_personalizada"]:
        lista_fechas, lista_fechas_anios = cambiar_formato_fecha_seleccionar_reporte(seleccionar_reporte)
        for llave in seleccionar_reporte:
            if llave != "fecha_personalizada":
                if llave == "ubicacion":
                    lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas([ruta_nuevo_sui])
                else:
                    lista_ubicaciones = mod_1.buscar_carpetas_lista_carpetas(lista_ubicaciones)
                if llave == "anios":
                    lista_ubicaciones = mod_1.filtrar_carpetas(lista_ubicaciones, lista_fechas_anios)
                elif llave == "meses":
                    lista_ubicaciones = mod_1.filtrar_carpetas_mes_anio(lista_ubicaciones, lista_fechas)
                else:
                    lista_ubicaciones = mod_1.filtrar_carpetas(lista_ubicaciones, seleccionar_reporte[llave])
        lista_archivos_esperados = apoyo_archivos_esperados(lista_ubicaciones,tipo)
    return lista_archivos_esperados,lista_fechas,lista_fechas_anios

def todos_los_archivos(lista_archivos_esperados, lista_archivos):
    lista_no_encontrados = lista_archivos_esperados.copy()
    for i in range(len(lista_archivos)):
        if lista_archivos[i] in lista_archivos_esperados:
            lista_no_encontrados.remove(lista_archivos[i])
    return lista_no_encontrados