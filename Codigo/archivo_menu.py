import os
import sys
import time
import subprocess
import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos, ruta_guardar_archivos
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
ruta_guardar_archivos = mod_rp.v_guardar_archivos()
sys.path.append(os.path.abspath(ruta_codigo))
import modulo as mod_1
import archivo_creacion_json as mod_2
import archivo_crear_carpetas as mod_3
import archivo_busqueda_reportes as mod_4

# * -------------------------------------------------------------------------------------------------------
# *                                             Constantes globales
# * -------------------------------------------------------------------------------------------------------
global version, lista_meses, lista_empresas,lista_anios,dic_reportes,lista_reportes_generales,reportes_generados,lista_reportes_totales,t_i,t_f,lista_reportes_generados,cantidad_datos_estilo_excel
version = "1.0"
lista_anios = list(mod_2.leer_archivos_json(ruta_constantes+"anios.json")["datos"].values())
lista_meses = list(mod_2.leer_archivos_json(ruta_constantes+"tabla_18.json")["datos"].values())
lista_trimestres = list(mod_2.leer_archivos_json(ruta_constantes+"trimestres.json")["datos"].values())
lista_filiales = list(mod_2.leer_archivos_json(ruta_constantes+"tabla_empresa.json")["datos"].keys())
dic_reportes = mod_2.leer_archivos_json(ruta_constantes+"carpetas.json")["carpeta_6"]
lista_reportes_generales = mod_2.leer_archivos_json(ruta_constantes+"carpetas_1.json")["carpeta_2"]
reportes_generados = mod_2.leer_archivos_json(ruta_constantes+"carpetas_1.json")["carpeta_4"]
lista_reportes_generados = ["_resumen","_form_estandar", #formatos generales
                            "_reporte_consumo","_CLD","_PRD","_porcentaje_comparacion_SAP","_total_comparacion_SAP",
                            "_comparacion_iguales","_comparacion_diferentes","_subsidio","_info_comercial","_reporte_compensacion","_compilado_compensacion", #formatos comerciales
                            "_reporte_tarifario", #formatos tarifarios
                            "_indicador_tecnico","_reporte_suspension", #formatos tecnicos
                            "_inventario_suscriptores","_usuarios_unicos","_reporte_facturacion",#calidad de la información
                            "porcentaje_cumplimientos_regulatorios"] #formatos regulatorios
cantidad_datos_estilo_excel = 80000

def crear_lista_reportes_totales():
    dic = mod_2.leer_archivos_json(ruta_constantes+"/reportes_disponibles.json")["datos"]
    lista = []
    for i in dic:
        lista.extend(dic[i])
    return lista
lista_reportes_totales = crear_lista_reportes_totales()

# * -------------------------------------------------------------------------------------------------------
# *                                             Procesamiento de opciones de menú
# * -------------------------------------------------------------------------------------------------------
def reodenar_lista(lista):
    n_lista = []
    l1 = []
    l2 = []
    for i in range(0,len(lista),2):
        n_lista.append(lista[i])
        l1.append(lista[i])
    for i in range(1,len(lista),2):
        n_lista.append(lista[i])
        l2.append(lista[i])
    return n_lista,l1,l2


def lista_opciones_menu(lista, separacion):
    dic_menu = {}
    largo = len(lista)
    if not separacion:
        for i in range(largo):
            if i+1 < 10:
                elemento = str(i+1)+".  "+lista[i]
            else:
                elemento = str(i+1)+". "+lista[i]
            print(elemento)
            dic_menu[str(i+1)] = lista[i]
    else:
        lista,l1,l2 = reodenar_lista(lista)
        for i in range(largo):
            elemento = str(i+1)+". "+lista[i]
            dic_menu[str(i+1)] = lista[i]
        n = 30
        largo_1 = len(l1)
        largo_2 = len(l2)
        for i in range(largo_1):
            if i < largo_1 and i < largo_2:
                if i+1 < 10:
                    t1 = str(i+1)+".  "+l1[i]
                    t2 = str(i+13)+". "+l2[i]
                else:
                    t1 = str(i+1)+". "+l1[i]
                    t2 = str(i+13)+". "+l2[i]
                print(t1+" "*(n-len(t1))+t2)
            elif i < largo_1:
                if i+1 < 10:
                    t1 = str(i+1)+".  "+l1[i]
                else:
                    t1 = str(i+1)+". "+l2[i]
                print(t1)
    return dic_menu

def comprobar_opcion_lista_menu(lista, opcion):
    if opcion in lista:
        return True
    else:
        return False

def confirmacion_seleccion(lista, texto=None):
    centinela = True
    while centinela:
        if texto:
            print(texto)
        else:
            print("\n¿Desea continuar?")
        dic_menu = lista_opciones_menu(lista,False)
        option = str(input("Ingrese la opción a seleccionar: "))
        rta = comprobar_opcion_lista_menu(dic_menu, option)
        if rta:
            print(f"Opción \'{option}. {dic_menu[option]}\' seleccionada\n")
            return option,dic_menu[option]
        else:
            print("\nOpción no válida. Intente de nuevo.\n")

def opcion_menu_valida(lista, nombre, separacion=False):
    centinela = True
    while centinela:
        mod_1.mostrar_titulo(f"Menú de opciones: {nombre}", True, None)
        dic_menu = lista_opciones_menu(lista,separacion)
        option = str(input("Ingrese la opción a seleccionar: "))
        rta = comprobar_opcion_lista_menu(dic_menu, option)
        if rta:
            print(f"\nOpción \'{option}. {dic_menu[option]}\' seleccionada\n")
            return option, dic_menu[option]
        else:
            print("\nOpción no válida. Intente de nuevo.\n")

# * -------------------------------------------------------------------------------------------------------
# *                                             Opciones adicionales
# * -------------------------------------------------------------------------------------------------------
def elegir_codigo_DANE():
    lista = ["Seleccionar un (1) Código DANE","Seleccionar más (>1) de un Código DANE","No seleccionar Código DANE"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, "Seleccionar Código DANE", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        centinela = True
        while centinela:
            try:
                codigo_DANE = int(input("\nIngresar el Código DANE a buscar: "))
                if len(str(codigo_DANE)) != 8:
                    print("El código DANE ingresado debe tener 8 dígitos")
                else:
                    print(f"\nCódigo DANE seleccionado: {codigo_DANE}\n")
                    centinela = False
            except ValueError:
                print("El código DANE ingresado no es válido")
            except TypeError:
                print("El código DANE ingresado no es válido")
        return [codigo_DANE]
    elif option == "2":
        codigo_DANE = str(input("\nIngresar los Código DANE a buscar separados por comas (,): ")).replace(" ","").replace(".","")
        lista_codigo_DANE = []
        for codigo in codigo_DANE.split(","):
            try:
                valor = int(codigo)
                if len(str(valor)) == 8:
                    lista_codigo_DANE.append(valor)
            except ValueError:
                pass
            except TypeError:
                pass
        if len(lista_codigo_DANE) > 0:
            texto = mod_1.lista_a_texto(lista_codigo_DANE,", ")
            print(f"\nCódigos DANE seleccionados: {texto}\n")
            return lista_codigo_DANE
        else:
            return None
    else:
        return None

def elegir_tiempo():
    lista = ["Sí","No"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, "Calcular tiempo de procesamiento", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        return True
    else:
        return False

def elegir_regenerar_archivos(texto):
    lista = ["Sí","No"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, f"Regenerar archivos necesarios ({texto})", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        return True
    else:
        return False

def elegir_regenerar_archivos_mensuales(texto):
    lista = ["Sí","No"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, f"Regenerar reportes necesarios mensuales ({texto})", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        return True
    else:
        return False

def elegir_valor_facturado():
    lista = ["Sí","No"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, "Incluir el valor total facturado", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        return True
    else:
        return False

def elegir_mostrar_archivos():
    lista = ["Sí","No"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, "Mostrar los archivos generados", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        return True
    else:
        return False

def elegir_cantidad_filas():
    lista = ["Sí","No"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, "Seleccionar una cantidad de filas mínimo", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        try:
            cantidad_filas = int(input("\nIngresar la cantidad de filas mínimo: "))
            if cantidad_filas > cantidad_datos_estilo_excel:
                print(f"\nCantidad de filas seleccionadas: {cantidad_datos_estilo_excel}\n")
                return cantidad_datos_estilo_excel
            else:
                print(f"\nCantidad de filas seleccionadas: {cantidad_filas}\n")
                return cantidad_filas
        except ValueError:
            return None
    else:
        return cantidad_datos_estilo_excel

def elegir_inventario():
    lista = ["Sí","No"]
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, f"Incluir información del inventario de suscriptores", False)
    if option == str(len(lista)):
        iniciar_menu()
    elif option == "1":
        return True
    else:
        return False

def anadir_opciones(regenerar=False, codigo_DANE=False, valor_facturado=False, cantidad_filas=False, mostrar_archivos=False, inventario=False,
                    calcular_tiempo=True, reportes_mensuales=False, texto_regenerar = "_form_estandar, _resumen", texto_regenerar_mensuales=""):
    if regenerar:
        regenerar = elegir_regenerar_archivos(texto_regenerar)
    if codigo_DANE:
        codigo_DANE = elegir_codigo_DANE()
    if valor_facturado:
        valor_facturado = elegir_valor_facturado()
    if cantidad_filas:
        cantidad_filas = elegir_cantidad_filas()
    if mostrar_archivos and regenerar:
        mostrar_archivos = elegir_mostrar_archivos()
    if not regenerar and reportes_mensuales:
        reportes_mensuales = elegir_regenerar_archivos_mensuales(texto_regenerar_mensuales)
    if (reportes_mensuales and inventario) or (reportes_mensuales == None and inventario):
        inventario = elegir_inventario()
    return (calcular_tiempo, regenerar, codigo_DANE, valor_facturado, cantidad_filas, mostrar_archivos, reportes_mensuales, inventario)

def especificar_lista_reportes_generados(lista_1):
    lista = lista_reportes_generados.copy()
    if len(lista_1):
        for i in lista_1:
            try:
                lista.remove(i)
            except ValueError:
                pass
    return lista

# * -------------------------------------------------------------------------------------------------------
# *                                             Menú de configuración inicial
# * -------------------------------------------------------------------------------------------------------

def menu_configuracion_inicial(option,valor):
    #? Creación de espacio de trabajo (Carpetas)
    if option == "1":
        lista_menu_1 = ["Sí","No"]
        option_1,valor_1 = confirmacion_seleccion(lista_menu_1)
        if option_1 == "1":
            t_i = time.time()
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_3.configuracion_inicial()
            mod_1.mostrar_texto("Configuración inicial completa.")
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Agregar un nuevo año
    elif option == "2":
        centinela = True
        while centinela:
            anio = input("Ingrese el nuevo año a almacenar: ")
            try:
                valor = int(anio)
                if valor > 2024:
                    centinela = False
                else:
                    print("\nEl año ingresado no es válido\n")
            except TypeError:
                print("\nEl año ingresado no es válido\n")
            except ValueError:
                print("\nEl año ingresado no es válido\n")
        lista_menu_1 = ["Sí","No"]
        option_1,valor_1 = confirmacion_seleccion(lista_menu_1, f"¿Desea ingresar el año {valor} a las carpetas de archivos?")
        if option_1 == "1":
            t_i = time.time()
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_2.cambiar_diccionario(str(valor))
            mod_3.configuracion_inicial()
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Editar un reporte existente
    elif option == "3":
        t_i = time.time()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)
    #? Agregar un nuevo tipo de reporte
        t_i = time.time()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)

# * -------------------------------------------------------------------------------------------------------
# *                                             Menú de edición de archivos
# * -------------------------------------------------------------------------------------------------------

def menu_opciones_archivos(option, valor):
    #? Conversión de archivos txt a csv
    if option == "1":
        tipo = ".txt"
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_general")
        option_1, valor_1 = opcion_menu_valida(["Conservar los archivos encontrados","Eliminar los archivos encontrados",
                                                "Regresar al menú inicial"], "Eliminar archivos txt", False)
        if option_1 == "1":
            eliminar = False
        elif option_1 == "2":
            eliminar = True
        opciones_adicionales = anadir_opciones(False, False)
        t_i = time.time()
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, [])
        lista_archivos.extend(mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo.upper(), []))
        if len(lista_archivos) == 0:
            print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
        else:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.conversion_archivos_lista(lista_archivos,"txt","csv")
            if eliminar:
                mod_1.eliminar_archivos(lista_archivos)
                print(f"\nArchivos con formato {tipo} eliminados\n")
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Almacenar archivos
    elif option == "2":
        t_i = time.time()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        mod_1.almacenar_archivos(ruta_guardar_archivos.replace('\\', '\\\\'),True)
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)
    #? Estandarización de archivos
    elif option == "3":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_vanti")
        opciones_adicionales = anadir_opciones()
        t_i = time.time()
        tipo = ".CSV"
        lista_evitar = especificar_lista_reportes_generados(["_CLD","_PRD"])
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
        mod_1.conversion_archivos_CSV(lista_archivos)
        tipo = ".csv"
        lista_evitar = especificar_lista_reportes_generados(["_CLD","_PRD"])
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
        if len(lista_archivos) == 0:
            print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
        else:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.estandarizacion_archivos(lista_archivos, True)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generar archivos de tipo resumen
    elif option == "4":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_vanti")
        opciones_adicionales = anadir_opciones(True)
        t_i = time.time()
        tipo = ".CSV"
        lista_evitar = especificar_lista_reportes_generados(["_CLD","_PRD"])
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        mod_1.conversion_archivos_CSV(lista_archivos)
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1],evitar_extra=["_CLD","_PRD"],solo_crear_arc=True)
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)
    #? Revisión de archivos existentes
    elif option == "5":
        t_i = time.time()
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_vanti")
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        busqueda_archivos_general(seleccionar_reporte)
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)

# * -------------------------------------------------------------------------------------------------------
# *                                             Activación de menú
# * -------------------------------------------------------------------------------------------------------

def comprimir_archivos(seleccionar_reporte, evitar_extra=["_CLD","_PRD"]):
    lista_archivos_comprimir = []
    tipo = ".csv"
    proceso, lista_archivos = busqueda_archivos_tipo(tipo, seleccionar_reporte,evitar_extra, informar=False)
    if proceso:
        lista_archivos_comprimir.extend(lista_archivos)
    tipo = "_form_estandar.csv"
    proceso, lista_archivos = busqueda_archivos_tipo(tipo, seleccionar_reporte,evitar_extra, informar=False)
    if proceso:
        lista_archivos_comprimir.extend(lista_archivos)
    tipo = ".txt"
    proceso, lista_archivos = busqueda_archivos_tipo(tipo, seleccionar_reporte,evitar_extra, txt=True, informar=False)
    if proceso:
        lista_archivos_comprimir.extend(lista_archivos)
    if len(lista_archivos_comprimir):
        mod_1.comprimir_archivos(lista_archivos_comprimir)

def generar_archivos_extra(seleccionar_reporte, regenerar=False, evitar_extra=[], continuar=False, informar=True, ext="_resumen.csv", solo_crear_arc=False, mostrar_dic=False):
    if regenerar:
        tipo = ".csv"
        proceso, lista_archivos = busqueda_archivos_tipo(tipo, seleccionar_reporte,evitar_extra, informar=informar)
        if proceso:
            mod_1.estandarizacion_archivos(lista_archivos,True)
            tipo = "_form_estandar.csv"
            proceso, lista_archivos = busqueda_archivos_tipo(tipo, seleccionar_reporte,evitar_extra, informar=informar)
            if proceso:
                mod_1.archivos_resumen(lista_archivos,True)
                tipo = "_resumen.csv"
                proceso, lista_archivos = busqueda_archivos_tipo(tipo, seleccionar_reporte,evitar_extra, informar=informar)
                comprimir_archivos(seleccionar_reporte, evitar_extra)
    if not solo_crear_arc:
        tipo = ext
        proceso_resumen, lista_archivos = busqueda_archivos_tipo(tipo, seleccionar_reporte, evitar_extra, informar=True)
        if proceso_resumen:
            proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos)
            if mostrar_dic:
                mostrar_dic_archivos_agrupados(proceso_agrupar, dic_archivos_mostrar)
            if continuar:
                option = "1"
            else:
                lista_menu = ["Sí","No"]
                option,valor = opcion_menu_valida(lista_menu, "¿Desea generar el reporte con los archivos disponibles?")
            if option == "1":
                dic_archivos_reporte = mod_4.agrupar_dic_archivos(dic_archivos)
                return True, dic_archivos_reporte
            else:
                return False, False
        return False, False
    else:
        return None, None

def busqueda_archivos_tipo(tipo, seleccionar_reporte, evitar_extra=[], txt=False, informar=True):
    tipo_evitar = tipo.replace(".csv","").replace(".CSV","").replace(".TXT","").replace(".txt","")
    lista_evitar_extra_copia = evitar_extra.copy()
    if len(tipo_evitar):
        lista_evitar_extra_copia.append(tipo_evitar)
    lista_evitar = especificar_lista_reportes_generados(lista_evitar_extra_copia)
    lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
    if len(lista_archivos) == 0:
        if informar:
            print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
        return False,lista_archivos
    else:
        return True,lista_archivos

def generar_archivos_extra_anual(seleccionar_reporte, tipo, evitar_extra=[], continuar=False, informar=True, mostrar_dic=True):
    list_of_tuples = list(seleccionar_reporte.items())
    list_of_tuples.insert(3, ('carpeta', ["REPORTES_GENERADOS_APLICATIVO"]))
    seleccionar_reporte_1 = dict(list_of_tuples)
    del seleccionar_reporte_1["clasificacion"]
    del seleccionar_reporte_1["filial"]
    proceso, lista_archivos = busqueda_archivos_tipo_anual(tipo, seleccionar_reporte_1, evitar_extra, informar)
    if proceso:
        proceso_agrupar, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos_anual(seleccionar_reporte, lista_archivos)
        if mostrar_dic:
            mostrar_dic_archivos_agrupados_anual(proceso_agrupar, dic_archivos_mostrar)
        if continuar:
            option = "1"
        else:
            lista_menu = ["Sí","No"]
            option,valor = opcion_menu_valida(lista_menu, "¿Desea generar el reporte con los archivos disponibles?")
        if option == "1":
            return True, dic_archivos
        else:
            return False, False
    return False, False


def busqueda_archivos_tipo_anual(tipo, seleccionar_reporte, evitar_extra=[], txt=False, informar=True):
    tipo_evitar = tipo.replace(".csv","").replace(".CSV","").replace(".TXT","").replace(".txt","")
    lista_evitar_extra_copia = evitar_extra.copy()
    if len(tipo_evitar):
        lista_evitar_extra_copia.append(tipo_evitar)
    lista_evitar = especificar_lista_reportes_generados(lista_evitar_extra_copia)
    lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte_anual(seleccionar_reporte, tipo, lista_evitar)
    if len(lista_archivos) == 0:
        if informar:
            print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
        return False,lista_archivos
    else:
        return True,lista_archivos


def busqueda_archivos_general(seleccionar_reporte, tipo=None, evitar_extra=[],informar=True):
    lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, evitar_extra)
    if len(lista_archivos) == 0:
        if informar:
            print(f"\nNo se encontraron archivos en la ubicación seleccionada\n")
    else:
        lista_archivos_formato = []
        for archivo in lista_archivos:
            if archivo.endswith((".csv",".zip",".json",".xlsx")):
                lista_archivos_formato.append(archivo)
        proceso, dic_archivos, dic_archivos_mostrar = mod_4.agrupar_archivos(seleccionar_reporte, lista_archivos_formato)
        mostrar_dic_archivos_agrupados(proceso, dic_archivos_mostrar)

def mostrar_dic_archivos_agrupados(proceso, dic_archivos):
    if proceso:
        print("\nArchivos disponibles para la selección realizada: \n")
        for llave, valor in dic_archivos.items():
            print(f"Fecha: {llave}")
            for filial, lista_archivos_filial in valor.items():
                if len(lista_archivos_filial):
                    print(f"Filial: {filial}")
                    for texto in lista_archivos_filial:
                        print(texto)
            print("\n")
    else:
        print("\n¡No existen archivos disponibles!\n")

def mostrar_dic_archivos_agrupados_anual(proceso, dic_archivos):
    if proceso:
        print("\nArchivos disponibles para la selección realizada: \n")
        for llave, valor in dic_archivos.items():
            print(f"Fecha: {llave}")
            for i in valor:
                print(i)
            print("\n")
    else:
        print("\n¡No existen archivos disponibles!\n")



# * -------------------------------------------------------------------------------------------------------
# *                                             Menú de reportes comerciales
# * -------------------------------------------------------------------------------------------------------

def menu_comercial_sectores_consumo(option,valor):
    #? Generación de información comercial por sectores de consumo mensual
    if option == "1":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comercial_mensual")
        opciones_adicionales = anadir_opciones(True, True, True)
        if opciones_adicionales[0]:
            t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            codigo_DANE = opciones_adicionales[2]
            valor_facturado = opciones_adicionales[3]
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comercial_sector_consumo(lista_archivos, seleccionar_reporte, codigo_DANE, valor_facturado)
            if opciones_adicionales[0]:
                t_f = time.time()
                mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información comercial por sectores de consumo anual
    elif option == "2":
        print(valor)
        #reporte_comercial_anual
    #? Generación de información comercial (sumatoria) mensual
    elif option == "3":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comercial_mensual")
        opciones_adicionales = anadir_opciones(True, True, True)
        if opciones_adicionales[0]:
            t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            codigo_DANE = opciones_adicionales[2]
            valor_facturado = opciones_adicionales[3]
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comercial_sector_consumo(lista_archivos, seleccionar_reporte, codigo_DANE, valor_facturado, total=True)
            if opciones_adicionales[0]:
                t_f = time.time()
                mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información comercial (sumatoria) anual
    elif option == "4":
        print(valor)
        #reporte_comercial_anual
        """seleccionar_reporte = funcion_seleccionar_reportes("reporte_info_comercial_anual")
        seleccionar_reporte_copia = seleccionar_reporte.copy()
        opciones_adicionales = anadir_opciones(True, mostrar_archivos=True)
        if opciones_adicionales[0]:
            t_i = time.time()
        tipo = ".csv"
        lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
        lista_archivos_esperados,lista_fechas,lista_fechas_anios = mod_4.archivos_esperados(seleccionar_reporte,tipo)
        lista_no_encontrados = mod_4.todos_los_archivos(lista_archivos_esperados, lista_archivos)
        seleccionar_reporte_copia["fecha_personalizada"] = None
        fecha_aux = fecha_anterior_rango(lista_fechas[0][0],lista_fechas[0][1])
        seleccionar_reporte_copia["meses"] = [fecha_aux[1]]
        seleccionar_reporte_copia["anios"] = [fecha_aux[0]]
        lista_archivos_copia = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte_copia, tipo, lista_evitar)
        if len(lista_no_encontrados) > 0 or len(lista_archivos_copia) == 0:
            if len(lista_no_encontrados) > 0:
                print("\nNo es posible generar el reporte anual")
                mod_1.mostrar_lista_archivos(lista_no_encontrados, "Los archivos no encontrados son")
            if len(lista_archivos_copia) == 0:
                print(f"\nNo se encontraron archivos con la extensión {tipo} para la fecha {fecha_aux[1]}-{fecha_aux[0]}\n")
        else:
            if opciones_adicionales[1]:
                if opciones_adicionales[5]:
                    mod_1.estandarizacion_archivos(lista_archivos,True)
                else:
                    mod_1.estandarizacion_archivos(lista_archivos,False)
            tipo = "_form_estandar.csv"
            lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
            lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
            lista_archivos_esperados,lista_fechas,lista_fechas_anios = mod_4.archivos_esperados(seleccionar_reporte,tipo)
            lista_no_encontrados = mod_4.todos_los_archivos(lista_archivos_esperados, lista_archivos)
            lista_archivos_copia = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte_copia, tipo, lista_evitar)
            if len(lista_no_encontrados) > 0 or len(lista_archivos_copia) == 0:
                if len(lista_no_encontrados) > 0:
                    print("\nNo es posible generar el reporte anual")
                    mod_1.mostrar_lista_archivos(lista_no_encontrados, "Los archivos no encontrados son")
                    mod_1.regenerar_archivos_necesarios(lista_no_encontrados, tipo.replace(".csv",""))
                else:
                    print(f"\nNo se encontraron archivos con la extensión {tipo} para la fecha {fecha_aux[1]}-{fecha_aux[0]}\n")
            else:
                if opciones_adicionales[1]:
                    if opciones_adicionales[5]:
                        mod_1.archivos_resumen(lista_archivos,True)
                    else:
                        mod_1.archivos_resumen(lista_archivos,False)
                tipo = "_resumen.csv"
                lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
                lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
                lista_archivos_esperados,lista_fechas,lista_fechas_anios = mod_4.archivos_esperados(seleccionar_reporte,tipo)
                lista_no_encontrados = mod_4.todos_los_archivos(lista_archivos_esperados, lista_archivos)
                lista_archivos_copia = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte_copia, tipo, lista_evitar)
                if len(lista_no_encontrados) > 0 or len(lista_archivos_copia) == 0:
                    if len(lista_no_encontrados) > 0:
                        print("\nNo es posible generar el reporte anual")
                        mod_1.mostrar_lista_archivos(lista_no_encontrados, "Los archivos no encontrados son")
                        mod_1.regenerar_archivos_necesarios(lista_no_encontrados, tipo.replace(".csv",""))
                    if len(lista_archivos_copia) == 0:
                        print(f"\nNo se encontraron archivos con la extensión {tipo} para la fecha {fecha_aux[1]}-{fecha_aux[0]}\n")
                else:
                    mod_1.reporte_info_comercial_anual(lista_archivos,lista_archivos_copia, True, seleccionar_reporte, lista_fechas)
                    if opciones_adicionales[0]:
                        t_f = time.time()
                        mod_1.mostrar_tiempo(t_f, t_i)"""
    #? Generación de información comercial por sectores de consumo para usuarios subsidiados mensual
    elif option == "5":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comercial_subsidio_mensual")
        opciones_adicionales = anadir_opciones(True, True, True)
        if opciones_adicionales[0]:
            t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            codigo_DANE = opciones_adicionales[2]
            valor_facturado = opciones_adicionales[3]
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comercial_sector_consumo(lista_archivos, seleccionar_reporte, codigo_DANE, valor_facturado, subsidio=True)
            if opciones_adicionales[0]:
                t_f = time.time()
                mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información comercial por sectores de consumo para usuarios subsidiados anual
    elif option == "6":
        print(valor)
        #reporte_comercial_subsidio_anual
    #? Generación de información comercial (sumatoria) mensual
    elif option == "7":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comercial_subsidio_mensual")
        opciones_adicionales = anadir_opciones(True, True, True)
        if opciones_adicionales[0]:
            t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            codigo_DANE = opciones_adicionales[2]
            valor_facturado = opciones_adicionales[3]
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comercial_sector_consumo(lista_archivos, seleccionar_reporte, codigo_DANE, valor_facturado, total=True, subsidio=True)
            if opciones_adicionales[0]:
                t_f = time.time()
                mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información comercial (sumatoria) anual
    elif option == "8":
        print(valor)
        #reporte_comercial_subsidio_anual

def menu_comercial_compensaciones(option,valor):
    #? Generación de reportes de compensaciones mensual
    if option == "1":
        seleccionar_reporte = funcion_seleccionar_reportes("reportes_compensacion_mensual")
        op_add = anadir_opciones(regenerar=True, inventario=True, reportes_mensuales=None)
        regenerar = op_add[1]
        inventario = op_add[7]
        t_i = time.time()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        if regenerar:
            proceso,dic_archivos = generar_archivos_extra(seleccionar_reporte, regenerar, continuar=True, mostrar_dic=False, informar=False)
        proceso,dic_archivos = generar_archivos_extra(seleccionar_reporte, False, continuar=False, mostrar_dic=True)
        if proceso:
            mod_1.generar_reporte_compensacion_mensual(dic_archivos, seleccionar_reporte, True, inventario)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de reportes de compensaciones anual
    elif option == "2":
        seleccionar_reporte = funcion_seleccionar_reportes("reportes_compensacion_anual")
        reporte = "_compilado_compensacion.csv"
        op_add = anadir_opciones(True, reportes_mensuales=True,texto_regenerar_mensuales=reporte, inventario=True)
        t_i = time.time()
        regenerar = op_add[1]
        regenerar_reportes_mensuales = op_add[6]
        inventario = op_add[7]
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        if regenerar:
            proceso,dic_archivos = generar_archivos_extra(seleccionar_reporte, regenerar, continuar=True, mostrar_dic=False, informar=False)
        if regenerar_reportes_mensuales:
            proceso,dic_archivos = generar_archivos_extra(seleccionar_reporte, False, continuar=True, mostrar_dic=True)
            if proceso:
                mod_1.generar_reporte_compensacion_mensual(dic_archivos, seleccionar_reporte, True, inventario)
        proceso,dic_archivos_anual = generar_archivos_extra_anual(seleccionar_reporte, reporte)
        if proceso:
            mod_1.generar_reporte_compensacion_anual(dic_archivos_anual, seleccionar_reporte, True, inventario)
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)

def menu_comercial_trimestral(option,valor):
    #? Generación de información para el comportamiento patrimonial
    if option == "1":
        t_i = time.time()
        fi,ff,listas_unidas = eleccion_rango_trimestral()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        mod_1.reporte_comportamiento_patrimonial(fi,ff,listas_unidas)
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información de relación reclamos facturación (10.000)
    elif option == "2":
        t_i = time.time()
        fi,ff,listas_unidas = eleccion_rango_trimestral()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        mod_1.reporte_info_reclamos(fi,ff,listas_unidas)
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)

def menu_comercial_analisis_previo(option,valor):
    #? Generación de información para el inventrario de suscriptores mensual
    if option == "1":
        seleccionar_reporte = funcion_seleccionar_reportes("inventario_suscriptores_mensual")
        opciones_adicionales = anadir_opciones(regenerar=True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_usuarios_filial(lista_archivos, True, seleccionar_reporte)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información para el inventrario de suscriptores anual
    elif option == "2":
        seleccionar_reporte = funcion_seleccionar_reportes("inventario_suscriptores_anual")
        opciones_adicionales = anadir_opciones(regenerar=True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            #mod_1.reporte_usuarios_filial(lista_archivos, True, seleccionar_reporte)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información para usuarios regulados / no regulados mensual
    elif option == "3":
        seleccionar_reporte = funcion_seleccionar_reportes("usuarios_unicos_mensual")
        opciones_adicionales = anadir_opciones(regenerar=True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_usuarios_unicos_mensual(lista_archivos, True, seleccionar_reporte)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de información para usuarios regulados / no regulados anual
    elif option == "4":
        seleccionar_reporte = funcion_seleccionar_reportes("usuarios_unicos_anual")
        opciones_adicionales = anadir_opciones(regenerar=True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            #mod_1.reporte_usuarios_unicos_mensual(lista_archivos, True, seleccionar_reporte,incluir_factura=True)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)

def menu_comercial_cer_cld_prd(option,valor):
    #? Generación de reporte de comparación Producción - Calidad (GRC1-SAP)
    if option == "1":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comparacion_PRD_CLD")
        opciones_adicionales = anadir_opciones(True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1],["_CLD","_PRD"])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comparacion_prd_cld_cer(lista_archivos, seleccionar_reporte, True)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de reporte de comparación Certificación - Calidad (GRC1-SAP)
    elif option == "2":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comparacion_CLD")
        opciones_adicionales = anadir_opciones(regenerar=True, cantidad_filas=True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1],["_CLD","_PRD"])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comparacion_SAP(lista_archivos, seleccionar_reporte, True, opciones_adicionales[4], "GRC1_", "_CLD")
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de reporte de comparación Certificación - Producción (GRC1-SAP)
    elif option == "3":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comparacion_CLD")
        opciones_adicionales = anadir_opciones(regenerar=True, cantidad_filas=True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1],["_CLD","_PRD"])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comparacion_SAP(lista_archivos, seleccionar_reporte, True, opciones_adicionales[4], "GRC1_", "_PRD")
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de reporte de comparación Producción - Calidad (GRC1-SAP)
    elif option == "4":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_comparacion_CLD")
        opciones_adicionales = anadir_opciones(regenerar=True, cantidad_filas=True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1],["_CLD","_PRD"], "_PRD", "_CLD")
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_comparacion_SAP(lista_archivos, seleccionar_reporte, True, opciones_adicionales[4])
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)

def menu_comercial(option,valor):
    #? Información comercial por sector de consumo
    if option == "1":
        lista_menu = ["Generación de información comercial por sectores de consumo mensual",
                    "Generación de información comercial por sectores de consumo anual",
                    "Generación de información comercial (sumatoria) mensual",
                    "Generación de información comercial (sumatoria) anual",
                    "Generación de información comercial por sectores de consumo para usuarios subsidiados mensual",
                    "Generación de información comercial por sectores de consumo para usuarios subsidiados anual",
                    "Generación de información comercial (sumatoria) para usuarios subsidiados mensual",
                    "Generación de información comercial (sumatoria) para usuarios subsidiados anual",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Información comercial por sector de consumo")
        menu_comercial_sectores_consumo(option,valor)
    #? Compensaciones
    elif option == "2":
        lista_menu = ["Generación de reportes de compensaciones mensual",
                    "Generación de reportes de compensaciones anual",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Información comercial para compensaciones")
        menu_comercial_compensaciones(option,valor)
    #? Información comercial para reportes trimestrales
    elif option == "3":
        lista_menu = ["Generación de información para el comportamiento patrimonial",
                    "Generación de información de relación reclamos facturación (10.000)",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Información comercial para información de usuarios únicos")
        menu_comercial_trimestral(option,valor)
    #? Análisis previo para comprobar la calidad de la información
    elif option == "4":
        lista_menu = ["Generación de información para el inventrario de suscriptores mensual",
                    "Generación de información para el inventrario de suscriptores anual",
                    "Generación de información de facturación para usuarios regulados / no regulados mensual",
                    "Generación de información de facturación para usuarios regulados / no regulados anual",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Información comercial para información de usuarios únicos")
        menu_comercial_analisis_previo(option,valor)
    #? "Análisis previo para comprobar la calidad de la información
    elif option == "5":
        lista_menu = ["Generación de reporte de comparación Certificación - Calidad - Producción (GRC1-SAP)", #Op1
                    "Generación de reporte de comparación Certificación - Calidad (GRC1-SAP)", #Op2
                    "Generación de reporte de comparación Certificación - Producción (GRC1-SAP)", #Op3
                    "Generación de reporte de comparación Calidad - Producción (GRC1-SAP)", #Op4
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Información comercial para comparación de archivos de Certificación, Calidad y Producción")
        menu_comercial_cer_cld_prd(option,valor)

# * -------------------------------------------------------------------------------------------------------
# *                                             Menú de reportes tarifarios
# * -------------------------------------------------------------------------------------------------------
def menu_tarifario(option,valor):
    #? Generación de reportes tarifarios mensual
    if option == "1":
        seleccionar_reporte = funcion_seleccionar_reportes("reporte_tarifas_mensual")
        opciones_adicionales = anadir_opciones(regenerar=True)
        if opciones_adicionales[0]:
            t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.reporte_tarifas_mensual(lista_archivos, True, seleccionar_reporte)
            if opciones_adicionales[0]:
                t_f = time.time()
                mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de reportes tarifarios anual
    elif option == "2":
        print(valor)
        """seleccionar_reporte = funcion_seleccionar_reportes("reporte_tarifas_anual")
        seleccionar_reporte_copia = seleccionar_reporte.copy()
        opciones_adicionales = anadir_opciones(True, mostrar_archivos=True)
        if opciones_adicionales[0]:
            t_i = time.time()
        tipo = ".csv"
        lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
        lista_archivos_esperados,lista_fechas,lista_fechas_anios = mod_4.archivos_esperados(seleccionar_reporte,tipo)
        lista_no_encontrados = mod_4.todos_los_archivos(lista_archivos_esperados, lista_archivos)
        seleccionar_reporte_copia["fecha_personalizada"] = None
        fecha_aux = fecha_anterior_rango(lista_fechas[0][0],lista_fechas[0][1])
        seleccionar_reporte_copia["meses"] = [fecha_aux[1]]
        seleccionar_reporte_copia["anios"] = [fecha_aux[0]]
        lista_archivos_copia = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte_copia, tipo, lista_evitar)
        if len(lista_no_encontrados) > 0 or len(lista_archivos_copia) == 0:
            if len(lista_no_encontrados) > 0:
                print("\nNo es posible generar el reporte anual")
                mod_1.mostrar_lista_archivos(lista_no_encontrados, "Los archivos no encontrados son")
            if len(lista_archivos_copia) == 0:
                print(f"\nNo se encontraron archivos con la extensión {tipo} para la fecha {fecha_aux[1]}-{fecha_aux[0]}\n")
        else:
            if opciones_adicionales[1]:
                if opciones_adicionales[5]:
                    mod_1.estandarizacion_archivos(lista_archivos,True)
                else:
                    mod_1.estandarizacion_archivos(lista_archivos,False)
            tipo = "_form_estandar.csv"
            lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
            lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
            lista_archivos_esperados,lista_fechas,lista_fechas_anios = mod_4.archivos_esperados(seleccionar_reporte,tipo)
            lista_no_encontrados = mod_4.todos_los_archivos(lista_archivos_esperados, lista_archivos)
            lista_archivos_copia = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte_copia, tipo, lista_evitar)
            if len(lista_no_encontrados) > 0 or len(lista_archivos_copia) == 0:
                if len(lista_no_encontrados) > 0:
                    print("\nNo es posible generar el reporte anual")
                    mod_1.mostrar_lista_archivos(lista_no_encontrados, "Los archivos no encontrados son")
                    mod_1.regenerar_archivos_necesarios(lista_no_encontrados, tipo.replace(".csv",""))
                else:
                    print(f"\nNo se encontraron archivos con la extensión {tipo} para la fecha {fecha_aux[1]}-{fecha_aux[0]}\n")
            else:
                if opciones_adicionales[1]:
                    if opciones_adicionales[5]:
                        mod_1.archivos_resumen(lista_archivos,True)
                    else:
                        mod_1.archivos_resumen(lista_archivos,False)
                tipo = "_resumen.csv"
                lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
                lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
                lista_archivos_esperados,lista_fechas,lista_fechas_anios = mod_4.archivos_esperados(seleccionar_reporte,tipo)
                lista_no_encontrados = mod_4.todos_los_archivos(lista_archivos_esperados, lista_archivos)
                lista_archivos_copia = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte_copia, tipo, lista_evitar)
                if len(lista_no_encontrados) > 0 or len(lista_archivos_copia) == 0:
                    if len(lista_no_encontrados) > 0:
                        print("\nNo es posible generar el reporte anual")
                        mod_1.mostrar_lista_archivos(lista_no_encontrados, "Los archivos no encontrados son")
                        mod_1.regenerar_archivos_necesarios(lista_no_encontrados, tipo.replace(".csv",""))
                    if len(lista_archivos_copia) == 0:
                        print(f"\nNo se encontraron archivos con la extensión {tipo} para la fecha {fecha_aux[1]}-{fecha_aux[0]}\n")
                else:
                    mod_1.reporte_tarifas_anual(lista_archivos,lista_archivos_copia, True, seleccionar_reporte, lista_fechas)
                    if opciones_adicionales[0]:
                        t_f = time.time()
                        mod_1.mostrar_tiempo(t_f, t_i)"""

# * -------------------------------------------------------------------------------------------------------
# *                                             Menú de reportes técnicos
# * -------------------------------------------------------------------------------------------------------
def menu_tecnico(option,valor):
    #? Generación de consolidación de indicadores técnicos (IPLI,IO,IRST-EG) mensual
    if option == "1":
        seleccionar_reporte = funcion_seleccionar_reportes("reportes_indicadores_tecnicos_mensual")
        opciones_adicionales = anadir_opciones(True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.generar_reporte_indicadores_tecnicos_mensual(lista_archivos, seleccionar_reporte, True)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de consolidación de indicadores técnicos (IPLI,IO,IRST-EG) anual
    elif option == "2":
        print(valor)
        """seleccionar_reporte = funcion_seleccionar_reportes("reportes_indicadores_tecnicos_anual")
        tipo = ".csv"
        lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
        lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
        lista_archivos_esperados,lista_fechas,lista_fechas_anios = mod_4.archivos_esperados(seleccionar_reporte)
        lista_no_encontrados = mod_4.todos_los_archivos(lista_archivos_esperados, lista_archivos)
        if lista_no_encontrados:
            print("\nNo es posible generar el reporte anual")
            mod_1.mostrar_lista(lista_no_encontrados, "Los archivos no encontrados son")
        else:
            mod_1.estandarizacion_archivos(lista_archivos,False)
            tipo = "_form_estandar.csv"
            lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
            lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
            if len(lista_archivos) == 0:
                print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
            else:
                mod_1.archivos_resumen(lista_archivos,False)
                tipo = "_resumen.csv"
                lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
                lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
                if len(lista_archivos) == 0:
                    print(f"\nNo se encontraron archivos con la extensión {tipo}\n")
                else:
                    mod_1.generar_reporte_indicadores_tecnicos_mensual(lista_archivos, False)
                    tipo = "_indicador_tecnico.csv"
                    lista_evitar = especificar_lista_reportes_generados([tipo.replace(".txt","").replace(".csv","")])
                    lista_archivos = mod_4.encontrar_archivos_seleccionar_reporte(seleccionar_reporte, tipo, lista_evitar)
                    if len(seleccionar_reporte["filial"]) == 1:
                        mod_1.generar_reporte_indicadores_tecnicos_anual(lista_archivos, True, seleccionar_reporte["filial"][0], seleccionar_reporte)
                    else:
                        mod_1.generar_reporte_indicadores_tecnicos_anual_total(lista_archivos, True, seleccionar_reporte)"""
    #? Generación de reporte de suspensiones mensual
    elif option == "3":
        seleccionar_reporte = funcion_seleccionar_reportes("reportes_suspension_mensual")
        opciones_adicionales = anadir_opciones(True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.generar_reporte_suspension_mensual(lista_archivos, seleccionar_reporte, True)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de reporte de suspensiones anual
    elif option == "4":
        seleccionar_reporte = funcion_seleccionar_reportes("reportes_suspension_anual")
        print("Reporte a generar:",seleccionar_reporte)
    #? Generación de reporte de información de respuesta a servicio técnico (IRST) mensual
    elif option == "5":
        seleccionar_reporte = funcion_seleccionar_reportes("reportes_indicadores_tecnicos_IRST_mensual")
        opciones_adicionales = anadir_opciones(True)
        t_i = time.time()
        proceso,lista_archivos = generar_archivos_extra(seleccionar_reporte, opciones_adicionales[1])
        if proceso:
            print(f"\nInicio de procesamiento para: {valor}\n\n")
            mod_1.generar_reporte_indicadores_tecnicos_IRST_mensual(lista_archivos, seleccionar_reporte)
            t_f = time.time()
            mod_1.mostrar_tiempo(t_f, t_i)
    #? Generación de reporte de información de respuesta a servicio técnico (IRST) anual
    elif option == "6":
        print(valor)
        #seleccionar_reporte = funcion_seleccionar_reportes("reportes_indicadores_tecnicos_IRST_anual")
        #print("Reporte a generar:",seleccionar_reporte)

# * -------------------------------------------------------------------------------------------------------
# *                                             Menú de Cumplimiento de Reportes Regulatorios
# * -------------------------------------------------------------------------------------------------------
def menu_cumplimientos_reportes(option, valor):
    #? Porcentaje de Cumplimientos Regulatorios
    if option == "1":
        t_i = time.time()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        mod_1.generar_porcentaje_cumplimientos_regulatorios()
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)
    #? Porcentaje de AEGR
    elif option == "2":
        t_i = time.time()
        print(f"\nInicio de procesamiento para: {valor}\n\n")
        #LL=llamado función
        t_f = time.time()
        mod_1.mostrar_tiempo(t_f, t_i)

# * -------------------------------------------------------------------------------------------------------
# *                                             Menú general
# * -------------------------------------------------------------------------------------------------------
def menu_inicial(lista, nombre):
    option,valor = opcion_menu_valida(lista, nombre, False)
    if option == str(len(lista)):
        mod_1.mostrar_texto("Adiós","texto")
        time.sleep(2)
        subprocess.run(['taskkill', '/F', '/IM', 'pwsh.exe', '/T'], check=True)
        os.system("exit")
        #os.system("taskkill /F /IM cmd.exe") 
    elif option == "1":
        lista_menu = ["Creación de espacio de trabajo (Carpetas)",
                        "Agregar un nuevo año",
                        "Editar un reporte existente",
                        "Agregar un nuevo tipo de reporte",
                        "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Menú de configuración inicial",False)
        menu_configuracion_inicial(option,valor)
    elif option == "2":
        lista_menu = ["Conversión de archivos txt a csv",
                    "Almacenar archivos",
                    "Estandarización de archivos",
                    "Generar archivos de tipo resumen",
                    "Revisión de archivos existentes",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Edición de archivos",False)
        menu_opciones_archivos(option,valor)
    elif option == "3":
        lista_menu = ["Información comercial por sector de consumo",
                        "Información comercial para compensaciones",
                        "Información comercial para reportes trimestrales",
                        "Análisis previo para comprobar la calidad de la información",
                        "Comparación entre archivos de certificación, calidad (CLD) y/o producción (PRD)",
                        "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Reportes de Información Comercial", False)
        menu_comercial(option, valor)
    elif option == "4":
        lista_menu = ["Generación de reportes tarifarios mensual",
                    "Generación de reportes tarifarios anual",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Reportes Tarifarios", False)
        menu_tarifario(option,valor)
    elif option == "5":
        lista_menu = ["Generación de consolidación de indicadores técnicos (IPLI,IO,IRST-EG) mensual",
                    "Generación de consolidación de indicadores técnicos (IPLI,IO,IRST-EG) anual",
                    "Generación de reporte de suspensiones mensual",
                    "Generación de reporte de suspensiones anual",
                    "Generación de reporte de información de respuesta a servicio técnico (IRST) mensual",
                    "Generación de reporte de información de respuesta a servicio técnico (IRST) anual",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Reportes Técnicos", False)
        menu_tecnico(option,valor)
    elif option == "6":
        lista_menu = ["Porcentaje de Cumplimientos Regulatorios",
                    "Porcentaje de AEGR",
                    "Regresar al menú inicial"]
        option,valor = opcion_menu_valida(lista_menu, "Reportes Técnicos", False)
        menu_cumplimientos_reportes(option,valor)
    elif option == "7":
        print("\nCreación de Dashboard en proceso...\n")
    return True

# * -------------------------------------------------------------------------------------------------------
# *                                             Configuración inicial seleccionar reporte
# * -------------------------------------------------------------------------------------------------------
def reset_reporte():
    seleccionar_reportes = {"ubicacion":None,
                        "anios":None,
                        "filial":None,
                        "meses":None,
                        "tipo":None,
                        "clasificacion":None,
                        "fecha_personalizada":None}
    return seleccionar_reportes

# * -------------------------------------------------------------------------------------------------------
# *                                             Configuración seleccionar reporte
# * -------------------------------------------------------------------------------------------------------
def eleccion_elemento(seleccionar_reportes, lista_evaluar, opcion_extra, nombre, llave, separacion):
    lista = []
    lista = lista_evaluar.copy()
    if opcion_extra:
        lista.append(opcion_extra)
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, nombre, separacion)
    largo = len(lista)
    if option == str(largo):
        iniciar_menu()
    elif option == str(largo-1):
        seleccionar_reportes[llave] = lista_evaluar.copy()
        return seleccionar_reportes
    else:
        seleccionar_reportes[llave] = [lista[int(option)-1]]
        return seleccionar_reportes

def elecciones_para_tipos_de_reporte(seleccionar_reportes):
    seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
    seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
    seleccionar_reportes = eleccion_elemento(seleccionar_reportes, dic_reportes[seleccionar_reportes["tipo"][0]].copy(), "Seleccionar todos los reportes", "Elección reporte", "clasificacion", False)
    return seleccionar_reportes

def funcion_seleccionar_reportes(tipo):
    seleccionar_reportes = reset_reporte()
    #? Reportes generales
    if tipo == "reporte_vanti":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, list(dic_reportes.keys()).copy(), "Seleccionar todos los tipos de reporte", "Elección tipo de reporte", "tipo", False)
        if len(seleccionar_reportes["tipo"]) == 1:
            seleccionar_reportes = eleccion_elemento(seleccionar_reportes, dic_reportes[seleccionar_reportes["tipo"][0]].copy(), "Seleccionar todos los reportes", "Elección reporte", "clasificacion", False)
        elif len(seleccionar_reportes["tipo"]) > 1:
            seleccionar_reportes["clasificacion"] = lista_reportes_totales
        return seleccionar_reportes
    elif tipo == "reporte_general":
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_reportes_generales.copy(), "Seleccionar todas las carpetas", "Elección carpeta general", "ubicacion", False)
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        if "Reportes Nuevo SUI" in seleccionar_reportes["ubicacion"]:
            seleccionar_reportes = eleccion_elemento(seleccionar_reportes, list(dic_reportes.keys()).copy(), "Seleccionar todos los tipos de reporte", "Elección tipo de reporte", "tipo", False)
            if len(seleccionar_reportes["tipo"]) == 1:
                seleccionar_reportes = eleccion_elemento(seleccionar_reportes, dic_reportes[seleccionar_reportes["tipo"][0]].copy(), "Seleccionar todos los reportes", "Elección reporte", "clasificacion", False)
            elif len(seleccionar_reportes["tipo"]) > 1:
                seleccionar_reportes["clasificacion"] = lista_reportes_totales
        return seleccionar_reportes
    #? Reportes comerciales
    elif tipo == "inventario_suscriptores_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRTT2","GRC1"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "inventario_suscriptores_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRTT2","GRC1"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
    elif tipo == "usuarios_unicos_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1","GRC2","GRTT2"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "usuarios_unicos_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1","GRC2"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reporte_comercial_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1","GRC2","GRTT2"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reporte_comercial_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1","GRC2","GRTT2"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reporte_comercial_subsidio_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1","GRTT2"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reporte_comercial_subsidio_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1","GRTT2"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reporte_comparacion_PRD_CLD":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1","GRTT2"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reporte_comparacion_CLD":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC1"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reportes_compensacion_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC3","GRTT2"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reportes_compensacion_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Comercial"]
        seleccionar_reportes["clasificacion"] = ["GRC3","GRTT2"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    #? Reportes tarifarios
    elif tipo == "reporte_tarifas_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tarifario"]
        seleccionar_reportes["clasificacion"] = ["GRT1"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reporte_tarifas_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tarifario"]
        seleccionar_reportes["clasificacion"] = ["GRT1"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    #? Reportes tecnicos
    elif tipo == "reportes_suspension_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tecnico"]
        seleccionar_reportes["clasificacion"] = ["GRS1"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reportes_suspension_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tecnico"]
        seleccionar_reportes["clasificacion"] = ["GRS1"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reportes_indicadores_tecnicos_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tecnico"]
        seleccionar_reportes["clasificacion"] = ["GRCS2"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reportes_indicadores_tecnicos_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tecnico"]
        seleccionar_reportes["clasificacion"] = ["GRCS2"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reportes_indicadores_tecnicos_IRST_mensual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tecnico"]
        seleccionar_reportes["clasificacion"] = ["GRCS1"]
        seleccionar_reportes = eleccion_fecha_personalizada(seleccionar_reportes, True)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    elif tipo == "reportes_indicadores_tecnicos_IRST_anual":
        seleccionar_reportes["ubicacion"] = ["Reportes Nuevo SUI"]
        seleccionar_reportes["tipo"] = ["Tecnico"]
        seleccionar_reportes["clasificacion"] = ["GRCS1"]
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_filiales.copy(), "Seleccionar todas las filiales", "Elección filial", "filial", False)
        return seleccionar_reportes
    iniciar_menu()

# * -------------------------------------------------------------------------------------------------------
# *                                             Procesamiento de fechas
# * -------------------------------------------------------------------------------------------------------

def eleccion_fecha_personalizada(seleccionar_reportes, personalizado):
    if personalizado:
        lista = ["Elegir un año y mes específico",
                "Elegir un rango anual (12 meses)",
                "Elegir un periodo personalizado (Mes/Año Inicial - Mes/Año Final)"]
    else:
        lista = ["Elegir un año y mes específico",
                "Elegir un rango anual (12 meses)"]
    seleccionar_reportes = eleccion_fecha(seleccionar_reportes, lista, None, "Elección de fechas para la búsqueda de información",False, personalizado)
    return seleccionar_reportes

def fecha_final_rango(anio_inicial, mes_inicial):
    ubi_mes = lista_meses.index(mes_inicial)
    if ubi_mes == 0:
        return (anio_inicial, lista_meses[-1])
    else:
        anio_final = str(int(anio_inicial)+1)
        mes_final = lista_meses[ubi_mes-1]
        return (anio_final, mes_final)

def fecha_inicial_rango(anio_final, mes_final):
    ubi_mes = lista_meses.index(mes_final)
    if ubi_mes == len(lista_meses)-1:
        return (anio_final, lista_meses[0])
    else:
        anio_incial = str(int(anio_final)-1)
        mes_inicial = lista_meses[ubi_mes+1]
        return (anio_incial, mes_inicial)

def fecha_anterior_rango(anio, mes):
    ubi_mes = lista_meses.index(mes)
    if ubi_mes == 0:
        return (str(anio-1), lista_meses[-1])
    else:
        anio = str(int(anio))
        mes = lista_meses[ubi_mes-1]
        return (anio,  mes)

def eleccion_rango_anual(seleccionar_reportes):
    option_1,valor_1 = opcion_menu_valida(["Inicio del rango anual","Fin del rango anual"], "Elección tipos de rangos", False)
    if option_1 == "1":
        option_2,valor_2 = opcion_menu_valida(mod_1.unir_listas_anio_mes(lista_anios, lista_meses), "Elección de mes-año inicial para el rango anual", True)
        fecha = valor_2.split(" - ")
        fi = (fecha[0],fecha[1])
        ff = fecha_final_rango(fecha[0],fecha[1])
        seleccionar_reportes["fecha_personalizada"] = [fi,ff]
        print(f"\nRango anual seleccionado: {fi[0]}/{fi[1]} - {ff[0]}/{ff[1]}\n")
    elif option_1 == "2":
        option_2,valor_2 = opcion_menu_valida(mod_1.unir_listas_anio_mes(lista_anios, lista_meses), "Elección de mes-año final para el rango anual", True)
        fecha = valor_2.split(" - ")
        ff = (fecha[0],fecha[1])
        fi = fecha_inicial_rango(fecha[0],fecha[1])
        seleccionar_reportes["fecha_personalizada"] = [fi,ff]
        print(f"\nRango anual seleccionado: {fi[0]}/{fi[1]} - {ff[0]}/{ff[1]}\n")
    return seleccionar_reportes

def fecha_final_rango_tri(anio_inicial, tri_inicial):
    ubi_tri = lista_trimestres.index(tri_inicial)
    if ubi_tri == 0:
        return (anio_inicial, lista_trimestres[-1])
    else:
        anio_final = str(int(anio_inicial)+1)
        tri_final = lista_trimestres[ubi_tri-1]
        return (anio_final, tri_final)

def fecha_inicial_rango_tri(anio_final, tri_final):
    ubi_tri = lista_trimestres.index(tri_final)
    if ubi_tri == len(lista_trimestres)-1:
        return (anio_final, lista_trimestres[0])
    else:
        anio_incial = str(int(anio_final)-1)
        tri_inicial = lista_trimestres[ubi_tri+1]
        return (anio_incial, tri_inicial)

def eleccion_rango_trimestral():
    option_1,valor_1 = opcion_menu_valida(["Inicio del rango anual","Fin del rango anual"], "Elección tipos de rangos", False)
    listas_unidas = mod_1.unir_listas_anio_tri(lista_anios, lista_trimestres)
    if option_1 == "1":
        if len(lista_anios) > 4:
            salto = True
        else:
            salto = False
        option_2,valor_2 = opcion_menu_valida(listas_unidas, "Elección de trimestre-año inicial para el rango anual", salto)
        fecha = valor_2.split(" - ")
        fi = (fecha[0],fecha[1])
        ff = fecha_final_rango_tri(fecha[0],fecha[1])
        print(f"\nRango anual seleccionado: {fi[0]}/{fi[1]} - {ff[0]}/{ff[1]}\n")
        return fi,ff,listas_unidas
    elif option_1 == "2":
        option_2,valor_2 = opcion_menu_valida(listas_unidas, "Elección de trimestre-año final para el rango anual", False)
        fecha = valor_2.split(" - ")
        ff = (fecha[0],fecha[1])
        fi = fecha_inicial_rango_tri(fecha[0],fecha[1])
        print(f"\nRango anual seleccionado: {fi[0]}/{fi[1]} - {ff[0]}/{ff[1]}\n")
        return fi,ff,listas_unidas

def eleccion_fecha(seleccionar_reportes, lista_evaluar, opcion_extra, nombre, separacion, personalizado):
    lista = []
    lista = lista_evaluar.copy()
    if opcion_extra:
        lista.append(opcion_extra)
    lista.append("Regresar al menú inicial")
    option,valor = opcion_menu_valida(lista, nombre, separacion)
    largo = len(lista)
    if option == str(largo):
        iniciar_menu()
    elif option == "1":
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_anios.copy(), "Seleccionar todos los años", "Elección año", "anios", False)
        seleccionar_reportes = eleccion_elemento(seleccionar_reportes, lista_meses.copy(), "Seleccionar todos los meses", "Elección mes", "meses", False)
        return seleccionar_reportes
    elif option == "2":
        seleccionar_reportes = eleccion_rango_anual(seleccionar_reportes)
        return seleccionar_reportes
    if personalizado and option == "3":
        option_1,valor_1 = opcion_menu_valida(mod_1.unir_listas_anio_mes(lista_anios, lista_meses), "Elección periodo (mes-año) inicial para el rango", True)
        option_2,valor_2 = opcion_menu_valida(mod_1.unir_listas_anio_mes(lista_anios, lista_meses), "Elección periodo (mes-año) final para el rango", True)
        fecha_1 = valor_1.split(" - ")
        fecha_2 = valor_2.split(" - ")
        if fecha_1 == fecha_2:
            seleccionar_reportes["fecha_personalizada"] = [(fecha_1[0],fecha_1[1]),(fecha_2[0],fecha_2[1])]
            print(f"\nRango seleccionado: {fecha_1[0]}/{fecha_1[1]} - {fecha_2[0]}/{fecha_2[1]}\n")
            return seleccionar_reportes
        elif int(fecha_1[0]) > int(fecha_2[0]):
            seleccionar_reportes["fecha_personalizada"] = [(fecha_2[0],fecha_2[1]),(fecha_1[0],fecha_1[1])]
            print(f"\nRango seleccionado: {fecha_2[0]}/{fecha_2[1]} - {fecha_1[0]}/{fecha_1[1]}\n")
            return seleccionar_reportes
        elif int(fecha_1[0]) < int(fecha_2[0]):
            seleccionar_reportes["fecha_personalizada"] = [(fecha_1[0],fecha_1[1]),(fecha_2[0],fecha_2[1])]
            print(f"\nRango seleccionado: {fecha_1[0]}/{fecha_1[1]} - {fecha_2[0]}/{fecha_2[1]}\n")
            return seleccionar_reportes
        elif fecha_1[0] == fecha_2[0]:
            if lista_meses.index(fecha_1[1]) > lista_meses.index(fecha_2[1]):
                seleccionar_reportes["fecha_personalizada"] = [(fecha_2[0],fecha_2[1]),(fecha_1[0],fecha_1[1])]
                print(f"\nRango seleccionado: {fecha_2[0]}/{fecha_2[1]} - {fecha_1[0]}/{fecha_1[1]}\n")
                return seleccionar_reportes
            else:
                seleccionar_reportes["fecha_personalizada"] = [(fecha_1[0],fecha_1[1]),(fecha_2[0],fecha_2[1])]
                print(f"\nRango seleccionado: {fecha_1[0]}/{fecha_1[1]} - {fecha_2[0]}/{fecha_2[1]}\n")
                return seleccionar_reportes

# * -------------------------------------------------------------------------------------------------------
# *                                             Opciones de menú inicial
# * -------------------------------------------------------------------------------------------------------
def iniciar_menu():
    lista_menu_incial = ["Configuración inicial",
                        "Edición de archivos",
                        "Actividades con Reportes Comerciales",
                        "Actividades con Reportes Tarifarios",
                        "Actividades con Reportes Técnicos",
                        "Activides con Cumplimiento de Reportes",
                        "Generar archivos Dashboard",
                        "Salir"]
    centinela = True
    while centinela:
        centinela = menu_inicial(lista_menu_incial, "Inicial")

def mostrar_inicio_app():
    mod_1.mostrar_titulo(f"Bienvenid@ al aplicativo de VANTI versión {version}", True, None)
    mod_1.mostrar_titulo("Vicepresidencia de Estrategia y Finanzas", None, "up")
    mod_1.mostrar_titulo("Regulación, Márgenes y Tarifas", None, "down")
    iniciar_menu()

mostrar_inicio_app()


# TODO Pendientes:
    #Descargar archivos
    # Archivos anuales
    #Revisar llamado de todas las funciones
    # Crear carpeta comercial,tarifario,tecnico en cada reporte anual
    #Encontrar los reportes mensuales generados y faltantes para los reportes anuales
    #Archivos necesarios para el Dashboard (cambiar la función de archivos esperados)

# TODO Aplicativo:
    # Generación de gráficas
    # Incluir tiempo estimado promedio por mes para la documentación de explicación