import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
import numpy as np
import seaborn as sns
import pandas as pd
from pandas.plotting import table
import os
from PIL import Image,ImageDraw,ImageFont
from skimage.transform import resize

import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos,ruta_fuentes,ruta_imagenes
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
ruta_fuentes = mod_rp.v_fuentes()
ruta_imagenes = mod_rp.v_imagenes()
import modulo as mod_1
import archivo_creacion_json as mod_2

global grupo_vanti, lista_filiales, dic_filiales, dic_filiales_largo, limite_facturas, porcentaje_ISRT, dic_nom_eventos,dic_sectores_consumo,dic_sectores_consumo_ordenados,dic_sectores_consumo_imagenes,dic_estratos,dic_industrias,lista_filiales_corto,fuente_texto,ruta_fuente,ruta_fuente_negrilla,custom_font,dic_colores,dic_industrias_grupos,dic_mercados
dic_sectores_consumo = mod_1.leer_archivos_json(ruta_constantes+"sectores_consumo_categoria.json")["datos"]
dic_sectores_consumo_ordenados = {"Regulados": ["Residencial","Comercial","Industrial"],
                                "No regulados": ["Industrial","GNCV","Comercial","Comercializadoras /\nTransportadores","Petroqu\u00edmica","Oficiales","Termoel\u00e9ctrico","Refiner\u00eda"]}
dic_sectores_consumo_imagenes = {"Residencial":"residencial.png",
                                "Comercial":"comercial.png",
                                "Industrial":"industrial.png",
                                "GNCV":"gncv.png",
                                "Comercializadoras /\nTransportadores":"transporte.png",
                                "Petroqu\u00edmica":"otros.png",
                                "Oficiales":"otros.png",
                                "Termoel\u00e9ctrico":"electrico.png",
                                "Refiner\u00eda":"otros.png"}
dic_sectores_consumo_imagenes_pie = {"Residencial":"residencial.png",
                                "Comercial":"comercial.png",
                                "Industrial":"industrial.png",
                                "GNCV":"gncv.png",
                                "Comercializadoras / Transportadores":"transporte.png",
                                "Petroqu\u00edmica":"otros.png",
                                "Oficiales":"otros.png",
                                "Termoel\u00e9ctrico":"otros.png",
                                "Refiner\u00eda":"otros.png",
                                "Otros":"otros.png"}
grupo_vanti = "Grupo Vanti"
dic_nom_eventos = {"CONTROLADO" : "Controlados",
                    "NO CONTROLADO" : "No Controlados"}
dic_colores = mod_1.leer_archivos_json(ruta_constantes+"colores.json")["datos"]
dic_mercados = mod_1.leer_archivos_json(ruta_constantes+"mercado_relevante_resumen.json")
empresa_indicador_SUI = mod_1.leer_archivos_json(ruta_constantes+"empresa_indicador_SUI.json")["datos"]
porcentaje_ISRT = 100
limite_facturas = 4.04
dic_filiales = mod_1.leer_archivos_json(ruta_constantes+"tabla_empresa.json")["datos"]
lista_filiales = list(dic_filiales.values())
lista_filiales_corto = list(dic_filiales.keys())
dic_filiales_largo = {valor: llave for llave, valor in dic_filiales.items()}
dic_filiales_largo[grupo_vanti] = "grupo_vanti"
dic_cumplimientos_reporte = {"VANTI S.A. ESP":"VANTI S.A. ESP.",
                            grupo_vanti:grupo_vanti,
                            "GAS NATURAL CUNDIBOYACENSE SA ESP":"GAS NATURAL CUNDIBOYACENCE S.A. ESP.",
                            "GAS NATURAL DEL CESAR S.A. EMPRESA DE SERVICIOS PUBLICOS":"GAS NATURAL DEL CESAR S.A. ESP.",
                            'GAS NATURAL DEL ORIENTE SA ESP':'GAS NATURAL DE ORIENTE S.A. ESP.'}
dic_estratos = mod_1.leer_archivos_json(ruta_constantes+"sector_consumo_estrato.json")["datos"]
dic_industrias = mod_1.leer_archivos_json(ruta_constantes+"sector_consumo_industrias.json")["datos"]
dic_industrias_grupos = mod_1.leer_archivos_json(ruta_constantes+"sector_consumo_industrias_grupos.json")["datos"]
ruta_fuente = ruta_fuentes+"Muli.ttf"
ruta_fuente_negrilla = ruta_fuentes+"Muli-Bold.ttf"
custom_font = FontProperties(fname=ruta_fuente)

def union_listas_df_trimestre(df):
    lista = []
    for i in range(len(df)):
        lista.append(str(df['Periodo_reportado'][i]).replace('TRIM_','Trimestre ')+'\n'+str(df['Anio_reportado'][i]).replace('np.int64(','').replace(')',''))
    df['Periodo_reportado_Periodo_reportado'] = lista
    return df

def union_listas_df_fecha(df, sep=False, anio=None, mes=None):
    if sep:
        llave1 = "Mes reportado"
        llave2 = "Anio reportado"
    else:
        llave1 = "Mes_reportado"
        llave2 = "Anio_reportado"
    if anio and mes:
        llave1 = mes
        llave2 = anio
    lista = []
    for i in range(len(df)):
        lista.append(str(df[llave1][i])+'\n'+str(df[llave2][i]))
    df['Fecha'] = lista
    return df

def informar_imagen(archivo):
    texto = mod_1.acortar_nombre(archivo)
    print(f"\nSe creó la imagen {texto}\n")

def suma_listas_pos(pos, matriz):
    lista = [0]*24
    for i in range(len(matriz)):
        if i < pos:
            for j in range(len(matriz[0])):
                lista[j] += float(matriz[i][j])
    return lista

def suma_matriz(pos, matriz):
    lista = [0]*len(matriz[0])
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if i < pos:
                lista[j] += float(matriz[i][j])
    return lista

def max_columna_matriz(matriz):
    lista = [0]*len(matriz[0])
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            lista[j] += matriz[i][j]
    return max(lista)


def suma_listas(matriz):
    lista = [0]*24
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            lista[j] += float(matriz[i][j])
    return lista

def grafica_barras_trimestre_reclamos(archivo):
    if os.path.exists(archivo):
        dic_grafica = {}
        df = pd.read_csv(archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje_reclamos_fact_10000'] = df['Porcentaje_reclamos_fact_10000'].str.replace(" %", "").astype(float)
        df_filtro = df[df["Filial"]!="Grupo Vanti"].reset_index(drop=True)
        df_filtro = union_listas_df_trimestre(df_filtro)
        lista_filiales = list(df_filtro['Filial'].unique())
        for filial in lista_filiales:
            df_filial = df_filtro[df_filtro['Filial'] == filial]
            lista_periodos = list(df_filial["Periodo_reportado_Periodo_reportado"].unique())
            lista_porcentaje = list(df_filial['Porcentaje_reclamos_fact_10000'])
            dic_grafica[filial] = lista_porcentaje
        cmap = LinearSegmentedColormap.from_list("", [dic_colores["rosa_p2"], dic_colores["rosa_p2"]])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        colors = [cmap(i/3) for i in range(4)]
        c = 0
        for filial in lista_filiales:
            valores = dic_grafica[filial]
            fig, ax = plt.subplots(figsize=(30, 17))
            x = np.arange(len(lista_periodos))
            ax.set_xticks(x)
            ax.set_xticklabels(lista_periodos)
            for i in range(len(lista_periodos)):
                ax.bar(x[i], valores[i], color=colors[i])
            for i in range(len(lista_periodos)):
                ax.text(x[i], valores[i] + 0.15, f"{valores[i]}%", ha='center', va='bottom', fontsize=42, color=colors[0])
            ax.tick_params(axis='x', colors=dic_colores["azul_v"],labelsize=32)
            ax.tick_params(axis='y', colors=dic_colores["azul_v"],size=0)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.text(x=-0.9, y=limite_facturas+0.1, s=f'{limite_facturas} %', color=dic_colores["azul_v"], fontsize=36)
            ax.axhline(xmin=-0.4, xmax=2, y=limite_facturas, linestyle='--', color=dic_colores["azul_v"], label=f'Límite regulatorio ({limite_facturas}%)',linewidth=6)
            ax.legend(bbox_to_anchor=(0.5, -0.08), loc='upper center',
                        borderaxespad=0.0, fontsize=32, labelcolor=dic_colores["azul_v"])
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_xlim(-0.9,3.6)
            lista_archivo = archivo.split("\\")
            lista_archivo.insert(-1, "Imagenes")
            archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
            n_imagen = archivo_copia.replace('.csv',f'_{filial}.png')
            plt.savefig(n_imagen, transparent=True)
            plt.close()
            if c == 0:
                c+=1
                imagen = Image.open(n_imagen)
                recorte = (1100, 1428, imagen.width-1000, imagen.height)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(archivo_copia.replace('.csv','_limite.png'))
            imagen = Image.open(n_imagen)
            recorte = (330, 50, imagen.width-220, imagen.height-70)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)
            informar_imagen(n_imagen)

def velocimetro_cumplimientos_regulatorios(archivo, fecha):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje_cumplimiento'] = df['Porcentaje_cumplimiento'].str.replace(" %", "").astype(float)
        lista = ["Incumplido","Certificado Extemporaneo","Certificado en plazo"]
        lista = ["Fuera de plazo","En plazo"]
        df['Estado'] = df['Estado'].str.lower().astype(str)
        df['Estado'] = df['Estado'].str.replace("incumplido","Fuera de plazo").replace("certificado extemporaneo","En plazo").replace("certificado en plazo","En plazo").astype(str)
        lista_filiales = list(df["Filial"].unique())
        for filial in lista_filiales:
            dic_df = {}
            dic_cantidad_reportes = {}
            df_filial = df[df["Filial"]==filial].reset_index(drop=True)
            lista_estado = list(df_filial["Estado"].unique())
            for estado in lista_estado:
                df_estado = df_filial[df_filial["Estado"]==estado].reset_index(drop=True)
                porcentaje = round(df_estado["Porcentaje_cumplimiento"].sum(),2)
                dic_cantidad_reportes[estado] = estado+" ("+str(df_estado["Cantidad_reportes"].sum())+" - "+str(porcentaje)+" %)"
                dic_df[estado] = porcentaje
            ordenadas_llaves = sorted(dic_df, key=lambda x: lista.index(x))
            dic_df = {k: dic_df[k] for k in ordenadas_llaves}
            data = {}
            for llave, valor in dic_df.items():
                data[dic_cantidad_reportes[llave]] = valor
            values = list(data.values())
            colors = ['red','green']
            labels = list(data.keys())
            fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': 'polar'})
            start = 0
            for i, value in enumerate(values):
                end = start + (value / 100) * np.pi
                ax.barh(1, end - start, left=start, height=0.5, color=colors[i],edgecolor='none')
                mid_angle = (start + end)  # Ángulo medio de cada sección
                if value < 30:
                    ax.text(mid_angle*0.5, 1.8, f'{value}%', ha='center', va='center', fontsize=18, color=colors[i])
                else:
                    ax.text(mid_angle*0.5, 1.5, f'{value}%', ha='center', va='center', fontsize=18, color=colors[i])
                start = end
            ax.set_yticklabels([])
            ax.set_xticks([])
            ax.spines['polar'].set_visible(False)
            ax.xaxis.set_visible(False)  # Hacer que el eje X no sea visible
            ax.yaxis.set_visible(False)
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(labels[i]),
                                                markerfacecolor=colors[i], markersize=10)
                                        for i in range(len(colors))]
            ax.legend(reversed(legend_handles), reversed(labels), loc='lower center', bbox_to_anchor=(0.5, 0.31), fontsize=14, ncol=1)
            plt.title(f'Oportunidad en la certifiación de\n reportes regulatorios para\n{dic_cumplimientos_reporte[filial]} (Acumulado año)', y=0.8, color=colors[-1], fontsize=18)
            ax.set_ylim(-0.01, 3.2)
            ax.grid(False)
            lista_archivo = archivo.split("\\")
            lista_archivo.insert(-1, "Imagenes")
            archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
            n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[dic_cumplimientos_reporte[filial]]}.png")
            plt.savefig(n_imagen)
            plt.close()
            imagen = Image.open(n_imagen)
            if filial == grupo_vanti:
                recorte = (240, 125, imagen.width-240, imagen.height - 285)
            else:
                recorte = (120, 125, imagen.width-110, imagen.height - 285)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)
            informar_imagen(n_imagen)

def grafica_matriz_requerimientos(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje_entidad'] = df['Porcentaje_entidad'].str.replace(" %", "").astype(float)
        labels = list(df["Categoria_entidad"])
        sizes = list(df["Cantidad"])
        colors = ["#ea7916","#2db6cf","#4eb6a8","#815081"]
        plt.figure(figsize=(8.3,8))
        plt.pie(sizes, labels=labels, colors=colors, autopct=lambda p : '{:.0f}'.format(p * sum(df['Cantidad']) / 100), textprops={'fontsize': 29,'color':'white'}, wedgeprops={'linewidth': 10, 'edgecolor': 'none'},startangle=90, explode=[0.05, 0.05, 0.05, 0.05])
        plt.legend(bbox_to_anchor=(0.5, 0.01), loc='upper center',
                                ncol=2, borderaxespad=0.0, fontsize=26)
        plt.title("Cantidad de requerimientos solicitados \n(Acumulado año)", fontsize=30, color=colors[-1], y=0.97)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        n_imagen = archivo_copia.replace(".csv", ".png")
        plt.savefig(n_imagen)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (35, 30, imagen.width-20, imagen.height)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)

def cambio_matriz_AOM(matriz):
    nueva_matriz = []
    for i in range(len(matriz)):
        lista = []
        for j in range(len(matriz[0])):
            if i == 0:
                lista.append(matriz[i][j])
            else:
                lista.append(nueva_matriz[i-1][j]+matriz[i][j])
        nueva_matriz.append(lista)
    return nueva_matriz

def grafica_gastos_AOM(archivo, anio):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje gastos'] = df['Porcentaje gastos'].str.replace(" %", "").astype(float)
        df['Valor'] = df['Valor'].astype(float)
        df['Valor millones'] = (round(df['Valor'] / 1e12,2)).astype(str) + 'B'
        df['Valor millones m'] = (round(df['Valor'] / 1e9,2)).astype(str) + ''
        df_anio = df[(df["Año"]==anio)&(df["Filial"]==grupo_vanti)]
        sizes = list(df_anio["Valor"])
        lista_porcentajes = list(df_anio["Porcentaje gastos"])
        labels = list(df_anio["Negocio"])
        colors = [dic_colores["azul_agua_v"],dic_colores["naranja_v"],dic_colores["morado_v"],dic_colores["verde_v"]]
        fig, ax = plt.subplots(figsize=(13,13))
        wedges, texts, autotexts = ax.pie(sizes,
                                    labels=None,
                                    autopct=lambda p : '{:.2f} B'.format(p * sum(sizes)/1e12),
                                    startangle=90,
                                    textprops={'fontsize': 27,'color':'white'},
                                    wedgeprops={'linewidth': 4, 'edgecolor': 'none'},
                                    explode=[0.05] * len(labels),
                                    labeldistance=1.1,
                                    colors=colors)
        for i, (wedge, pct) in enumerate(zip(wedges, lista_porcentajes)):
            ang = ((wedge.theta1 + wedge.theta2)/2)
            text = f'{pct:.1f}%'
            curved_text(text, ang, 1.14, ax, colors[i])
        plt.legend(labels,bbox_to_anchor=(0.5, -0.03), loc='upper center',
                                ncol=2, borderaxespad=0.0, fontsize=25)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        n_imagen = archivo_copia.replace(".csv", "_pie.png")
        plt.savefig(n_imagen, transparent=True)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (0, 130, imagen.width, imagen.height)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)
        matriz_1 = []
        matriz_2 = []
        matriz_3 = []
        colors = [dic_colores["azul_agua_v"],dic_colores["morado_v"],dic_colores["verde_v"]]
        df_filial = df[df["Filial"] == grupo_vanti].reset_index(drop=True)
        lista_negocios_agrupados = []
        for i in range(len(df_filial["Negocio"])):
            negocio = df_filial["Negocio"][i]
            if "Otros" in negocio:
                lista_negocios_agrupados.append("Otros DIS - COM")
            else:
                lista_negocios_agrupados.append(negocio)
        df_filial["Negocio_agru"] = lista_negocios_agrupados
        anios = list(df_filial["Año"].unique())
        lista_negocios = list(df_filial["Negocio_agru"].unique())
        for negocio in lista_negocios:
            lista_1 = []
            lista_2 = []
            lista_3 = []
            for anio in anios:
                df_filtro = df_filial[(df_filial["Negocio_agru"]==negocio)&((df_filial["Año"]==anio))]
                porcentaje = round(df_filtro["Porcentaje gastos"].sum(),2)
                lista_1.append(porcentaje)
                valor = df_filtro["Valor"].sum()
                lista_2.append(valor)
                valor_millones = f"{round(valor / 1e9,2)}"
                lista_3.append(valor_millones)
            matriz_1.append(lista_1)
            matriz_2.append(lista_2)
            matriz_3.append(lista_3)
        matriz_5 = cambio_matriz_AOM(matriz_2)
        bar_width = 0.7
        fig, ax = plt.subplots(figsize=(24,16))
        x = range(len(anios))
        v_max = max_columna_matriz(matriz_2)
        v_cambio = v_max*0.065
        for i in range(len(matriz_5)):
            if i == 0:
                ax.bar(x, matriz_2[0], bar_width, label=f'{lista_negocios[0]}', color=colors[0])
            else:
                ax.bar(x, matriz_2[i], bar_width, label=f'{lista_negocios[i]}', color=colors[i], bottom=matriz_5[i-1])
            for j in range(len(matriz_1[0])):
                valor = matriz_3[i][j]
                valor_1 = matriz_1[i][j]
                if i == 0:
                    ax.text(x[j], matriz_2[i][j]*0.4, f"{valor}", ha='center', fontsize=32, color="white", fontweight='bold')
                    ax.text(x[j]+(bar_width*0.6), matriz_2[i][j]*0.2, f"{valor_1} %", ha='center', fontsize=28, color=dic_colores["azul_v"], rotation=90)
                else:
                    ax.text(x[j], matriz_5[i-1][j]+(matriz_2[i][j]*0.4), f"{valor}", ha='center', fontsize=32, color="white", fontweight='bold')
                    ax.text(x[j]+(bar_width*0.6), matriz_5[i-1][j]+(matriz_2[i][j]*0.2), f"{valor_1} %", ha='center', fontsize=28, color=dic_colores["azul_v"], rotation=90)
        ax.set_ylim(0, v_max*1.03)
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1e9:.1f} m M'))
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_color(dic_colores["azul_v"])
            tick.label1.set_fontsize(27)
            tick.set_pad(8)
        ax.set_xticks(x)
        ax.set_xticklabels(anios, color=dic_colores["azul_v"], fontsize=28)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.legend(bbox_to_anchor=(0.5, -0.055), loc='upper center',
                    ncol=4, borderaxespad=0.0, fontsize=18)
        n_imagen = archivo_copia.replace(".csv", ".png")
        plt.savefig(n_imagen, transparent=True)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (440, 1482, imagen.width-380, imagen.height-52)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(archivo_copia.replace(".csv", "_limite.png"))
        imagen = Image.open(n_imagen)
        recorte = (80, 70, imagen.width-170, imagen.height-120)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)

def grafica_pie_tipo_usuario(archivo, fecha):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Anio reportado'] = df['Anio reportado'].astype(int)
        df = df[(df["Anio reportado"]==int(fecha[0]))].reset_index(drop=True)
        df = df[(df["Mes reportado"] == fecha[1])].reset_index(drop=True)
        df['Porcentaje Cantidad de usuarios'] = df['Porcentaje Cantidad de usuarios'].str.replace(" %", "").astype(float)
        df['Porcentaje Consumo m3'] = df['Porcentaje Consumo m3'].str.replace(" %", "").astype(float)
        lista_filiales = list(df["Filial"].unique())
        lista_colores = [[dic_colores["azul_c"],dic_colores["azul_o"]],
                        [dic_colores["rojo_c"],dic_colores["rojo_o"]],
                        [dic_colores["morado_c"],dic_colores["morado_o"]],
                        [dic_colores["amarillo_c"],dic_colores["amarillo_o"]],
                        [dic_colores["azul_agua_v"],dic_colores["morado_v"]]]
        dic = {"Consumo m3":"Metros cúbicos de GN consumidos para\n"}
        llave = list(dic.keys())[0]
        valor = list(dic.values())[0]
        for pos in range(len(lista_filiales)):
            filial = lista_filiales[pos]
            df_filtro = df[(df["Filial"]==filial) & (df["Tipo de usuario"]!="Total") & (df["Sector de consumo"]=="Total")]
            labels = list(df_filtro["Tipo de usuario"])
            sizes = list(df_filtro[llave])
            plt.figure(figsize=(10,7))
            plt.pie(sizes, autopct=lambda p : '{:.2f} M'.format(p * sum(sizes) / 100000000), 
                    colors=lista_colores[pos], textprops={'fontsize': 24,'color':'white'}, 
                    wedgeprops={'linewidth': 4, 'edgecolor': 'none'})
            plt.legend(bbox_to_anchor=(0.5, 0.01), loc='upper center',
                                    ncol=3, borderaxespad=0.0, fontsize=20, labels=labels)
            #plt.title(f'{valor}{filial} ({fecha[0]}/{fecha[1]})', color=lista_colores[pos][0], fontsize=25)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}_pie_consumo_m3.png")
            plt.savefig(n_imagen, transparent=True)
            plt.close()
            imagen = Image.open(n_imagen)
            recorte = (100, 40, imagen.width-100, imagen.height-20)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)
            informar_imagen(n_imagen)

def grafico_barras_consumo(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df, sep=True)
        lista_llaves = ["Regulados", "No regulados"]
        fig, ax = plt.subplots(figsize=(20, 12))
        matriz = []
        bar_width = 0.75
        for llave in lista_llaves:
            df_filtro = df[(df['Filial'] == grupo_vanti) & (df["Tipo de usuario"] == llave)].reset_index(drop=True)
            df_filtro['Consumo m3 millones'] = (round(df_filtro['Consumo m3'] / 1000000,2)).astype(str) + ' M'
            lista_periodos = list(df_filtro["Fecha"].unique())
            lista_valores = list(df_filtro["Consumo m3"])
            matriz.append(lista_valores)
            lista_valores_millones = list(df_filtro["Consumo m3 millones"])
            x = np.arange(len(lista_periodos))
        for i in range(len(matriz)):
            if i == 0:
                ax.bar(x, matriz[0], bar_width, label=f'{matriz[0]}', color=dic_colores["rosa_p1"])
            else:
                ax.bar(x, matriz[i], bar_width, label=f'{matriz[i]}', color=dic_colores["azul_p1"], bottom=matriz[0])
            for j in range(len(matriz[0])):
                valor = round(matriz[i][j]/1e6,1)
                if i == 0:
                    ax.text(x[j], matriz[i][j]*0.2, f"{valor}", ha='center', fontsize=22, color="white", rotation=90, fontweight='bold')
                else:
                    ax.text(x[j], matriz[i-1][j]+(matriz[i][j]*0.3), f"{valor}", ha='center', fontsize=22, color="white", rotation=90, fontweight='bold')
                valor = matriz[i][j]+matriz[i-1][j]
                ax.text(x[j], (valor)*1.03, f"{round(valor/1e6,1)} M", ha='center', fontsize=17, color=dic_colores["azul_v"])
        ax.tick_params(axis='x', colors=dic_colores["azul_v"],labelsize=17)
        ax.tick_params(axis='y', colors=dic_colores["azul_v"],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.15)
        ax.set_yticks([])
        ax.set_yticklabels([])
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        ax.set_xticks(x)
        ax.set_xticklabels(lista_periodos)
        n_imagen = archivo_copia.replace('_reporte_consumo_sumatoria.csv','_consumo.png')
        colors = [dic_colores["rosa_p1"],dic_colores["azul_p1"]]
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=lista_llaves[i],
                                            markerfacecolor=colors[i], markersize=18)
                                    for i in range(len(lista_llaves))]
        ax.legend(handles=legend_handles, bbox_to_anchor=(0.5, -0.08), loc='upper center',
                            ncol=2, borderaxespad=0.0, fontsize=22)
        plt.savefig(n_imagen, transparent=True)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (0, 55, imagen.width, imagen.height)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)

def grafico_usuarios(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        nombre = archivo_copia.replace('_reporte_consumo_sumatoria.csv','_usuarios.png')
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df["Mes reportado"] = df['Mes reportado'].str[:3]
        df = union_listas_df_fecha(df, sep=True)
        df_filtro = df[(df['Filial'] == grupo_vanti) & (df["Tipo de usuario"] == "Total")].reset_index(drop=True)
        df_filtro["Diferencia Cantidad de usuarios"] = (round(df_filtro["Diferencia Cantidad de usuarios"])).astype(int)
        df_filtro["Cantidad de usuarios"] = (round(df_filtro["Cantidad de usuarios"])).astype(int)
        df_filtro["Cantidad de usuarios millones"] = (round(df_filtro["Cantidad de usuarios"] / 1000000,2)).astype(str) + ' M'
        lista_periodos = list(df_filtro["Fecha"])
        lista_usuarios = list(df_filtro["Cantidad de usuarios"])
        lista_usuarios_millones = list(df_filtro["Cantidad de usuarios millones"])
        lista_usuarios_nuevos = list(df_filtro["Diferencia Cantidad de usuarios"])
        lista_porcentaje = []
        for i in range(len(lista_periodos)):
            lista_porcentaje.append(str(round((lista_usuarios_nuevos[i] / lista_usuarios[i]) * 100,2))+" %")
        v_min = min(lista_usuarios)*0.988
        v_cambio = (v_min)*0.0005
        v_min1 = v_min-(v_cambio*3)
        v_max = max(lista_usuarios)*1.01
        v_min_ax1 = min(lista_usuarios_nuevos)*0.7
        v_max_ax1 = max(lista_usuarios_nuevos)*1.1
        fig, ax = plt.subplots(figsize=(24, 12))
        x = range(len(lista_periodos))
        bar_width = 0.75
        lista_colores = [dic_colores["azul_v"], "white"]
        line3, = ax.plot(lista_periodos, lista_usuarios, marker='o', label='Cantidad de usuarios (millones)', color=dic_colores["amarillo_v"], alpha=0.6)
        ax1 = ax.twinx()
        line2, = ax1.plot(lista_periodos, lista_usuarios_nuevos, marker='o', label='Nuevos usuarios', color=dic_colores["azul_v"], alpha=0.3)
        for i in range(len(lista_periodos)):
            ax.annotate(f'{lista_usuarios_millones[i]}', xy=(i, v_min1), xytext=(0, 10),
                        textcoords='offset points', ha='center', va='bottom', color=dic_colores["amarillo_v"], fontsize=24)
            ax1.annotate(f'{lista_usuarios_nuevos[i]}', xy=(i, lista_usuarios_nuevos[i]), xytext=(0, 10),
                        textcoords='offset points', ha='center', va='bottom', color=dic_colores["azul_v"], fontsize=24)
        ax.tick_params(axis='x', colors="white",labelsize=15)
        ax.tick_params(axis='y', colors="white",size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for spine in ax1.spines.values():
            spine.set_visible(False)
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax1.set_yticks([])
        ax1.set_yticklabels([])
        ax.set_xticks(x)
        ax.tick_params(axis='x')
        ax.set_xticklabels(lista_periodos, fontsize=24)
        ax.set_ylabel('Cantidad de usuarios (millones)', color=dic_colores["amarillo_v"], fontsize=25)
        ax.tick_params(axis='y', labelcolor=dic_colores["amarillo_v"])
        ax1.set_ylabel('Nuevos usuarios', color=dic_colores["azul_v"],fontsize=25)
        ax1.tick_params(axis='y', labelcolor=dic_colores["azul_v"])
        ax.set_ylim(v_min1, v_max)
        ax1.set_ylim(v_min_ax1, v_max_ax1)
        plt.savefig(nombre, transparent=True)
        plt.close()
        imagen = Image.open(nombre)
        recorte = (0, 140, imagen.width, imagen.height)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(nombre)
        informar_imagen(nombre)

def grafica_pie_usuarios(archivo, fecha, dic_metricas):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Anio reportado'] = df['Anio reportado'].astype(int)
        df =  df[(df["Anio reportado"]==int(fecha[0]))].reset_index(drop=True)
        df =  df[(df["Mes reportado"] == fecha[1])].reset_index(drop=True)
        df = df[(df["Filial"]!=grupo_vanti)&(df["Tipo de usuario"]!="Total")&(df["Sector de consumo"]!="Total")]
        df['Porcentaje Cantidad de usuarios'] = df['Porcentaje Cantidad de usuarios'].str.replace(" %", "").astype(float)
        lista_colores = [dic_colores["morado_v"],
                        dic_colores["azul_agua_v"],
                        dic_colores["naranja_v"],
                        dic_colores["verde_v"],
                        dic_colores["morado_c_v"],
                        dic_colores["azul_agua_c_v"]]
        lista_sector_consumo = list(df["Sector de consumo"].unique())
        dic = {"Regulados":{},
                "No regulados":{}}
        dic_total = {"Regulados":0,
                "No regulados":0}
        dic_metricas["usarios_residenciales"] = 0
        dic_metricas["usarios_no_residenciales"] = 0
        for sector_consumo in lista_sector_consumo:
            df_sector = df[df["Sector de consumo"] == sector_consumo]
            cantidad = df_sector["Cantidad de usuarios"].sum()
            if cantidad:
                if sector_consumo in dic_estratos:
                    if dic_estratos[sector_consumo] not in dic["Regulados"]:
                        dic["Regulados"][dic_estratos[sector_consumo]] = [0,0]
                    dic_metricas["usarios_residenciales"] +=  cantidad
                    dic["Regulados"][dic_estratos[sector_consumo]][0] += cantidad
                    dic_total["Regulados"] += cantidad
                elif sector_consumo in dic_industrias_grupos:
                    if dic_industrias_grupos[sector_consumo] not in dic["No regulados"]:
                        dic["No regulados"][dic_industrias_grupos[sector_consumo]] = [0,0]
                    dic_metricas["usarios_no_residenciales"] += cantidad
                    dic["No regulados"][dic_industrias_grupos[sector_consumo]][0] += cantidad
                    dic_total["No regulados"] += cantidad
        total = dic_total["No regulados"]+dic_total["Regulados"]
        for llave, dic_llave in dic.items():
            lista_labels = list(dic_llave.keys())
            lista_valores = []
            lista_porcentajes = []
            lista_porcentajes_str = []
            for sector_consumo, lista_sector_consumo in dic_llave.items():
                dic[llave][sector_consumo][1] = round(dic[llave][sector_consumo][0]/dic_total[llave]*100,2)
                lista_valores.append(dic[llave][sector_consumo][0])
                lista_porcentajes.append(dic[llave][sector_consumo][1])
            nueva_lista_labels = []
            for i in range(len(lista_labels)):
                if lista_labels[i] == "Comercializadoras / Transportadores":
                    nueva_lista_labels.append("Comercia. /\nTranspor.")
                else:
                    nueva_lista_labels.append(f"{lista_labels[i]}")
                lista_porcentajes_str.append(str(round(lista_porcentajes[i],1))+" %")
            labels = nueva_lista_labels
            fig, ax = plt.subplots(figsize=(16,14))
            sizes = [360/len(lista_valores)]*len(lista_valores)
            v_lista_colores = lista_colores
            if llave == "Regulados":
                texto = f"Usuarios residenciales del {grupo_vanti}"
                wedges, texts, autotexts = ax.pie(sizes,
                                    labels=lista_porcentajes_str,
                                    autopct='%1.1f%%',
                                    pctdistance=1.3,
                                    startangle=0,
                                    labeldistance=1.68,
                                    textprops={'fontsize': 0.0001},
                                    wedgeprops={'linewidth': 4, 'edgecolor': 'none', 'width': 0.6},
                                    explode=[0.05] * len(labels),
                                    colors=lista_colores)
                texto_1 = str(round((dic_total["Regulados"]/total)*100,2))+" %"
                plt.text(0, 0, texto_1, ha='center', va='center', fontsize=50, color=v_lista_colores[0])
                for i, (wedge, pct) in enumerate(zip(wedges, lista_porcentajes)):
                    ang = ((wedge.theta1 + wedge.theta2)/2)
                    text = f'{pct:.1f}%'
                    ubicar_porcentajes(text, ang, 1.3, ax, v_lista_colores[i])
            else:
                texto = f"Usuarios no residenciales del {grupo_vanti}"
                wedges, texts, autotexts = ax.pie(sizes,
                                    labels=lista_porcentajes_str,
                                    autopct='',
                                    startangle=0,
                                    labeldistance=0.68,
                                    textprops={'fontsize': 0.00001},
                                    wedgeprops={'linewidth': 4, 'edgecolor': 'none', 'width': 0.6},
                                    explode=[0.05] * len(labels),
                                    colors=lista_colores)
                texto_1 = str(round((dic_total["No regulados"]/total)*100,2))+" %"
                plt.text(0, 0, texto_1, ha='center', va='center', fontsize=50, color=v_lista_colores[0])
                for i, (wedge, pct) in enumerate(zip(wedges, lista_porcentajes)):
                    ang = ((wedge.theta1 + wedge.theta2)/2)
                    text = f'{pct:.1f}%'
                    ubicar_porcentajes(text, ang, 1.3, ax, v_lista_colores[i])
            plt.gca().set_aspect('equal')
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.subplots_adjust(bottom=0.18)
            texto = llave.lower().replace(" ","_")
            n_imagen = archivo_copia.replace("_reporte_consumo_sumatoria.csv", f"_pie_{texto}.png")
            plt.savefig(n_imagen, transparent=True)
            plt.close()
            imagen = Image.open(n_imagen)
            recorte = (70, 110, imagen.width-30, imagen.height-180)
            imagen_recortada = imagen.crop(recorte)
            if llave == "Regulados":
                ruta_imagen = ruta_constantes+"residencial.png"
                lista_esp = [[965,350],#2
                            [695,195],#1
                            [430,350],#6
                            [430,630],#5
                            [695,780],#4
                            [965,630]]#3
                if os.path.exists(ruta_imagen):
                    for i in range(len(labels)):
                        esp = lista_esp[i]
                        imagen_recortada = colocar_imagen(imagen_recortada, esp, ruta_imagen)
                        texto = labels[i]
                        esp[1] += 80
                        esp[0] += 50
                        imagen_recortada = ubicar_texto(imagen_recortada, esp, texto, color="white")
            else:
                llaves = list(dic["No regulados"].keys())
                lista_esp = [[920,290],
                            [575,195],
                            [375,435],
                            [595,740],
                            [905,610]]
                for i in range(len(llaves)):
                    llave = llaves[i]
                    ruta_imagen = ruta_constantes+dic_sectores_consumo_imagenes_pie[llave]
                    if os.path.exists(ruta_imagen):
                        esp = lista_esp[i]
                        imagen_recortada = colocar_imagen(imagen_recortada, esp, ruta_imagen, (140,140))
                        esp[1] += 120
                        esp[0] += 70
                        texto = labels[i]
                        imagen_recortada = ubicar_texto(imagen_recortada, esp, texto, color="white")
            imagen_recortada.save(n_imagen)
            informar_imagen(n_imagen)
        valor = dic_metricas["usarios_residenciales"]
        dic_metricas["usarios_residenciales"] = f"{round(valor/1e6,1)} M"
        valor = dic_metricas["usarios_no_residenciales"]
        dic_metricas["usarios_no_residenciales"] = f"{round(valor/1e3,3)}"
        return dic_metricas
    else:
        dic_metricas["usarios_residenciales"] = None
        dic_metricas["usarios_no_residenciales"] = None
        return dic_metricas

def ubicacion_imagen(nueva_imagen, espacio):
    ancho, alto = nueva_imagen.size
    tamanio = (abs(espacio[0][0]-espacio[1][0]),abs(espacio[0][1]-espacio[3][1]))
    if alto > tamanio[1]:
        escalar = tamanio[1]/alto
    else:
        escalar = alto/tamanio[1]
    if int(ancho*escalar) <= tamanio[0]:
        nueva_imagen = nueva_imagen.resize((int(ancho*escalar), tamanio[1]))
    else:
        nueva_imagen = nueva_imagen.resize((tamanio[0],int(alto*escalar)))
    ancho, alto = nueva_imagen.size
    posicion = (espacio[0][0]+(abs(espacio[1][0]-espacio[0][0]-ancho)//2),abs(espacio[0][1]))
    return nueva_imagen,posicion

def colocar_imagen(imagen, pos, nueva_imagen, tamanio=(100,100)):
    nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
    ancho, alto = nueva_imagen.size
    if alto > tamanio[1]:
        escalar = tamanio[1]/alto
    else:
        escalar = alto/tamanio[1]
    if int(ancho*escalar) <= tamanio[0]:
        nueva_imagen = nueva_imagen.resize((int(ancho*escalar), tamanio[1]))
    else:
        nueva_imagen = nueva_imagen.resize((tamanio[0],int(alto*escalar)))
    imagen.paste(nueva_imagen, pos, nueva_imagen)
    return imagen

def ubicar_texto(imagen_recortada, esp, texto, color="black"):
    x = esp[0]
    y = esp[1]
    dibujo = ImageDraw.Draw(imagen_recortada)
    fuente = ImageFont.truetype(ruta_fuente, 32)
    bbox = dibujo.textbbox((0, 0), texto, font=fuente)
    tamanio_texto = (bbox[2] - bbox[0], bbox[3] - bbox[1])
    dibujo.text((x - (tamanio_texto[0]*0.5), y), texto, fill=color, font=fuente)
    return imagen_recortada

def curved_text(text, theta, radius, ax, color):
    char_spacing = 5
    start_angle = theta - (len(text) * char_spacing) / 2
    lista_char = []
    lista_angle = []
    lista_rot = []
    for i, char in enumerate(text):
        if start_angle > 180:
            char_angle = start_angle + (i * char_spacing)
        else:
            char_angle = start_angle - (i * char_spacing)
        if char_angle > 360:
            char_angle -= 360
        if char_angle > 180:
            rotation = (char_angle + 90)
            char_angle = start_angle + (i * char_spacing)
        else:
            rotation = (char_angle - 90)
            char_angle = start_angle + (i * char_spacing)
        char_rad = np.deg2rad(char_angle)
        if char_angle > 360:
            char_angle -= 360
        #print(char, char_angle)
        lista_char.append(char)
        lista_angle.append(char_angle)
        lista_rot.append(rotation)
    if lista_angle[0] < 180:
        lista_angle.reverse()
    for i in range(len(lista_char)):
        ax.text(radius*np.cos(np.deg2rad(lista_angle[i])), radius*np.sin(np.deg2rad(lista_angle[i])), lista_char[i],
                rotation = lista_rot[i],
                ha='center',
                va='center',
                size=28,
                color=color)

def ubicar_porcentajes(text, ang, radius, ax, color,size=34):
    ax.text(radius*np.cos(np.deg2rad(ang)), radius*np.sin(np.deg2rad(ang)), 
        text,
        ha='center',
        va='center',
        size=size,
        color=color)

def grafica_tabla_sector_consumo(archivo, fecha):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Anio reportado'] = df['Anio reportado'].astype(int)
        df =  df[(df["Anio reportado"]==int(fecha[0]))].reset_index(drop=True)
        df =  df[(df["Mes reportado"] == fecha[1])].reset_index(drop=True)
        df_filiales = df[(df["Filial"] != grupo_vanti) & (df["Tipo de usuario"] != "Total") & (df["Sector de consumo"] != "Total")].reset_index(drop=True)
        dic_sectores_compilado = {}
        for i in range(len(df_filiales)):
            tipo_usuario = df_filiales["Tipo de usuario"][i]
            if tipo_usuario not in dic_sectores_compilado:
                dic_sectores_compilado[tipo_usuario] = {}
            sector_consumo = dic_sectores_consumo[tipo_usuario][df_filiales["Sector de consumo"][i]]
            if sector_consumo not in dic_sectores_compilado[tipo_usuario]:
                dic_sectores_compilado[tipo_usuario][sector_consumo] = 0
            dic_sectores_compilado[tipo_usuario][sector_consumo] += df_filiales["Consumo m3"][i]
        for tipo_usuario, dic in dic_sectores_compilado.items():
            ordenadas_llaves = sorted(dic, key=lambda x: dic_sectores_consumo_ordenados[tipo_usuario].index(x))
            dic_sectores_compilado[tipo_usuario] = {k: dic[k] for k in ordenadas_llaves}
        dic_df = {"Sector de consumo":[],
                "Tipo de usuario":[],
                "Consumo (Millones m3)":[]}
        for tipo_usuario, dic in dic_sectores_compilado.items():
            for llave, valor in dic.items():
                dic_df["Sector de consumo"].append(llave)
                dic_df["Tipo de usuario"].append(tipo_usuario)
                dic_df["Consumo (Millones m3)"].append(f"{round(valor/1000000,1)}")
        df1 = pd.DataFrame(dic_df)
        fig, ax = plt.subplots(figsize=(15, 5.5))  # Ajusta el tamaño de la imagen si es necesario
        ax.axis('tight')
        ax.axis('off')
        tbl = ax.table(cellText=df1.values, colLabels=df1.columns, cellLoc='center', loc='center')
        table_bbox = tbl.get_window_extent(fig.canvas.get_renderer())
        table_width = table_bbox.width
        table_height = table_bbox.height
        for (i, j), cell in tbl.get_celld().items():
            text = cell.get_text().get_text()
            if i == 0:
                cell.set_text_props(weight='bold', color='#071c8e')
                cell.set_edgecolor('black')
            elif j == 0:
                cell.set_text_props(weight='bold', color='#0d2cd4')
                cell.set_edgecolor('black')
                y_pos = (1 - (i + 2) / (len(df1) + 1))*2-0.16
                ruta_logo = ruta_constantes+dic_sectores_consumo_imagenes[text]
                add_image(ax, ruta_logo, 0.16, y_pos, zoom=0.15)
            else:
                cell.set_text_props(color='#3250f3')
                cell.set_edgecolor('black')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(16)
        tbl.scale(1.55, 2.8*2)
        ax.set_title(f"Demanda de Gas Natural para el {grupo_vanti} ({fecha[0]}/{fecha[1]})", y=1.55, weight="bold", color='#071c8e', fontsize=24)
        n_imagen = archivo_copia.replace(".csv", "_tabla_consumo.png")
        plt.savefig(n_imagen,bbox_inches='tight', dpi=300)
        plt.close()
        informar_imagen(n_imagen)

def add_image(ax, img, x, y, zoom=0.1):
    img = plt.imread(img)
    width, height = 50, 50
    zoom = min(width / img.shape[1], height / img.shape[0])
    im = OffsetImage(img, zoom=zoom)
    #img = plt.imread(img_path)
    #img = resize(img, (100, 100))
    im = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(im, (x, y), xycoords='axes fraction', 
                        frameon=False, box_alignment=(0.5, 0.5))
    ax.add_artist(ab)

def grafica_barras_compensacion(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df)
        df_filtro = df[df['Filial'] == grupo_vanti].reset_index(drop=True)
        df_filtro = union_listas_df_fecha(df_filtro)
        df_filtro['Valor_compensado_millones'] = (round(df_filtro['Valor_compensado'] / 1000000,2)).astype(str) + ' M'
        lista_periodos = list(df_filtro["Fecha"].unique())
        lista_valores = list(df_filtro["Valor_compensado"].unique())
        lista_valores_millones = list(df_filtro["Valor_compensado_millones"].unique())
        cmap = LinearSegmentedColormap.from_list("", [dic_colores["blanco"],dic_colores["blanco"]])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        fig, ax = plt.subplots(figsize=(16, 10))
        x = np.arange(len(lista_periodos))
        bar_width = 0.75
        colors = [cmap(i/11.0) for i in range(12)]  # Use the custom color map
        for i in range(12):
            ax.bar(lista_periodos[i], lista_valores[i], width=bar_width, color=colors[i])
            ax.text(lista_periodos[i], lista_valores[i] + 2, f"{lista_valores_millones[i]}", ha='center', va='bottom', fontsize=18, color=colors[i])
        #ax.set_title(f'Valor compensado por el {grupo_vanti} ($ COP)', color=colors[0],fontsize=25, y=1.05)
        ax.tick_params(axis='x', colors=colors[0],labelsize=15)
        ax.tick_params(axis='y', colors=colors[0],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.95, bottom=0.08)
        ax.set_yticks([])
        ax.set_yticklabels([])
        n_imagen = archivo_copia.replace('.csv','.png')
        plt.savefig(n_imagen, transparent=True)
        plt.close()
        informar_imagen(n_imagen)

def grafica_DS(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Mes_reportado'] = df['Mes_reportado'].str[:3]
        df['Porcentaje_atendidos'] = df['Porcentaje_atendidos'].str.replace(" %", "").astype(float)
        df = union_listas_df_fecha(df)
        lista_filiales = list(df["Filial"].unique())
        lista_periodos = list(df["Fecha"].unique())
        lista_colores = [dic_colores["azul_agua_v"], dic_colores["naranja_v"], dic_colores["morado_v"], dic_colores["verde_v"], dic_colores["azul_agua_c_v"], dic_colores["naranja_c_v"], dic_colores["morado_c_v"], dic_colores["verde_c_v"]]
        for filial in lista_filiales:
            df_filial = df[df["Filial"] == filial].reset_index(drop=True)
            lista_mercado = list(df_filial["Mercado_relevante"].unique())
            lista_mercado_nombre = []
            fig, ax = plt.subplots(figsize=(40,26))
            x = range(len(lista_periodos))
            vmax = 0
            for j in range(len(lista_mercado)):
                id_mercado = lista_mercado[j]
                lista_porcentaje = []
                if str(id_mercado) in dic_mercados:
                    nombre_mercado = dic_mercados[str(id_mercado)]["Nombre_mercado"]
                    lista_mercado_nombre.append(nombre_mercado)
                    df_mercado = df_filial[df_filial["Mercado_relevante"] == id_mercado].reset_index(drop=True)
                    for fecha in lista_periodos:
                        df_fecha = df_mercado[df_mercado["Fecha"] == fecha].reset_index(drop=True)
                        if len(df_fecha):
                            lista_porcentaje.append(df_fecha["Porcentaje_atendidos"][0])
                        else:
                            lista_porcentaje.append(0)
                    print(len(lista_periodos), lista_periodos)
                    print(len(lista_porcentaje), lista_porcentaje)
                    if max(lista_porcentaje) > vmax:
                        vmax = max(lista_porcentaje)
                    line, = ax.plot(lista_periodos, lista_porcentaje, marker='o', label=nombre_mercado, color=lista_colores[j], markersize=60, alpha=0.6, linewidth=5)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.set_xticks(x)
            ax.tick_params(axis='x')
            ax.set_xticklabels(lista_periodos, fontsize=44, color=dic_colores["azul_v"])
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(lista_mercado_nombre[i]),
                                                markerfacecolor=lista_colores[i], markersize=40)
                                        for i in range(len(lista_mercado_nombre))]
            ax.legend(handles=legend_handles, bbox_to_anchor=(0.5, -0.08), loc='upper center',
                                ncol=len(lista_mercado_nombre), borderaxespad=0.0, fontsize=42)
            ax.yaxis.set_major_locator(ticker.FixedLocator(list(np.arange(0, vmax + 0.5, 0.5))))  # Especifica los valores en una lista
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x} %'))
            for tick in ax.yaxis.get_major_ticks():
                tick.label1.set_color(dic_colores["azul_v"])
                tick.label1.set_fontsize(48)
                tick.set_pad(8)
            ax.set_ylim(-0.1, vmax+0.2)
            ax.grid(axis='y', color='gray', linestyle='--', linewidth=3)
            dic_filiales_cambio = {valor: clave for clave, valor in dic_filiales.items()}
            nombre = archivo_copia.replace('.csv',f'_{dic_filiales_cambio[filial]}.png')
            plt.savefig(nombre, transparent=True)
            plt.close()
            imagen = Image.open(nombre)
            recorte = (0, 140, imagen.width, imagen.height)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(nombre)
            informar_imagen(nombre)

def cambio_lista_IRST(lista, v_min):
    lista_1 = []
    for i in lista:
        if i < v_min:
            v_min = i
        lista_1.append(round(i-porcentaje_ISRT,12))
    return lista_1, v_min

def cambio_lista_cumplimientos(matriz,lista_periodos):
    lista_cumplimientos = []
    for j in range(len(list(matriz[:,0]))):
        if matriz[j,0] == porcentaje_ISRT and matriz[j,1] == porcentaje_ISRT and matriz[j,2] == porcentaje_ISRT:
            lista_cumplimientos.append(True)
        else:
            lista_cumplimientos.append(False)
    lista_pos = []
    i = 0
    cantidad = len(lista_periodos)-1
    info_nueva_lista = []
    while i < len(lista_periodos):
        if not lista_cumplimientos[i]:
            lista_pos.append([lista_periodos[i]])
            info_nueva_lista.append((matriz[i,0],matriz[i,1],matriz[i,2]))
            i += 1
        else:
            if i+2 <= cantidad:
                if lista_cumplimientos[i+1] and lista_cumplimientos[i+2]:
                    lista_pos.append((lista_periodos[i],lista_periodos[i+2]))
                    info_nueva_lista.append((matriz[i,0],matriz[i,1],matriz[i,2]))
                    i+=3
                elif lista_cumplimientos[i+1]:
                    lista_pos.append((lista_periodos[i],lista_periodos[i+1]))
                    info_nueva_lista.append((matriz[i,0],matriz[i,1],matriz[i,2]))
                    i+=2
                else:
                    lista_pos.append([lista_periodos[i]])
                    info_nueva_lista.append((matriz[i,0],matriz[i,1],matriz[i,2]))
                    i += 1
            elif i+1 <= cantidad:
                if lista_cumplimientos[i+1]:
                    lista_pos.append((lista_periodos[i],lista_periodos[i+1]))
                    info_nueva_lista.append((matriz[i,0],matriz[i,1],matriz[i,2]))
                    i+=2
                else:
                    lista_pos.append((lista_periodos[i]))
                    info_nueva_lista.append((matriz[i,0],matriz[i,1],matriz[i,2]))
                    i += 1
            else:
                lista_pos.append([lista_periodos[i]])
                info_nueva_lista.append((matriz[i,0],matriz[i,1],matriz[i,2]))
                i += 1
    nueva_matriz = []
    v_min = float("inf")
    for j in range(3):
        lista = []
        for i in range(len(lista_pos)):
            if info_nueva_lista[i][j] < v_min:
                v_min = info_nueva_lista[i][j]
            lista.append(info_nueva_lista[i][j])
        nueva_matriz.append(lista)
    nueva_lista_periodos = []
    for i in range(len(lista_pos)):
        periodo = lista_pos[i]
        if len(periodo) == 1:
            nueva_lista_periodos.append(periodo[0].replace("\n"," / "))
        else:
            texto = periodo[0].replace("\n"," / ")+" -\n"+periodo[1].replace("\n"," / ")
            nueva_lista_periodos.append(texto)
    return nueva_lista_periodos, nueva_matriz, v_min

def grafica_barras_indicador_tecnico(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df)
        lista_filiales = list(df['Filial'].unique())
        cmap = LinearSegmentedColormap.from_list("Orange", ["#fd8c25","#fec692"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        lista_colores = [dic_colores["verde_v"],dic_colores["morado_v"],dic_colores["azul_agua_v"]]
        for filial in lista_filiales:
            dic_grafica = {}
            dic_grafica_100 = {}
            v_min = porcentaje_ISRT
            df_filial = df[df['Filial'] == filial].reset_index(drop=True)
            lista_periodos = list(df_filial["Fecha"])
            lista_indicadores = ["IPLI", "IO", "IRST_EG"]
            for indicador in lista_indicadores:
                if indicador == "IRST_EG":
                    dic_grafica["IRST-EG"],v_min = cambio_lista_IRST(list(df_filial["IRST_EG"]), v_min)
                    dic_grafica_100["IRST-EG"] = list(df_filial["IRST_EG"])
                else:
                    dic_grafica[indicador],v_min = cambio_lista_IRST(list(df_filial[indicador]), v_min)
                    dic_grafica_100[indicador] = list(df_filial[indicador])
            data_100 = np.array(list(dic_grafica_100.values())).T
            cantidad = len(list(dic_grafica.keys()))
            lista_indicadores = list(dic_grafica.keys())
            nueva_lista_periodos, nuevas_barras, v_min = cambio_lista_cumplimientos(data_100, lista_periodos)
            fig, ax = plt.subplots(figsize=(25, 14))
            bar_width = 0.3
            cmap = LinearSegmentedColormap.from_list("Orange", ["#fd8c25","#fec692"])
            x = np.arange(len(nueva_lista_periodos))
            for i in range(cantidad):
                bars = ax.bar(x + i * bar_width, nuevas_barras[i], bar_width, label=lista_indicadores[i], color=lista_colores[i])
                for bar, value in zip(bars.patches, nuevas_barras[i]):
                    if value == porcentaje_ISRT:
                        value = int(value)
                        ax.text(bar.get_x() + bar.get_width()/2, 100.2, f"{value}%", color=dic_colores["azul_v"], ha="center", va="bottom", fontsize=28, rotation=90)
                    else:
                        ax.text(bar.get_x() + bar.get_width()/2, 100.2, f"{value:.2f}%", color=dic_colores["azul_v"], ha="center", va="bottom", fontsize=28, rotation=90)
            ax.set_xticks(x + bar_width)
            ax.set_xticklabels(nueva_lista_periodos, color=dic_colores["azul_v"], fontsize=16)
            lista = ["IPLI", "IO", "IRST-EG"]
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(lista[i]),
                                            markerfacecolor=lista_colores[i], markersize=18)
                                    for i in range(len(lista))]
            ax.legend(handles=legend_handles, bbox_to_anchor=(0.5, -0.075), loc='upper center',
                            ncol=len(lista), borderaxespad=0.0, fontsize=24)
            ax.set_ylim(v_min-2, 101)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.set_yticks([])
            ax.set_yticklabels([])
            n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}.png")
            plt.savefig(n_imagen, transparent=True)
            plt.close()
            c = 0
            if c == 0:
                c+=1
                imagen = Image.open(n_imagen)
                recorte = (950, 1330, imagen.width-870, imagen.height-20)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(archivo_copia.replace('.csv','_limite.png'))
            imagen = Image.open(n_imagen)
            recorte = (380, 150, imagen.width-300, imagen.height-75)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)
            informar_imagen(n_imagen)

def grafica_pie_subsidios(archivo,fecha):
    anio = int(fecha[0])
    mes = fecha[1].capitalize()
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df, sep=True)
        df_filiales = df[(df["Filial"]!=grupo_vanti)&(df["Anio reportado"]==anio)&(df["Mes reportado"]==mes)&(df["Tipo de usuario"]=="Regulados")&(df["Sector de consumo"]!="Total")]
        lista_sector_consumo = list(df_filiales["Sector de consumo"].unique())
        lista_cantidad = []
        lista_labels = []
        lista_porcentajes = []
        for sector_consumo in lista_sector_consumo:
            if sector_consumo in dic_estratos:
                df_sector = df_filiales[df_filiales["Sector de consumo"]==sector_consumo]
                lista_cantidad.append(abs(df_sector["Subsidios"].sum()))
                lista_labels.append(dic_estratos[sector_consumo])
        for i in lista_cantidad:
            lista_porcentajes.append((i/sum(lista_cantidad))*100)
        labels = lista_labels
        sizes = lista_cantidad
        colors = [dic_colores["naranja_v"],dic_colores["azul_agua_v"]]
        fig, ax = plt.subplots(figsize=(11,10))
        #plt.pie(sizes, labels=labels, colors=colors, autopct=lambda p : '{:.2f} m M'.format(p * sum(lista_cantidad) / 1000000000), textprops={'fontsize': 24,'color':'white'}, wedgeprops={'linewidth': 5, 'edgecolor': 'none'},startangle=90, explode=[0.02, 0.02],pctdistance=0.5)
        wedges, texts, autotexts = ax.pie(sizes,
                                    labels=None,
                                    autopct=lambda p : '{:.2f} m M'.format(p * sum(lista_cantidad) / 1000000000),
                                    startangle=90,
                                    textprops={'fontsize': 24,'color':'white'},
                                    wedgeprops={'linewidth': 4, 'edgecolor': 'none'},
                                    explode=[0.05] * len(labels),
                                    colors=colors)
        for i, (wedge, pct) in enumerate(zip(wedges, lista_porcentajes)):
            ang = ((wedge.theta1 + wedge.theta2)/2)
            text = f'{pct:.1f}%'
            curved_text(text, ang, 1.14, ax, colors[i])
        plt.legend(labels,bbox_to_anchor=(0.5, 0.055), loc='upper center',
                                ncol=2, borderaxespad=0.0, fontsize=24)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        n_imagen = archivo_copia.replace("_reporte_consumo_subsidio_sumatoria.csv", "_pie_subsidio.png")
        plt.savefig(n_imagen, transparent=True)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (0, 130, imagen.width-0, imagen.height-80)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)

def grafica_barras_subsidios(archivo, dic_metricas):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df, sep=True)
        anio_1 = 2023
        mes_1 = "Diciembre"
        llave_1 = "Transportadores de gas natural"
        filial_1 = "VANTI S.A. ESP."
        v1 = df[(df["Anio reportado"]==anio_1)&((df["Mes reportado"]==mes_1))&(df["Filial"]==filial_1)&(df["Sector de consumo"]==llave_1)]["Contribuciones"].sum()
        if v1 > 0:
            df.loc[(df['Filial'] == grupo_vanti)&(df["Tipo de usuario"]=="Total")&(df["Anio reportado"]==anio_1)&((df["Mes reportado"]==mes_1)), "Contribuciones"] -= v1
            texto_v1 = f"El valor de las contribuciones para los {llave_1} en \n{filial_1} ({mes_1}/{anio_1}) fue de {round(v1/1e9,1)} m M"
        else:
            texto_v1 = None
        dic_metricas["Subsidios"] = texto_v1
        df_filtro = df[(df["Filial"]!=grupo_vanti)&(df["Tipo de usuario"]=="Regulados")&(df["Sector de consumo"]!="Total")]
        lista_labels = []
        matriz = []
        lista_sector_consumo = list(df_filtro["Sector de consumo"].unique())
        for sector_consumo in lista_sector_consumo:
            lista_labels.append(dic_estratos[sector_consumo])
            df_sector_consumo = df_filtro[df_filtro["Sector de consumo"] == sector_consumo]
            lista_sector_conmsumo = []
            lista_fechas = list(df_sector_consumo["Fecha"].unique())
            for fecha in lista_fechas:
                df_fecha = df_sector_consumo[df_sector_consumo["Fecha"]==fecha]
                lista_sector_conmsumo.append(abs(df_fecha["Subsidios"].sum()))
            matriz.append(lista_sector_conmsumo)
        df_filtro = df[(df['Filial'] == grupo_vanti)&(df["Tipo de usuario"]=="Total")].reset_index(drop=True)
        df_filtro['Contribuciones_millones'] = (round(df_filtro['Contribuciones'] / 1000000,2)).astype(str) + ' M'
        lista_valores = list(df_filtro["Contribuciones"])
        matriz.append(lista_valores)
        lista_valores_millones = list(df_filtro["Contribuciones_millones"])
        lista_mme = []
        for i in range(len(matriz[0])):
            valor = matriz[0][i]+matriz[1][i]
            if matriz[2][i] < valor:
                valor -= matriz[2][i]
            else:
                valor = 0
            lista_mme.append(valor)
        matriz.append(lista_mme)
        colors = [dic_colores["naranja_v"], dic_colores["azul_agua_v"], dic_colores["morado_v"], dic_colores["rojo_c"]]
        lista_labels = ["Estrato 1", "Estrato 2", "Contribuciones", "CxC MME"]
        fig, ax = plt.subplots(figsize=(36,14))
        x = np.arange(len(lista_fechas))
        bar_width = 0.3
        E1 = ax.bar(x - bar_width/2, matriz[0], bar_width, label=lista_labels[0], color=colors[0])
        Con = ax.bar(x + bar_width/2, matriz[2], bar_width, label=lista_labels[2], color=colors[2])
        E2 = ax.bar(x - bar_width/2, matriz[1], bar_width, label=lista_labels[1], bottom=matriz[0], color=colors[1])
        mme = ax.bar(x + bar_width/2, matriz[3], bar_width, label=lista_labels[3], bottom=matriz[2], color=colors[3])
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                valor = round(matriz[i][j]/1e9,1)
                if i == 0 or i == 2:
                    if i == 0:
                        x1 = x[j] - bar_width/2
                    else:
                        x1 = x[j] + bar_width/2
                    ax.text(x1, matriz[i][j]*0.2, f"{valor}", ha='center', fontsize=25, color="white", rotation=90)
                else:
                    if i == 1:
                        x1 = x[j] - bar_width/2
                        ax.text(x1, matriz[i-1][j]+(matriz[i][j]*0.3), f"{valor}", ha='center', fontsize=25, color="white", rotation=90)
                    else:
                        x1 = x[j] + bar_width/2
                        ax.text(x1, matriz[i-1][j]+(matriz[i][j]*0.3), f"{valor}", ha='center', fontsize=28, color="white", rotation=90, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(lista_fechas, color=dic_colores["azul_v"], fontsize=21)
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=lista_labels[i],
                                            markerfacecolor=colors[i], markersize=18)
                                    for i in range(len(lista_labels))]
        ax.legend(handles=legend_handles, bbox_to_anchor=(0.5, -0.09), loc='upper center',
                            ncol=4, borderaxespad=0.0, fontsize=22)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1000000000:.0f} m M'))
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_color(dic_colores["azul_v"])
            tick.label1.set_fontsize(27)
            tick.set_pad(6)
        n_imagen = archivo_copia.replace("_reporte_consumo_subsidio_sumatoria.csv", "_subsidios_estratos.png")
        plt.savefig(n_imagen, transparent=True)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (100, 50, imagen.width-130, imagen.height)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)
        return dic_metricas

def grafica_barras_contribuciones(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df, sep=True)
        df_filtro = df[(df['Filial'] == grupo_vanti)&(df["Tipo de usuario"]=="Total")].reset_index(drop=True)
        df_filtro['Contribuciones_millones'] = (round(df_filtro['Contribuciones'] / 1000000,2)).astype(str) + ' M'
        lista_periodos = list(df_filtro["Fecha"])
        lista_valores = list(df_filtro["Contribuciones"])
        lista_valores_millones = list(df_filtro["Contribuciones_millones"])
        cmap = LinearSegmentedColormap.from_list("Azul", ["#815081","#c0a8c0"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        fig, ax = plt.subplots(figsize=(16, 10))
        x = np.arange(len(lista_periodos))
        bar_width = 0.75
        colors = [cmap(i/11.0) for i in range(12)]  # Use the custom color map
        for i in range(12):
            ax.bar(lista_periodos[i], lista_valores[i], width=bar_width, color=colors[i])
            ax.text(lista_periodos[i], lista_valores[i] + 2, f"{lista_valores_millones[i]}", ha='center', va='bottom', fontsize=16, color=colors[0])
        ax.set_title(f'Contribuciones generadas por el {grupo_vanti} ($ COP)', color=colors[0],fontsize=32, y=1.03)
        ax.tick_params(axis='x', colors=colors[0],labelsize=15)
        ax.tick_params(axis='y', colors=colors[0],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.07)
        ax.set_yticks([])
        ax.set_yticklabels([])
        n_imagen = archivo_copia.replace("_reporte_consumo_subsidio_sumatoria.csv", "_contribuciones.png")
        plt.savefig(n_imagen)
        plt.close()
        informar_imagen(n_imagen)

def grafica_barras_indicador_tecnico_minutos(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df)
        df['Porcentaje_cantidad_eventos'] = df['Porcentaje_cantidad_eventos'].str.replace(" %", "").astype(float)
        lista_filiales = list(df['Filial'].unique())
        c = 0
        for filial in lista_filiales:
            dic_grafica = {}
            df_filial = df[df['Filial'] == filial].reset_index(drop=True)
            lista_periodos = list(df_filial["Fecha"].unique())
            lista_tipos = list(df_filial["Tipo_evento"].unique())
            for tipo in lista_tipos:
                if tipo == "NO CONTROLADO":
                    df_tipo = df_filial[df_filial["Tipo_evento"]==tipo]
                    lista_clasi = list(df_tipo["Clasificacion"].unique())
                    dic_grafica[tipo] = {}
                    for clasificacion in lista_clasi:
                        df_filtro = df_filial[(df_filial["Tipo_evento"] == tipo) & (df_filial["Clasificacion"] == clasificacion)].reset_index(drop=True)
                        if len(df_filtro):
                            dic_grafica[tipo][clasificacion] = []
                        for fecha in lista_periodos:
                            df_fecha = df_filtro[df_filtro["Fecha"]==fecha].reset_index(drop=True)
                            if len(df_fecha):
                                dic_grafica[tipo][clasificacion].append(df_fecha["Cantidad_eventos"][0])
                            else:
                                dic_grafica[tipo][clasificacion].append(0)
            dic_info = list(dic_grafica.values())[0]
            bar_width = 0.75
            fig, ax = plt.subplots(figsize=(32,16))
            colors = [dic_colores["azul_v"],"red"]
            labels = list(dic_info.keys())
            for i, (llave, valor) in enumerate(dic_info.items()):
                x = np.arange(len(lista_periodos))
                if i == 0:
                    limite = llave
                    ax.bar(x, valor, bar_width, label=f'{llave}', color=dic_colores["azul_agua_v"])
                    v_max = max(valor)
                    for i in range(len(lista_periodos)):
                        ax.text(x[i], valor[i]*0.5, f"{valor[i]}", ha='center', va='bottom', fontsize=32, color="white", rotation=90, fontweight='bold')
                else:
                    y = [v_max*1.15]*len(x)
                    v_x = []
                    v_y = []
                    for i in range(len(lista_periodos)):
                        if valor[i] > 0:
                            v_x.append(x[i])
                            v_y.append(y[i])
                            ax.text(x[i], y[i]*0.985, f"{valor[i]}", ha='center', va='bottom', fontsize=30, color="white", fontweight='bold')
                    ax.scatter(v_x, v_y, color='red', s=4500, label=llave)
            ax.text(x=-2, y=v_max*1.05, s=f'{limite}', color=dic_colores["azul_v"], fontsize=28)
            ax.axhline(y=v_max*1.05, linestyle='--', color=dic_colores["azul_v"], linewidth=3)
            for spine in ax.spines.values():
                spine.set_visible(False)
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(labels[i]),
                                                markerfacecolor=colors[i], markersize=25)
                                        for i in range(len(colors))]
            ax.legend(reversed(legend_handles), reversed(labels), loc='lower center', bbox_to_anchor=(0.5, -0.16), fontsize=24, ncol=2)
            ax.set_yticklabels([])
            ax.set_xticks(x)
            ax.tick_params(axis='x', color=dic_colores["azul_v"])
            ax.set_xticklabels(lista_periodos, fontsize=24, color=dic_colores["azul_v"])
            n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}.png")
            plt.savefig(n_imagen, transparent=True)
            plt.close()
            if c == 0:
                c+=1
                imagen = Image.open(n_imagen)
                recorte = (600, 1420, imagen.width-550, imagen.height)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(archivo_copia.replace(".csv", f"_limite.png"))
            imagen = Image.open(n_imagen)
            recorte = (180, 95, imagen.width-180, imagen.height-80)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)
            informar_imagen(n_imagen)

def grafica_barras_indicador_tecnico_horas(archivo, fecha):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        lista_filiales = list(df['Filial'].unique())
        dic_grafica = {}
        for filial in lista_filiales:
            df_filial = df[df["Filial"] == filial]
            lista_tipos = list(df_filial["Tipo_evento"].unique())
            lista_horas = list(df_filial["Hora_solicitud"].unique())
            lista_horas.sort()
            for tipo in lista_tipos:
                df_tipo = df_filial[df_filial["Tipo_evento"] == tipo]
                lista_clasi = list(df_tipo["Clasificacion"].unique())
                dic_grafica[tipo] = {}
                for clasificacion in lista_clasi:
                    dic_grafica[tipo][clasificacion] = []
                    for hora in lista_horas:
                        df_filtro = df_filial[(df_filial["Tipo_evento"] == tipo) & (df_filial["Clasificacion"] == clasificacion) & (df_filial["Hora_solicitud"] == hora)].reset_index(drop=True)
                        dic_grafica[tipo][clasificacion].append(df_filtro["Cantidad_eventos"].sum())
            for evento, dic in dic_grafica.items():
                lista_colores = ["#02c028","#ff8000","#cc0000"]
                fig, ax = plt.subplots(figsize=(24,12))
                bar_width = 0.7
                v_max = 0
                for i,(llave, valor) in enumerate(dic.items()):
                    lista_valores = list(dic.values())
                    if i == len(dic)-1:
                        base = suma_listas(lista_valores)
                        if max(base) > v_max:
                            v_max = max(base)
                for i,(llave, valor) in enumerate(dic.items()):
                    lista_llaves = list(dic.keys())
                    lista_valores = list(dic.values())
                    if i == 0:
                        ax.bar(range(24), lista_valores[0], bar_width, label=f'{evento} ({llave})', color=lista_colores[i])
                    else:
                        ax.bar(range(24), lista_valores[i], bar_width, label=f'{evento} ({llave})', color=lista_colores[i], bottom=suma_listas_pos(i, lista_valores))
                    if i == len(dic)-1:
                        for j in range(24):
                            ax.text(j, base[j]+v_max*0.03, f"{lista_valores[i][j]}", ha='center', fontsize=26, color=lista_colores[-1])
                ax.set_xticks(np.arange(24))
                ax.set_xlabel("Franja horaria", color=dic_colores["azul_v"],fontsize=27)
                ax.set_ylabel("Cantidad de eventos", color=dic_colores["azul_v"],fontsize=27)
                ax.set_xticklabels(range(24), color=dic_colores["azul_v"], fontsize=23)
                ax.legend(bbox_to_anchor=(0.5, -0.095), loc='upper center',
                                ncol=3, borderaxespad=0.0, fontsize=15)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.yaxis.set_major_locator(ticker.AutoLocator())
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:.0f}'))
                for tick in ax.yaxis.get_major_ticks():
                    tick.label1.set_color(dic_colores["azul_v"])
                    tick.label1.set_fontsize(23)
                    tick.set_pad(8)
                ax.set_ylim(0, v_max*1.15)
                nombre_evento = evento.replace(" ","_")
                n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}_{nombre_evento}.png")
                plt.savefig(n_imagen, transparent=True)
                plt.close()
                c = 0
                if c == 0:
                    c+=1
                    imagen = Image.open(n_imagen)
                    recorte = (570, 1150, imagen.width-540, imagen.height-2)
                    imagen_recortada = imagen.crop(recorte)
                    imagen_recortada.save(archivo_copia.replace(".csv", f"_limite_{nombre_evento}.png"))
                imagen = Image.open(n_imagen)
                recorte = (160, 50, imagen.width-275, imagen.height-45)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(n_imagen)
                informar_imagen(n_imagen)

def func(pct, allvalues):
    absolute = int(pct / 100. * sum(allvalues))  # Calcula el valor absoluto
    if absolute < 10:
        return ''  # No mostrar porcentaje si es menor a 10
    else:
        return f'{pct:.1f}%'

def conversion_tarifa_texto(tarifa, texto):
    ext = "/ m³"
    if texto == "Cuf":
        ext = "/ factura"
    if tarifa < 1000:
        texto = f"{texto}: ${tarifa} {ext}"
    else:
        tarifa_1000 = tarifa%1000
        if len(str(tarifa_1000)) < 3:
                        tarifa_1000 = str(tarifa_1000)+"0"*(3-len(str(tarifa_1000)))
        texto = f"{texto}: ${tarifa//1000}.{tarifa_1000} {ext}"
    return texto

def recortar_imagen(nombre,nombre_guardar,v1=0,v2=0,v3=0,v4=0,informar=False):
    imagen = Image.open(nombre)
    recorte = (v1,v2,imagen.width-v3,imagen.height-v4)
    imagen_recortada = imagen.crop(recorte)
    imagen_recortada.save(nombre_guardar)
    if informar:
        informar_imagen(nombre_guardar)
    imagen.close()

def fun_tarifas(n_archivo, fecha, dic_metricas):
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        archivo_copia = archivo_copia.replace("_reporte_tarifario","_rt")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = df[(df["Anio_reportado"]==int(fecha[0]))&(df["Mes_reportado"]==fecha[1])]
        dic_tarifas = {}
        llaves_por = ["Porcentaje G","Porcentaje T","Porcentaje D", "Porcentaje P_perdidas"]
        for llave in llaves_por:
            df[llave] = df[llave].str.replace(" %", "").astype(float)
        colors_pie = [dic_colores["azul_v"],dic_colores["amarillo_v"],dic_colores["vinotinto"],dic_colores["gris"]]
        colors_pie = [(color, 0.9) for color in colors_pie]
        c = 0
        lista_mercado = list(df["ID_Mercado"].unique())
        for id_mercado in lista_mercado:
            df_mercado = df[df["ID_Mercado"]==int(id_mercado)].reset_index(drop=True)
            if str(id_mercado) in dic_mercados and len(df_mercado):
                id_empresa = dic_mercados[str(id_mercado)]["Id_empresa"]
                if id_empresa in empresa_indicador_SUI:
                    filial = empresa_indicador_SUI[id_empresa]
                    if filial not in dic_tarifas:
                        dic_tarifas[filial] = {}
                    df_mercado = df[df["ID_Mercado"]==int(id_mercado)].reset_index(drop=True)
                    if str(id_mercado) not in dic_tarifas[filial]:
                        dic_tarifas[filial][str(id_mercado)] = [dic_mercados[str(id_mercado)]["Nombre_mercado"]]
                    cuf = conversion_tarifa_texto(round(df_mercado["Cuf"][0]), "Cuf")
                    cuv = conversion_tarifa_texto(round(df_mercado["Cuv"][0]), "Cuv")
                    T1 = conversion_tarifa_texto(round(df_mercado["Tarifa_1"][0]), "Tarifa Estrato 1")
                    T2 = conversion_tarifa_texto(round(df_mercado["Tarifa_2"][0]), "Tarifa Estrato 2")
                    dic_tarifas[filial][str(id_mercado)].append([cuf,cuv,T1,T2])
                labels = ["Suministro (G)","Transporte (T)","Distribución (D)","Pérdidas (P)"]
                lables_c = ["G","T","D","P"]
                sizes = []
                for llave in llaves_por:
                    sizes.append(df_mercado[llave][0])
                fig, ax = plt.subplots(figsize=(20, 20), dpi=225)
                wedges, texts, autotexts = ax.pie(sizes,
                                    labels=[''] * len(sizes),
                                    autopct=lambda pct: func(pct, sizes),
                                    labeldistance=0.9,
                                    textprops={'fontsize': 75, "color":'white'},
                                    startangle=0,
                                    colors=[(color[0], color[1]) for color in colors_pie])
                for i, (wedge, pct) in enumerate(zip(wedges, sizes)):
                    ang = ((wedge.theta1 + wedge.theta2)/2)
                    text = lables_c[i]
                    ubicar_porcentajes(text, ang, 1.15, ax, colors_pie[i],size=95)
                plt.gca().set_aspect('equal')
                plt.gca().spines['top'].set_visible(False)
                plt.gca().spines['right'].set_visible(False)
                plt.gca().spines['bottom'].set_visible(False)
                plt.gca().spines['left'].set_visible(False)
                legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(labels[i]),
                                    markerfacecolor=colors_pie[i], markersize=28)
                                for i in range(len(labels))]
                ax.legend(handles=legend_handles, bbox_to_anchor=(0.5, -0.025), loc='upper center',
                        ncol=2, borderaxespad=0.0, fontsize=40)
                nombre = archivo_copia.replace(".csv", f"_{id_mercado}.png")
                nombre_limite = archivo_copia.replace(".csv", "_limite.png")
                plt.savefig(nombre, transparent=True)
                plt.close()
                if c == 0:
                    c += 1
                    recortar_imagen(nombre, nombre_limite, 500,3900,500,0, informar=True)
                recortar_imagen(nombre, nombre, 330,0,330,460, informar=True)
        dic_metricas["tarifas"] = dic_tarifas
    return dic_metricas

def metricas_sector_consumo(archivo, fecha_anterior, fecha_actual, dic_metricas):
    if os.path.exists(archivo):
        df = pd.read_csv(archivo, sep=",", encoding="utf-8-sig")
        df_filtro = df[(df["Tipo de usuario"]=="Total")&(df["Filial"]==grupo_vanti)].reset_index(drop=True)
        if len(df_filtro):
            texto_1 = float(df_filtro["Consumo m3"].sum())
            texto_1 = f"{round(texto_1/1e6,1)} M"
            dic_metricas["total_ventas"] = texto_1
        else:
            dic_metricas["total_ventas"] = None
        df_fecha = df[(df["Anio reportado"]==int(fecha_actual[0]))&(df["Mes reportado"]==fecha_actual[1])&(df["Filial"]==grupo_vanti)].reset_index(drop=True)
        df_filtro = df_fecha[(df_fecha["Tipo de usuario"]=="Total")].reset_index(drop=True)
        df2 = df_filtro.copy()
        if len(df_filtro):
            texto_1 = round(df_filtro["Diferencia Cantidad de usuarios"][0])
            texto_1 = f"{texto_1/1e3}"
            dic_metricas["nuevos_usuarios"] = texto_1
        else:
            dic_metricas["nuevos_usuarios"] = None
        df_filtro = df_fecha[(df_fecha["Tipo de usuario"]=="Regulados")].reset_index(drop=True)
        if len(df_filtro):
            texto_1 = round(df_filtro["Cantidad de usuarios"][0])
            texto_1 =  f"{round(texto_1/1e6,1)} M"
            dic_metricas["usuarios_regulados"] = texto_1
        else:
            dic_metricas["usuarios_regulados"] = None
        df_filtro = df_fecha[(df_fecha["Tipo de usuario"]=="No regulados")].reset_index(drop=True)
        if len(df_filtro):
            texto_1 = round(df_filtro["Cantidad de usuarios"][0])
            texto_1 =  f"{int(texto_1)}"
            dic_metricas["usuarios_no_regulados"] = texto_1
        else:
            dic_metricas["usuarios_no_regulados"] = None
        df1 = df[(df["Anio reportado"]==int(fecha_anterior[0]))&(df["Mes reportado"]==fecha_anterior[1])&(df["Tipo de usuario"]=="Total")&(df["Filial"]==grupo_vanti)].reset_index(drop=True)
        if len(df1) and len(df2):
            v1 = round(df1["Cantidad de usuarios"][0])
            v2 = round(df2["Cantidad de usuarios"][0])
            valor = round(abs(((v1-v2)/v2)*100),1)
            texto_1 =  f"{valor} %"
            dic_metricas["porcentaje_crecimiento"] = texto_1
        else:
            dic_metricas["porcentaje_crecimiento"] = None
    return dic_metricas

def metricas_suspensiones(archivo, fecha, dic_metricas):
    if os.path.exists(archivo):
        df = pd.read_csv(archivo, sep=",", encoding="utf-8-sig")
        df_filtro = df[(df["Anio_reportado"]==int(fecha[0]))&(df["Mes_reportado"]==fecha[1])].reset_index(drop=True)
        if len(df_filtro):
            dic_metricas["cantidad_eventos"] = str(len(df_filtro))
            suma = round(df_filtro["Numero_suscriptores_afectados"].sum())
            if suma > 1000:
                texto_1 = f"{suma/1e3}"
            else:
                texto_1 = str(suma)
            dic_metricas["usuarios_eventos"] = texto_1
        else:
            dic_metricas["usuarios_eventos"] = None
            dic_metricas["cantidad_eventos"] = None
    return dic_metricas

def metricas_indicadores(archivo, fecha, dic_metricas):
    if os.path.exists(archivo):
        df = pd.read_csv(archivo, sep=",", encoding="utf-8-sig")
        df_filtro = df[(df["Anio_reportado"]==int(fecha[0]))&(df["Mes_reportado"]==fecha[1])&(df["Tipo_evento"]=="NO CONTROLADO")].reset_index(drop=True)
        if len(df_filtro):
            suma = round(df_filtro["Cantidad_eventos"].sum())
            if suma > 1000:
                texto_1 = f"{suma/1e3}"
            else:
                texto_1 = str(suma)
            dic_metricas["cantidad_emergencias"] = texto_1
            texto_1 = str(round(df_filtro["Tiempo_promedio_llegada (min)"].mean(),1))+" min"
            dic_metricas["tiempo_emergencias"] = texto_1
        else:
            dic_metricas["cantidad_emergencias"] = None
            dic_metricas["tiempo_emergencias"] = None
    return dic_metricas

def metricas_compensacines(archivo, fecha, dic_metricas):
    if os.path.exists(archivo):
        df = pd.read_csv(archivo, sep=",", encoding="utf-8-sig")
        df_filtro = df[(df["Anio_reportado"]==int(fecha[0]))&(df["Mes_reportado"]==fecha[1])&(df["Filial"]==grupo_vanti)].reset_index(drop=True)
        if len(df_filtro):
            texto_1 = float(df_filtro["Usuarios_compensados"][0])
            texto_1 =  f"{texto_1/1e3}"
            dic_metricas["usuarios_compensados"] = texto_1
            texto_1 = round(df_filtro["Valor_compensado"][0])
            texto_1 = f"{round(texto_1/1e6,1)} M"
            dic_metricas["valor_compensado"] = texto_1
        else:
            dic_metricas["valor_compensado"] = None
            dic_metricas["usuarios_compensados"] = None
    return dic_metricas

def grafica_deuda_subsidios(archivo, archivo_1, dic_metricas):
    if os.path.exists(archivo) and os.path.exists(archivo_1):
        lista_archivo = archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        lista_archivo[-1] = f"KPI_subsidios.png"
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(archivo, sep=",", encoding="utf-8-sig")
        df_1 = pd.read_csv(archivo_1, sep=",", encoding="utf-8-sig")
        porcentaje = round(df_1["KPI"].mean(),2)
        meta_subsidios = 1.4
        error = (abs(meta_subsidios-porcentaje)/meta_subsidios)*100
        if porcentaje >= meta_subsidios:
            color = dic_colores["rojo_c"]
        elif error >= 25:
            color = dic_colores["naranja_p"]
        else:
            color = dic_colores["verde_c"]
        dic_metricas["kpi_subsidios"] = [porcentaje, color]
        df = union_listas_df_fecha(df, anio="Anio", mes="Mes")
        anios = list(df["Fecha"])
        x = range(1, len(df)+1)
        data = [list(df["Deuda"]), list(df["Pagado"])]
        lista_colores = [dic_colores["azul_v"], dic_colores["rojo_c"]]
        fig, ax = plt.subplots(figsize=(30,15))
        ax.fill_between(x, df["Deuda"], color=lista_colores[0], label='Causado')
        ax.fill_between(x, df["Pagado"], color=lista_colores[1], alpha=0.7, label='Girado MME')
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1e9:.1f} m M'))
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_color(dic_colores["azul_v"])
            tick.label1.set_fontsize(18)
            tick.set_pad(8)
        ax.set_xticks(x)
        ax.set_xticklabels(anios, color=dic_colores["azul_v"], fontsize=18)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.legend(bbox_to_anchor=(0.5, -0.08), loc='upper center',
                    ncol=2, borderaxespad=0.0, fontsize=18)
        ax.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
        plt.savefig(archivo_copia, transparent=True)
        plt.close()
        imagen = Image.open(archivo_copia)
        recorte = (50, 60, imagen.width-80, imagen.height-20)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(archivo_copia)
        informar_imagen(archivo_copia)
    return dic_metricas