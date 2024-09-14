import os
import sys
def v_ruta_principal(t=""):
    if t != "":
        valor = r"c:\\Aplicativo_Regulacion_Vanti"+"\\"+t
    else:
        valor = r"c:\\Aplicativo_Regulacion_Vanti"
    return valor

def v_codigo():
    valor = v_ruta_principal("Codigo_Vanti")
    return valor

def v_constantes():
    valor = v_ruta_principal("Constantes")
    return valor



