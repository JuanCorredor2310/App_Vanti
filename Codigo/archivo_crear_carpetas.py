import os
import sys
import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
sys.path.append(os.path.abspath(ruta_codigo))
import archivo_creacion_json as mod_2
import modulo as mod_1

# * -------------------------------------------------------------------------------------------------------
# *                                             Configuración inicial
# * -------------------------------------------------------------------------------------------------------
def configuracion_inicial():
    mod_2.crear_archivos_json_principales()
    iniciar_funcion_crear_carpetas()

def funcion_creacion_carpetas(nombre):
    dic_carpetas = mod_2.leer_archivos_json(ruta_constantes+nombre+".json")
    lista_ubicaciones = [ruta_archivos]
    for llave, valor in dic_carpetas.items():
        if llave != "carpeta_6":
            lista_ubicaciones_2 = []
            if llave == "carpeta_1":
                lista_enumerada = valor.copy()
            else:
                lista_enumerada = mod_1.enumerar_lista(valor, True)
            for carpeta in lista_ubicaciones:
                for elemento in lista_enumerada:
                    lista_ubicaciones_2.append(carpeta+"/"+elemento)
            lista_ubicaciones = lista_ubicaciones_2.copy()
            mod_1.creacion_carpeta(lista_ubicaciones)
        else:
            lista_ubicaciones_2 = []
            lista_ubicaciones_3 = []
            lista_copia_1 = list(dic_carpetas[llave].keys()).copy()
            lista_enumerada = mod_1.enumerar_lista(lista_copia_1, True)
            for carpeta in lista_ubicaciones:
                for i in range(len(lista_enumerada)):
                    elemento = lista_copia_1[i]
                    lista_ubicaciones_2.append(carpeta+"/"+lista_enumerada[i])
                    lista_enumerada_1 = mod_1.enumerar_lista(dic_carpetas[llave][elemento], True)
                    for elemento_1 in lista_enumerada_1:
                        lista_ubicaciones_3.append(carpeta+"/"+lista_enumerada[i]+"/"+elemento_1)
            mod_1.creacion_carpeta(lista_ubicaciones_2)
            mod_1.creacion_carpeta(lista_ubicaciones_3)

def iniciar_funcion_crear_carpetas():
    funcion_creacion_carpetas("carpetas")
    funcion_creacion_carpetas("carpetas_1")
    funcion_creacion_carpetas("carpetas_2")
    df = mod_1.leer_dataframe(ruta_constantes+"mercado_relevante.csv")
    dic_DANE = {}
    for i in range(len(df)):
        dic_DANE[str(df["Codigo_DANE"][i])] = {"Id_mercado":str(df["Id_mercado"][i]),
                                                "Id_empresa":str(df["Id_empresa"][i]),
                                                "Nombre_municipio":str(df["Nombre_municipio"][i])}
    mod_2.almacenar_json(dic_DANE, ruta_constantes+"mercado_relevante.json")
    df = mod_1.leer_dataframe(ruta_constantes+"mercado_relevante_resumen.csv")
    dic_mercado_rele = {}
    for i in range(len(df)):
        dic_mercado_rele[str(df["Id_mercado"][i])] = {"Id_empresa":str(df["Id_empresa"][i]),
                                                "Nombre_mercado":str(df["Nombre_mercado"][i]),
                                                "Nombre_municipio":str(df["Nombre_municipio"][i]),
                                                "Latitud":str(df["Latitud"][i]),
                                                "Longitud":str(df["Longitud"][i])}
    mod_2.almacenar_json(dic_mercado_rele, ruta_constantes+"mercado_relevante_resumen.json")
    lista = mod_1.buscar_carpetas(ruta_nuevo_sui)
    ruta_1 = None
    for i in lista:
        if "Tablas Maestras" in i:
            ruta_1 = i
    if ruta_1:
        df.to_csv(ruta_constantes+"mercado_relevante.csv", index=False)

