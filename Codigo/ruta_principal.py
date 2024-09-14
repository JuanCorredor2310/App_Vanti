def v_ruta_principal(t=""):
    if t != "":
        valor = r"c:\\Aplicativo_Regulacion_Vanti"+"\\"+t
    else:
        valor = r"c:\\Aplicativo_Regulacion_Vanti"
    return valor

def v_codigo():
    valor = v_ruta_principal("App_Vanti\\Codigo\\")
    return valor

def v_constantes():
    valor = v_ruta_principal("App_Vanti\\Constantes\\")
    return valor

def v_nuevo_sui():
    valor = v_ruta_principal("Archivos\\NUEVO SUI\\")
    return valor

def v_archivos():
    valor = v_ruta_principal("Archivos\\")
    return valor

def v_guardar_archivos():
    valor = v_ruta_principal("Archivos\\Gurdar_Archivos")
    return valor