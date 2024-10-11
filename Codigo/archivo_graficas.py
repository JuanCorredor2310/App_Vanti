import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import seaborn as sns
import pandas as pd
from pandas.plotting import table
import os
from PIL import Image
from skimage.transform import resize

import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
import modulo as mod_1
import archivo_creacion_json as mod_2

global grupo_vanti, lista_filiales, dic_filiales, dic_filiales_largo, limite_facturas, porcentaje_ISRT, dic_nom_eventos,dic_sectores_consumo,dic_sectores_consumo_ordenados,dic_sectores_consumo_imagenes
dic_sectores_consumo = {"Regulados": {
                            "Residencial Bajo - Bajo": "Residencial",
                            "Residencial Bajo": "Residencial",
                            "Residencial Medio - Bajo": "Residencial",
                            "Residencial Medio": "Residencial",
                            "Residencial Medio - Alto": "Residencial",
                            "Residencial Alto": "Residencial",
                            "Comercial": "Comercial",
                            "Industrial": "Industrial",
                            "Oficial": "Comercial",
                            "Especial Asistencial - EA": "Comercial",
                            "Especial Educativo - ED": "Comercial",
                            "Usuario Exento - UE": "Residencial",
                            "Industrial Exento - IE": "Industrial",
                            "Zonas comunes": "Residencial",
                            "Provisional": "Residencial"},
                        "No regulados": {
                            "Comercial": "Comercial",
                            "Comercializadoras de gas natural": "Comercializadoras /\nTransportadores",
                            "Transportadores de gas natural": "Comercializadoras /\nTransportadores",
                            "GNCV": "GNCV",
                            "Petroqu\u00edmica": "Petroqu\u00edmica",
                            "Industrial": "Industrial",
                            "Oficiales": "Oficiales",
                            "Termoel\u00e9ctrico": "Termoel\u00e9ctrico",
                            "Refiner\u00eda": "Refiner\u00eda"}}
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

grupo_vanti = "Grupo Vanti"
dic_nom_eventos = {"CONTROLADO" : "Controlados",
                "NO CONTROLADO" : "No Controlados"}
porcentaje_ISRT = 100
limite_facturas = 4.04
lista_filiales = ["VANTI S.A. ESP.",
                    "GAS NATURAL CUNDIBOYACENCE S.A. ESP.      ",
                    "GAS NATURAL DEL CESAR S.A. ESP.",
                    "GAS NATURAL DE ORIENTE S.A. ESP."]
dic_filiales = {"VANTI": "VANTI S.A. ESP.",
    "GNCB": "GAS NATURAL CUNDIBOYACENCE S.A. ESP.",
    "GNCR": "GAS NATURAL DEL CESAR S.A. ESP.",
    "GOR": "GAS NATURAL DE ORIENTE S.A. ESP."}
dic_cumplimientos_reporte = {"VANTI S.A. ESP":"VANTI S.A. ESP.",
                            grupo_vanti:grupo_vanti,
                            "GAS NATURAL CUNDIBOYACENSE SA ESP":"GAS NATURAL CUNDIBOYACENCE S.A. ESP.",
                            "GAS NATURAL DEL CESAR S.A. EMPRESA DE SERVICIOS PUBLICOS":"GAS NATURAL DEL CESAR S.A. ESP.",
                            'GAS NATURAL DEL ORIENTE SA ESP':'GAS NATURAL DE ORIENTE S.A. ESP.'}
dic_filiales_largo = {'VANTI S.A. ESP.':'VANTI',
                    'GAS NATURAL CUNDIBOYACENCE S.A. ESP.':'GNCB',
                    'GAS NATURAL DEL CESAR S.A. ESP.':'GNCR',
                    'GAS NATURAL DE ORIENTE S.A. ESP.':'GOR',
                    "Grupo Vanti":"grupo_vanti"}
lista_archivos = ["porcentaje_reclamos_facturacion_10000_2023_TRIM_3_2024_TRIM_2",
                    '2023_AGOSTO_2024_JULIO_compilado_compensacion',
                    '2023_AGOSTO_2024_JULIO_indicador_tecnico',
                    '2023_AGOSTO_2024_JULIO_indicador_tecnico_IRST_minutos',
                    '2023_AGOSTO_2024_JULIO_indicador_tecnico_IRST_horas',
                    "2023_AGOSTO_2024_JULIO_reporte_consumo_sumatoria",
                    "porcentaje_cumplimientos_regulatorios",
                    "porcentaje_matriz_requerimientos",
                    "gastos_AOM_2023"]
def union_listas_df_trimestre(df):
    lista = []
    for i in range(len(df)):
        lista.append(str(df['Periodo_reportado'][i]).replace('TRIM_','Trimestre ')+'\n'+str(df['Anio_reportado'][i]).replace('np.int64(','').replace(')',''))
    df['Periodo_reportado_Periodo_reportado'] = lista
    return df

def union_listas_df_fecha(df, sep=False):
    if sep:
        llave1 = "Mes reportado"
        llave2 = "Anio reportado"
    else:
        llave1 = "Mes_reportado"
        llave2 = "Anio_reportado"
    lista = []
    for i in range(len(df)):
        lista.append(str(df[llave1][i])+'\n'+str(df[llave2][i]))
    df['Fecha'] = lista
    return df

def grafica_barras_trimestre_reclamos(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        dic_grafica = {}
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje_reclamos_fact_10000'] = df['Porcentaje_reclamos_fact_10000'].str.replace(" %", "").astype(float)
        df_filtro = df[df["Filial"]!="Grupo Vanti"].reset_index(drop=True)
        df_filtro = union_listas_df_trimestre(df_filtro)
        lista_filiales = list(df_filtro['Filial'].unique())
        for filial in lista_filiales:
            df_filial = df_filtro[df_filtro['Filial'] == filial]
            lista_periodos = list(df_filial["Periodo_reportado_Periodo_reportado"].unique())
            lista_porcentaje = list(df_filial['Porcentaje_reclamos_fact_10000'])
            dic_grafica[filial] = lista_porcentaje
        cmap = LinearSegmentedColormap.from_list("Purple", ["#8d628e","#c0a8c0"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        colors = [cmap(i/3) for i in range(4)]
        for filial in lista_filiales:
            valores = dic_grafica[filial]
            fig, ax = plt.subplots(figsize=(16, 14))
            x = np.arange(len(lista_periodos))  # Adjust x-coordinates
            ax.set_xticks(x)  # Adjust x-ticks
            ax.set_xticklabels(lista_periodos)
            for i in range(len(lista_periodos)):
                ax.bar(x[i], valores[i], color=colors[i])  # Use align='edge' and adjust x-coordinates
            for i in range(len(lista_periodos)):
                ax.text(x[i], valores[i] + 0.15, f"{valores[i]}%", ha='center', va='bottom', fontsize=23, color=colors[i])
            ax.set_title(f'Relación de reclamos por cada 10.000 facturas\nexpedidas {dic_filiales[filial]}', color=colors[0],fontsize=26, y=1.05)
            ax.tick_params(axis='x', colors=colors[0],labelsize=20)
            ax.tick_params(axis='y', colors=colors[0],size=0)
            for spine in ax.spines.values():
                spine.set_visible(False)
            plt.subplots_adjust(left=-0.03, right=1.02, top=0.88, bottom=0.105)
            ax.axhline(y=limite_facturas, linestyle='--', color='#805181', label=f'Límite regulatorio ({limite_facturas}%)')
            ax.legend(bbox_to_anchor=(0.5, -0.065), loc='upper center',
                        borderaxespad=0.0, fontsize=16, labelcolor='#805181')
            ax.set_yticks([])
            ax.set_yticklabels([])
            plt.savefig(n_archivo.replace('.csv',f'_{filial}.png'))

def grafica_barras_compensacion(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df)
        """df_filtro = df[(df['Filial'] != grupo_vanti)].reset_index(drop=True)
        lista_filiales = list(df_filtro['Filial'].unique())
        lista_periodos = list(df_filtro['Fecha'].unique())
        dic_filiales = {}
        cmap = LinearSegmentedColormap.from_list("Azul", ["#4f5aec","#a7adf6"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        for filial in lista_filiales:
            df_filtro = df[(df['Filial'] == filial) & (df['Mes_compensado'] == "Total")].reset_index(drop=True)
            df_filtro['Valor_compensado_millones'] = (round(df_filtro['Valor_compensado'] / 1000000,2)).astype(str) + ' M'
            dic_filiales[filial] = [[],[]]
            for periodo in lista_periodos:
                df_periodo = df_filtro[df_filtro['Fecha'] == periodo].reset_index(drop=True)
                if len(df_periodo):
                    dic_filiales[filial][0].append(df_periodo['Valor_compensado'][0])
                    dic_filiales[filial][1].append(df_periodo['Valor_compensado_millones'][0])
                else:
                    dic_filiales[filial][0].append(0)
                    dic_filiales[filial][1].append("0 M")
        for filial, lista_valores in dic_filiales.items():
            fig, ax = plt.subplots(figsize=(16, 10))
            x = np.arange(len(lista_periodos))
            bar_width = 0.75
            colors = [cmap(i/11.0) for i in range(12)]  # Use the custom color map
            for i in range(12):
                ax.bar(lista_periodos[i], lista_valores[0][i], width=bar_width, color=colors[i])
                ax.text(lista_periodos[i], lista_valores[0][i] + 2, f"{lista_valores[1][i]}", ha='center', va='bottom', fontsize=18, color=colors[i])
            ax.set_title(f'Valor compensado por {filial} (COP)', color=colors[0],fontsize=22, y=1.05)
            ax.tick_params(axis='x', colors=colors[0],labelsize=15)
            ax.tick_params(axis='y', colors=colors[0],size=0)
            for spine in ax.spines.values():
                spine.set_visible(False)
            plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.08)
            ax.set_yticks([])
            ax.set_yticklabels([])
            plt.savefig(n_archivo.replace('.csv',f'_{dic_filiales_largo[filial]}.png'))"""

        df_filtro = df[df['Filial'] == grupo_vanti].reset_index(drop=True)
        df_filtro = union_listas_df_fecha(df_filtro)
        df_filtro['Valor_compensado_millones'] = (round(df_filtro['Valor_compensado'] / 1000000,2)).astype(str) + ' M'
        lista_periodos = list(df_filtro["Fecha"].unique())
        lista_valores = list(df_filtro["Valor_compensado"].unique())
        lista_valores_millones = list(df_filtro["Valor_compensado_millones"].unique())
        cmap = LinearSegmentedColormap.from_list("Azul", ["#4f5aec","#a7adf6"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        fig, ax = plt.subplots(figsize=(16, 10))
        x = np.arange(len(lista_periodos))
        bar_width = 0.75
        colors = [cmap(i/11.0) for i in range(12)]  # Use the custom color map
        for i in range(12):
            ax.bar(lista_periodos[i], lista_valores[i], width=bar_width, color=colors[i])
            ax.text(lista_periodos[i], lista_valores[i] + 2, f"{lista_valores_millones[i]}", ha='center', va='bottom', fontsize=18, color=colors[i])
        ax.set_title(f'Valor compensado por el {grupo_vanti} (COP)', color=colors[0],fontsize=22, y=1.05)
        ax.tick_params(axis='x', colors=colors[0],labelsize=15)
        ax.tick_params(axis='y', colors=colors[0],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.08)
        ax.set_yticks([])
        ax.set_yticklabels([])
        plt.savefig(n_archivo.replace('.csv','.png'))

def cambio_lista_IRST(lista, v_min):
    lista_1 = []
    for i in lista:
        if i < v_min:
            v_min = i
        lista_1.append(round(i-porcentaje_ISRT,12))
    return lista_1, v_min

def grafica_barras_indicador_tecnico(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df)
        lista_filiales = list(df['Filial'].unique())
        cmap = LinearSegmentedColormap.from_list("Orange", ["#fd8c25","#fec692"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        lista_colores = ["#a6194a","#fd8c25","#0391ce"]
        for filial in lista_filiales:
            dic_grafica = {}
            v_min = porcentaje_ISRT
            df_filial = df[df['Filial'] == filial].reset_index(drop=True)
            lista_periodos = list(df_filial["Fecha"])
            lista_indicadores = ["IPLI", "IO", "IRST_EG"]
            for indicador in lista_indicadores:
                if indicador == "IRST_EG":
                    dic_grafica["IRST-EG"],v_min = cambio_lista_IRST(list(df_filial["IRST_EG"]), v_min)
                else:
                    dic_grafica[indicador],v_min = cambio_lista_IRST(list(df_filial[indicador]), v_min)
            data = np.array(list(dic_grafica.values())).T
            lista_indicadores = list(dic_grafica.keys())
            fig, ax = plt.subplots(figsize=(25, 14))
            bar_width = 0.3
            cmap = LinearSegmentedColormap.from_list("Orange", ["#fd8c25","#fec692"])
            for i in range(3):
                colors = cmap(np.linspace(0, 1, 3))
                bars = ax.bar(np.arange(12) + i * bar_width, data[:, i], bar_width, label=lista_indicadores[i], color=lista_colores[i])
                for bar, value in zip(bars.patches, data[:, i]):
                    if value < 0:
                        ax.text(bar.get_x() + bar.get_width()/2, -(bar.get_y() - bar.get_height())-0.3, f"{(100+value):.2f}%", color=lista_colores[i], ha="center", va="bottom", fontsize=22, rotation=90)
                    elif i==1:
                        ax.text(bar.get_x() + bar.get_width()/2, 0, f"{(100):.2f}%", color=lista_colores[i], ha="center", va="bottom", fontsize=19)
            ax.set_xticks(np.arange(12) + bar_width)
            ax.set_xticklabels(lista_periodos, color=lista_colores[1], fontsize=20)
            ax.set_title(f"Indicadores técnicos para la filial {filial}", fontsize=25, color=lista_colores[1])
            lista = ["IPLI", "IO", "IRST-EG"]
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(lista[i]),
                                            markerfacecolor=lista_colores[i], markersize=10)
                                    for i in range(len(lista))]
            ax.legend(handles=legend_handles, bbox_to_anchor=(0.5, -0.075), loc='upper center',
                            ncol=len(lista), borderaxespad=0.0, fontsize=21)
            ax.set_ylim(v_min-100.5, 0.2)
            for spine in ax.spines.values():
                spine.set_visible(False)
            plt.subplots_adjust(left=-0.03, right=1.04, top=0.96, bottom=0.13)
            ax.set_yticks([])
            ax.set_yticklabels([])
            plt.savefig(n_archivo.replace(".csv", f"_{dic_filiales_largo[filial]}.png"))

def grafica_barras_indicador_tecnico_minutos(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df)
        df['Porcentaje_reclamos_fact_10000'] = df['Porcentaje_cantidad_eventos'].str.replace(" %", "").astype(float)
        lista_filiales = list(df['Filial'].unique())
        cmap1 = LinearSegmentedColormap.from_list("O1", ["#2f036c","#988eb0"])
        grad1 = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad1 = cmap1(grad1)
        cmap2 = LinearSegmentedColormap.from_list("O2", ["#a86bff","#a1a3d1"])
        grad2 = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad2 = cmap2(grad2)
        cmap3 = LinearSegmentedColormap.from_list("O3", ["#076bc1","#85d9e0"])
        grad3 = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad3 = cmap3(grad3)
        cmap4 = LinearSegmentedColormap.from_list("O4", ["#00fffd","#75e6c6"])
        grad4 = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad4 = cmap4(grad4)
        colors1 = [cmap1(i/11.0) for i in range(12)]
        colors2 = [cmap2(i/11.0) for i in range(12)]
        colors3 = [cmap3(i/11.0) for i in range(12)]
        colors4 = [cmap4(i/11.0) for i in range(12)]
        for filial in lista_filiales:
            dic_grafica = {}
            df_filial = df[df['Filial'] == filial].reset_index(drop=True)
            lista_periodos = list(df_filial["Fecha"].unique())
            periodos = range(len(lista_periodos))
            lista_tipos = list(df_filial["Tipo_evento"].unique())
            for tipo in lista_tipos:
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
            fig, ax = plt.subplots(figsize=(15,10))
            bar_width = 0.35
            v_max = 0
            for i, (llave, valor) in enumerate(dic_grafica.items()):
                lista_llaves = list(valor.keys())
                lista_valores = list(valor.values())
                v1 = max(lista_valores[0])
                if v1 > v_max:
                    v_max = v1
                v1 = max(lista_valores[1])
                if v1 > v_max:
                    v_max = v1
                if i == 0:
                    ax.bar([x + i * bar_width for x in periodos], lista_valores[0], bar_width, label=f'{llave} ({lista_llaves[0]})', color=colors1[0])
                    ax.bar([x + i * bar_width for x in periodos], lista_valores[1], bar_width, lista_valores[0], label=f'{llave} ({lista_llaves[1]})', color=colors2[0])
                    for j in range(12):
                        ax.text(x = j + i * bar_width, y=lista_valores[0][j]+lista_valores[1][j]+0.5, s=f'{lista_valores[0][j]}', ha='center', va='bottom', color=colors1[0], fontsize=12)
                        valor1 = (lista_valores[0][j]+lista_valores[1][j])*0.06
                        if valor1 < 2:
                            valor1 = 2
                        ax.text(x = j + i * bar_width, y=lista_valores[0][j]+lista_valores[1][j]+valor1, s=f'{lista_valores[1][j]}', ha='center', va='bottom', color=colors2[0], fontsize=12)
                else:
                    ax.bar([x + i * bar_width for x in periodos], lista_valores[0], bar_width, label=f'{llave} ({lista_llaves[0]})', color=colors3[0])
                    ax.bar([x + i * bar_width for x in periodos], lista_valores[1], bar_width, bottom=lista_valores[0], label=f'{llave} ({lista_llaves[1]})', color=colors4[0])
                    for j in range(12):
                        ax.text(x = j + i * bar_width, y=lista_valores[0][j]+lista_valores[1][j]+0.5, s=f'{lista_valores[0][j]}', ha='center', va='bottom', color=colors3[0], fontsize=12)
                        valor1 = (lista_valores[0][j]+lista_valores[1][j])*0.08
                        if valor1 < 4:
                            valor1 = 4
                        ax.text(x = j + i * bar_width, y=lista_valores[0][j]+lista_valores[1][j]+valor1, s=f'{lista_valores[1][j]}', ha='center', va='bottom', color=colors4[0], fontsize=12)
            ax.set_xticks(np.arange(12) + bar_width)
            ax.set_xticklabels(lista_periodos, color=colors1[0], fontsize=12)
            ax.set_title(f"Eventos Controlados / No Controlados\n para {filial}", fontsize=20, color=colors1[0])
            ax.set_ylim(0, v_max+10)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(reversed(handles), reversed(labels),
                    bbox_to_anchor=(0.5, -0.075), loc='upper center',
                    ncol=2, borderaxespad=0.0, fontsize=11)
            for spine in ax.spines.values():
                spine.set_visible(False)
            plt.subplots_adjust(left=-0.03, right=1.03, top=0.91, bottom=0.13)
            ax.set_yticks([])
            ax.set_yticklabels([])
            plt.savefig(n_archivo.replace(".csv", f"_{dic_filiales_largo[filial]}.png"))

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

def grafica_barras_indicador_tecnico_horas(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        ext = lista_archivo[-1].split("_")[:4]
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        lista_filiales = list(df['Filial'].unique())
        dic_grafica = {}
        for filial in lista_filiales:
            df_filial = df[df["Filial"] == filial]
            lista_tipos = list(df_filial["Tipo_evento"].unique())
            lista_horas = list(df_filial["Hora_solicitud"].unique())
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
                lista_colores = ["#77dd77","#FF964F","#ff6961"]
                fig, ax = plt.subplots(figsize=(14,9))
                bar_width = 0.7
                v_max = 0
                for i,(llave, valor) in enumerate(dic.items()):
                    lista_llaves = list(dic.keys())
                    lista_valores = list(dic.values())
                    if i == 0:
                        ax.bar(range(24), lista_valores[0], bar_width, label=f'{evento} ({llave})', color=lista_colores[i])
                    else:
                        ax.bar(range(24), lista_valores[i], bar_width, label=f'{evento} ({llave})', color=lista_colores[i], bottom=suma_listas_pos(i, lista_valores))
                    if i == len(dic)-1:
                        base = suma_listas(lista_valores)
                        if max(base) > v_max:
                            v_max = max(base)
                        for j in range(24):
                            ax.text(j, base[j]*1.08, f"{lista_valores[i][j]}", ha='center', fontsize=19, color=lista_colores[-1])
                ax.set_xticks(np.arange(24))
                ax.set_xlabel("Franja horaria", color = lista_colores[1],fontsize=16)
                ax.set_ylabel("Cantidad de eventos", color = lista_colores[1],fontsize=16)
                ax.set_xticklabels(range(24), color=lista_colores[1], fontsize=12)
                ax.set_title(f"Duración eventos {dic_nom_eventos[evento]} por franja horaria para\n{filial} ({ext[0]}/{ext[1]} - {ext[2]}/{ext[3]})", fontsize=20, color=lista_colores[1], y=1.01)
                ax.legend(bbox_to_anchor=(0.5, -0.085), loc='upper center',
                                ncol=3, borderaxespad=0.0, fontsize=11)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.yaxis.set_major_locator(ticker.AutoLocator())
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:.0f}'))
                for tick in ax.yaxis.get_major_ticks():
                    tick.label1.set_color(lista_colores[1])
                    tick.label1.set_fontsize(12)
                    tick.set_pad(8)
                ax.set_ylim(0, v_max*1.15)
                nombre_evento = evento.replace(" ","_")
                plt.subplots_adjust(left=0.065, right=1.01, top=0.91, bottom=0.11)
                plt.savefig(n_archivo.replace(".csv", f"_{dic_filiales_largo[filial]}_{nombre_evento}.png"))

def grafica_pie_tipo_usuario(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        ext = lista_archivos[-1].split("_")[:4]
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Anio reportado'] = df['Anio reportado'].astype(int)
        fecha = [2024, "Junio".capitalize()]
        df =  df[(df["Anio reportado"]==fecha[0])].reset_index(drop=True)
        df =  df[(df["Mes reportado"] == fecha[1])].reset_index(drop=True)
        df['Porcentaje Cantidad de usuarios'] = df['Porcentaje Cantidad de usuarios'].str.replace(" %", "").astype(float)
        df['Porcentaje Consumo m3'] = df['Porcentaje Consumo m3'].str.replace(" %", "").astype(float)
        lista_filiales = list(df["Filial"].unique())
        lista_colores = [["#a84bff","#3c0074"],
                        ["#9e1626","#da142c"],
                        ["#f29f12","#fcb741"],
                        ["#0e2395","#1637ef"],
                        ["#0f3654","#fdc743"]]
        #dic = {'Porcentaje Cantidad de usuarios':"Cantidad de usuarios para\n",
        #        "Porcentaje Consumo m3":"Metros cúbicos de GN consumidos para\n"}
        dic = {"Consumo m3":"Metros cúbicos de GN consumidos para\n"}
        for llave, valor in dic.items():
            for pos in range(len(lista_filiales)):
                filial = lista_filiales[pos]
                df_filtro = df[(df["Filial"]==filial) & (df["Tipo de usuario"]!="Total") & (df["Sector de consumo"]=="Total")]
                labels = list(df_filtro["Tipo de usuario"])
                sizes = list(df_filtro[llave])
                plt.figure(figsize=(8.3,6))
                plt.pie(sizes, labels=labels, autopct=lambda p : '{:.2f} M'.format(p * sum(sizes) / 100000000), colors=lista_colores[pos], textprops={'fontsize': 18,'color':'white'}, wedgeprops={'linewidth': 4, 'edgecolor': 'none'})
                plt.legend(bbox_to_anchor=(0.5, 0.01), loc='upper center',
                                        ncol=3, borderaxespad=0.0, fontsize=16)
                plt.title(f'{valor}{filial} ({fecha[0]}/{fecha[1]})', color=lista_colores[pos][0], fontsize=20)
                plt.gca().spines['top'].set_visible(False)
                plt.gca().spines['right'].set_visible(False)
                plt.gca().spines['bottom'].set_visible(False)
                plt.gca().spines['left'].set_visible(False)
                #plt.subplots_adjust(left=0, bottom=-0.03, right=0.000001, top=0)
                #plt.show()
                plt.savefig(n_archivo.replace(".csv", f"_{dic_filiales_largo[filial]}_pie_consumo_m3.png"))

def grafica_tabla_sector_consumo(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        ext = lista_archivos[-1].split("_")[:4]
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Anio reportado'] = df['Anio reportado'].astype(int)
        fecha = [2024, "Junio".capitalize()]
        df =  df[(df["Anio reportado"]==fecha[0])].reset_index(drop=True)
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
        """fig, ax = plt.subplots(figsize=(15, 5.5))  # Ajusta el tamaño de la imagen si es necesario
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
                print(text)
                y_pos = 1 - (i + 0.5) / (len(df1) + 1)
                print(y_pos)
                add_image(ax, dic_sectores_consumo_imagenes[text], 0.165, y_pos, zoom=0.1)
            else:
                cell.set_text_props(color='#3250f3')
                cell.set_edgecolor('black')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(12)
        ax.set_title(f"Demanda de Gas Natural para el {grupo_vanti} ({fecha[0]}/{fecha[1]})", y=1.07, weight="bold", color='#071c8e', fontsize=16)
        plt.subplots_adjust(left=0.13)
        tbl.scale(1.55, 2.8)
        plt.savefig(n_archivo.replace(".csv", "_tabla_consumo.png"),bbox_inches='tight', dpi=300)"""
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
                add_image(ax, dic_sectores_consumo_imagenes[text], 0.16, y_pos, zoom=0.15)
            else:
                cell.set_text_props(color='#3250f3')
                cell.set_edgecolor('black')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(16)
        #plt.subplots_adjust(left=0.13)
        tbl.scale(1.55, 2.8*2)
        ax.set_title(f"Demanda de Gas Natural para el {grupo_vanti} ({fecha[0]}/{fecha[1]})", y=1.55, weight="bold", color='#071c8e', fontsize=24)
        plt.savefig(n_archivo.replace(".csv", "_tabla_consumo.png"),bbox_inches='tight', dpi=300)

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

def velocimetro_cumplimientos_regulatorios(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        ext = lista_archivos[-1].split("_")[:4]
        fecha = [2024, "Junio".capitalize()]
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
            fig, ax = plt.subplots(figsize=(7, 6), subplot_kw={'projection': 'polar'})
            start = 0
            for i, value in enumerate(values):
                end = start + (value / 100) * np.pi
                ax.barh(1, end - start, left=start, height=0.5, color=colors[i],edgecolor='none')
                mid_angle = (start + end)  # Ángulo medio de cada sección
                if value < 30:
                    ax.text(mid_angle*0.5, 1.7, f'{value}%', ha='center', va='center', fontsize=12, color=colors[i])
                else:
                    ax.text(mid_angle*0.5, 1.4, f'{value}%', ha='center', va='center', fontsize=12, color=colors[i])
                start = end
            ax.set_yticklabels([])
            ax.set_xticks([])
            ax.spines['polar'].set_visible(False)
            ax.xaxis.set_visible(False)  # Hacer que el eje X no sea visible
            ax.yaxis.set_visible(False)
            legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=str(labels[i]),
                                                markerfacecolor=colors[i], markersize=10)
                                        for i in range(len(colors))]
            ax.legend(reversed(legend_handles), reversed(labels), loc='lower center', bbox_to_anchor=(0.5, 0.31), fontsize=10, ncol=1)
            plt.title(f'Oportunidad en la certifiación de reportes regulatorios para\n{dic_cumplimientos_reporte[filial]} (Acumulado año)', y=0.8, color=colors[-1])
            ax.set_ylim(-0.01, 3.2)
            ax.grid(False)
            n_imagen = n_archivo.replace(".csv", f"_cumplimientos_regulatorios_{dic_filiales_largo[dic_cumplimientos_reporte[filial]]}.png")
            plt.savefig(n_imagen)
            imagen = Image.open(n_imagen)
            recorte = (90, 105, imagen.width-80, imagen.height - 200)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)

def grafica_cantidad_usuarios(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        ext = lista_archivos[-1].split("_")[:4]
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = df[(df["Tipo de usuario"]=="Total") & (df["Sector de consumo"]=="Total")]
        df = union_listas_df_fecha(df)
        print(df[["Filial","Fecha","Cantidad de usuarios"]])

def grafica_matriz_requerimientos(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        ext = lista_archivos[-1].split("_")[:4]
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje_entidad'] = df['Porcentaje_entidad'].str.replace(" %", "").astype(float)
        labels = list(df["Categoria_entidad"])
        sizes = list(df["Cantidad"])
        colors = ["#5a015f","#751775","#ab27aa","#d138d0"]
        plt.figure(figsize=(8.3,6))
        #plt.pie(sizes, labels=labels, autopct=lambda p : '{:.2f} M'.format(p * sum(sizes) / 100000000), colors=lista_colores[pos], textprops={'fontsize': 18,'color':'white'}, wedgeprops={'linewidth': 4, 'edgecolor': 'none'})
        plt.pie(sizes, labels=labels, colors=colors, autopct=lambda p : '{:.0f}'.format(p * sum(df['Cantidad']) / 100), textprops={'fontsize': 18,'color':'white'}, wedgeprops={'linewidth': 10, 'edgecolor': 'none'},startangle=90, explode=[0.05, 0.05, 0.05, 0.05])
        plt.legend(bbox_to_anchor=(0.5, 0.01), loc='upper center',
                                ncol=2, borderaxespad=0.0, fontsize=16)
        #plt.title(f'{valor}{filial} ({fecha[0]}/{fecha[1]})', color=lista_colores[pos][0], fontsize=20)
        plt.title("Cantidad de requerimientos solicitados \n(Acumulado año)", fontsize=25, color=colors[0], y=0.97)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        #plt.subplots_adjust(left=0, bottom=-0.03, right=0.000001, top=0)
        n_imagen = n_archivo.replace(".csv", ".png")
        plt.savefig(n_imagen)
        imagen = Image.open(n_imagen)
        recorte = (35, 0, imagen.width-20, imagen.height)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)

def grafica_gastos_AOM(archivo, anio_1, anio_2):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        ext = lista_archivos[-1].split("_")[:4]
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje gastos'] = df['Porcentaje gastos'].str.replace(" %", "").astype(float)
        lista_filiales = list(df["Filial"].unique())
        for filial in lista_filiales:
            matriz = []
            matriz_1 = []
            df_filial = df[df["Filial"] == filial]
            anios = list(df_filial["Año"].unique())
            lista_negocios = list(df_filial["Negocio"].unique())
            for negocio in lista_negocios:
                matriz.append(list(df_filial[df_filial["Negocio"]==negocio]["Porcentaje gastos"]))
                matriz_1.append(list(df_filial[df_filial["Negocio"]==negocio]["Valor"]))
            lista_colores = ["#006261","#00b3b2","#00d4d5","#56feff"]
            fig, ax = plt.subplots(figsize=(20,12))
            bar_width = 0.7
            v_max = max_columna_matriz(matriz_1)
            for i in range(len(matriz)):
                if i == 0:
                    ax.bar(range(len(matriz[0])), matriz_1[i], bar_width, label=f'{lista_negocios[i]}', color=lista_colores[i])
                    for j in range(len(matriz[0])):
                        ax.text(j, matriz_1[i][j]*0.4, f"{matriz[i][j]} %", ha='center', fontsize=15, color=lista_colores[-1])
                else:
                    suma = suma_matriz(i, matriz_1)
                    ax.bar(range(len(matriz[0])), matriz_1[i], bar_width, label=f'{lista_negocios[i]}', color=lista_colores[i], bottom=suma)
                    for j in range(len(matriz[0])):
                        ax.text(j, suma[j]+matriz_1[i][j]*0.4, f"{matriz[i][j]} %", ha='center', fontsize=15, color=lista_colores[0])
            ax.set_ylim(0, v_max*1.015)
            ax.yaxis.set_major_locator(ticker.AutoLocator())
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1000000:.0f} M'))
            for tick in ax.yaxis.get_major_ticks():
                tick.label1.set_color(lista_colores[0])
                tick.label1.set_fontsize(12)
                tick.set_pad(8)
            ax.set_xticks(range(len(anios)))
            ax.set_xticklabels(anios, color=lista_colores[0], fontsize=16)
            ax.set_xlabel("Años", color = lista_colores[0],fontsize=18)
            ax.set_ylabel(f"Gastos AOM (M COP 31-dic-{anio_2})", color = lista_colores[0],fontsize=18)
            ax.set_title(f"Gastos AOM ({anio_1}-{anio_2})\npara {filial}", fontsize=23, color=lista_colores[0], y=1.01)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.legend(bbox_to_anchor=(0.5, -0.095), loc='upper center',
                        ncol=2, borderaxespad=0.0, fontsize=12)
            plt.subplots_adjust(bottom=0.135)
            n_imagen = n_archivo.replace(".csv", f"_{dic_filiales_largo[filial]}.png")
            plt.savefig(n_imagen)
            imagen = Image.open(n_imagen)
            recorte = (100, 40, imagen.width-200, imagen.height+100)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)
def grafico_barras_consumo(archivo):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df, sep=True)
        df_filtro = df[(df['Filial'] == grupo_vanti) & (df["Tipo de usuario"] == "Total")].reset_index(drop=True)
        df_filtro['Consumo m3 millones'] = (round(df_filtro['Consumo m3'] / 1000000,2)).astype(str) + ' M'
        lista_periodos = list(df_filtro["Fecha"].unique())
        lista_valores = list(df_filtro["Consumo m3"])
        lista_valores_millones = list(df_filtro["Consumo m3 millones"])
        cmap = LinearSegmentedColormap.from_list("Verde", ["#08850a","#9cce9d"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        fig, ax = plt.subplots(figsize=(16, 10))
        x = np.arange(len(lista_periodos))
        bar_width = 0.75
        colors = [cmap(i/11.0) for i in range(12)]  # Use the custom color map
        for i in range(12):
            ax.bar(lista_periodos[i], lista_valores[i], width=bar_width, color=colors[i])
            ax.text(lista_periodos[i], lista_valores[i] + 2, f"{lista_valores_millones[i]}", ha='center', va='bottom', fontsize=18, color=colors[i])
        ax.set_title(f'Consumo GN (Millones m3) por el {grupo_vanti}', color=colors[0],fontsize=22, y=1.02)
        ax.tick_params(axis='x', colors=colors[0],labelsize=15)
        ax.tick_params(axis='y', colors=colors[0],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.08)
        ax.set_yticks([])
        ax.set_yticklabels([])
        plt.savefig(n_archivo.replace('_reporte_consumo_sumatoria.csv','_consumo.png'))

def grafico_barras_usuarios(archivo, nuevos=False):
    n_archivo = ".\\"+archivo+".csv"
    if os.path.exists(n_archivo):
        if nuevos:
            llave = "Diferencia Cantidad de usuarios"
            titulo = f"Nuevos usuarios para el {grupo_vanti}"
            nombre = n_archivo.replace('_reporte_consumo_sumatoria.csv','_nuevos_usuarios.png')
            c1 = "#ff4040"
            c2 = "#ffb3b3"
        else:
            llave= "Cantidad de usuarios"
            titulo = f"Cantidad de usuarios (millones) para el {grupo_vanti}"
            nombre = n_archivo.replace('_reporte_consumo_sumatoria.csv','_usuarios.png')
            c1 = "#ff53bd"
            c2 = "#ffa0db"
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df, sep=True)
        df_filtro = df[(df['Filial'] == grupo_vanti) & (df["Tipo de usuario"] == "Total")].reset_index(drop=True)
        llave_millones = llave+" millones"
        if nuevos:
            df_filtro[llave] = (round(df_filtro[llave])).astype(int)
            df_filtro[llave_millones] = df_filtro[llave].astype(str)
        else:
            df_filtro[llave_millones] = (round(df_filtro[llave] / 1000000,2)).astype(str) + ' M'
        lista_periodos = list(df_filtro["Fecha"].unique())
        lista_valores = list(df_filtro[llave].unique())
        lista_valores_millones = list(df_filtro[llave_millones])
        cmap = LinearSegmentedColormap.from_list("", [c1,c2])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        colors = [cmap(i/11.0) for i in range(12)]
        fig, ax = plt.subplots(figsize=(16, 10))
        x = np.arange(len(lista_periodos))
        bar_width = 0.75
        for i in range(12):
            ax.bar(lista_periodos[i], lista_valores[i], width=bar_width, color=colors[i])
            ax.text(lista_periodos[i], lista_valores[i] + 2, f"{lista_valores_millones[i]}", ha='center', va='bottom', fontsize=18, color=colors[i])
        ax.set_title(titulo, color=colors[0],fontsize=22, y=1.02)
        ax.tick_params(axis='x', colors=colors[0],labelsize=15)
        ax.tick_params(axis='y', colors=colors[0],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.08)
        ax.set_yticks([])
        ax.set_yticklabels([])
        plt.savefig(nombre)

#grafica_barras_trimestre_reclamos(lista_archivos[0])
#grafica_barras_compensacion(lista_archivos[1])
#grafica_barras_indicador_tecnico(lista_archivos[2])
#grafica_barras_indicador_tecnico_minutos(lista_archivos[3])
#grafica_barras_indicador_tecnico_horas(lista_archivos[4])
#grafica_pie_tipo_usuario(lista_archivos[5])
#grafica_tabla_sector_consumo(lista_archivos[5])
grafico_barras_consumo(lista_archivos[5])
#velocimetro_cumplimientos_regulatorios(lista_archivos[6])
#grafica_matriz_requerimientos(lista_archivos[7])
#grafica_gastos_AOM(lista_archivos[8], 2021, 2023)
#grafico_barras_usuarios(lista_archivos[5], nuevos=False)
#grafico_barras_usuarios(lista_archivos[5], nuevos=True)

