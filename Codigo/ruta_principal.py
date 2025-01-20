def v_ruta_principal(t=""):
    if t != "":
        #valor = r"c:\\Aplicativo_Regulacion_Vanti\\"+t
        valor = r"c:\\Aplicativo_Regulacion_Vanti\\"+t
    else:
        #valor = r"c:\\Aplicativo_Regulacion_Vanti"
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
    valor = v_ruta_principal(r"Archivos\\Guardar_Archivos\\")
    return valor

def v_carpeta_comprimida():
    valor = v_ruta_principal(r"Archivos\\Carpetas_Comprimidas\\")
    return valor

def v_fuentes():
    valor = v_ruta_principal(r"App_Vanti\\Fuentes\\")
    return valor

def v_imagenes():
    valor = v_ruta_principal(r"App_Vanti\\Imagenes\\")
    return valor