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
from PIL import Image,ImageDraw,ImageFont
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

global grupo_vanti, lista_filiales, dic_filiales, dic_filiales_largo, limite_facturas, porcentaje_ISRT, dic_nom_eventos,dic_sectores_consumo,dic_sectores_consumo_ordenados,dic_sectores_consumo_imagenes,dic_estratos,dic_industrias,lista_filiales_corto
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
grupo_vanti = "Grupo Vanti"
dic_nom_eventos = {"CONTROLADO" : "Controlados",
                    "NO CONTROLADO" : "No Controlados"}
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
        cmap = LinearSegmentedColormap.from_list("Purple", ["#815081","#b396b3"])
        grad = np.atleast_2d(np.linspace(0, 1, 256)).T
        grad = cmap(grad)
        colors = [cmap(i/3) for i in range(4)]
        c = 0
        for filial in lista_filiales:
            valores = dic_grafica[filial]
            fig, ax = plt.subplots(figsize=(30, 15))
            x = np.arange(len(lista_periodos))  # Adjust x-coordinates
            ax.set_xticks(x)  # Adjust x-ticks
            ax.set_xticklabels(lista_periodos)
            for i in range(len(lista_periodos)):
                ax.bar(x[i], valores[i], color=colors[i])  # Use align='edge' and adjust x-coordinates
            for i in range(len(lista_periodos)):
                ax.text(x[i], valores[i] + 0.15, f"{valores[i]}%", ha='center', va='bottom', fontsize=34, color=colors[0])
            ax.set_title(f'Relación de reclamos por cada 10.000 facturas\nexpedidas {dic_filiales[filial]}', color=colors[0],fontsize=36, y=1.05)
            ax.tick_params(axis='x', colors=colors[0],labelsize=25)
            ax.tick_params(axis='y', colors=colors[0],size=0)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.text(x=-0.9, y=limite_facturas+0.1, s=f'{limite_facturas} %', color='#5a385a', fontsize=28)
            ax.axhline(xmin=-0.4, xmax=2, y=limite_facturas, linestyle='--', color='#5a385a', label=f'Límite regulatorio ({limite_facturas}%)',linewidth=4)
            ax.legend(bbox_to_anchor=(0.5, -0.08), loc='upper center',
                        borderaxespad=0.0, fontsize=28, labelcolor='#805181')
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_xlim(-0.9,3.6)
            lista_archivo = archivo.split("\\")
            lista_archivo.insert(-1, "Imagenes")
            archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
            n_imagen = archivo_copia.replace('.csv',f'_{filial}.png')
            plt.savefig(n_imagen)
            plt.close()
            if c == 0:
                c+=1
                imagen = Image.open(n_imagen)
                recorte = (1100, 1420, imagen.width-1000, imagen.height)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(archivo_copia.replace('.csv','_limite.png'))
            imagen = Image.open(n_imagen)
            recorte = (330, 5, imagen.width-220, imagen.height-75)
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
                    ax.text(mid_angle*0.5, 1.8, f'{value}%', ha='center', va='center', fontsize=15, color=colors[i])
                else:
                    ax.text(mid_angle*0.5, 1.5, f'{value}%', ha='center', va='center', fontsize=15, color=colors[i])
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
            n_imagen = archivo_copia.replace(".csv", f"_cumplimientos_regulatorios_{dic_filiales_largo[dic_cumplimientos_reporte[filial]]}.png")
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
                                ncol=2, borderaxespad=0.0, fontsize=20)
        plt.title("Cantidad de requerimientos solicitados \n(Acumulado año)", fontsize=25, color=colors[-1], y=0.97)
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
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df['Porcentaje gastos'] = df['Porcentaje gastos'].str.replace(" %", "").astype(float)
        df['Valor millones'] = (round(df['Valor'] / 1000000,2)).astype(str) + ' M'
        lista_colores = ["#924e8c","#e87722","#00c7b1","#d50032"]
        lista_filiales = list(df["Filial"].unique())
        for filial in lista_filiales:
            matriz = []
            matriz_1 = []
            matriz_3 = []
            df_filial = df[df["Filial"] == filial]
            anios = list(df_filial["Año"].unique())
            lista_negocios = list(df_filial["Negocio"].unique())
            for negocio in lista_negocios:
                matriz.append(list(df_filial[df_filial["Negocio"]==negocio]["Porcentaje gastos"]))
                matriz_1.append(list(df_filial[df_filial["Negocio"]==negocio]["Valor"]))
                matriz_3.append(list(df_filial[df_filial["Negocio"]==negocio]["Valor millones"]))
            matriz_2 = cambio_matriz_AOM(matriz_1)
            fig, ax = plt.subplots(figsize=(24,16))
            x = range(len(anios))
            v_max = max_columna_matriz(matriz_1)
            v_cambio = v_max*0.065
            for i in range(len(matriz)):
                line1, = ax.plot(x, matriz_2[i], marker='o', label=lista_negocios[i], color=lista_colores[i], linewidth=3)
            for j in range(len(matriz[0])):
                for i in range(len(matriz)):
                    ax.annotate(f'{matriz_3[i][j]} ({matriz[i][j]}) %', xy=(j, matriz_2[i][j]-v_cambio), xytext=(0, 10),
                            textcoords='offset points', ha='center', va='bottom', 
                            color=lista_colores[i], fontsize=20)
            ax.set_ylim(-v_cambio*0.5, v_max*1.03)
            ax.yaxis.set_major_locator(ticker.AutoLocator())
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1e9:.1f} m M'))
            for tick in ax.yaxis.get_major_ticks():
                tick.label1.set_color(lista_colores[0])
                tick.label1.set_fontsize(24)
                tick.set_pad(-12)
            ax.set_xlim(-0.3,len(anios)-0.88)
            ax.set_xticks(x)
            ax.set_xticklabels(anios, color=lista_colores[0], fontsize=24)
            ax.set_title(f"Gastos AOM (M COP 31-dic-{anio})\npara {filial}",
                    fontsize=27, color=lista_colores[0], y=1.01)
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.legend(bbox_to_anchor=(0.5, -0.055), loc='upper center',
                        ncol=4, borderaxespad=0.0, fontsize=18)
            archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
            n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}.png")
            plt.savefig(n_imagen)
            plt.close()
            c = 0
            if c == 0:
                c+=1
                imagen = Image.open(n_imagen)
                recorte = (490, 1482, imagen.width-430, imagen.height-52)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(archivo_copia.replace(".csv", "_limite.png"))
            imagen = Image.open(n_imagen)
            recorte = (110, 55, imagen.width-140, imagen.height-120)
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
        lista_colores = [["#a84bff","#3c0074"],
                        ["#9e1626","#da142c"],
                        ["#f29f12","#fcb741"],
                        ["#0e2395","#1637ef"],
                        ["#0f3654","#fdc743"]]
        dic = {"Consumo m3":"Metros cúbicos de GN consumidos para\n"}
        llave = list(dic.keys())[0]
        valor = list(dic.values())[0]
        for pos in range(len(lista_filiales)):
            filial = lista_filiales[pos]
            df_filtro = df[(df["Filial"]==filial) & (df["Tipo de usuario"]!="Total") & (df["Sector de consumo"]=="Total")]
            labels = list(df_filtro["Tipo de usuario"])
            sizes = list(df_filtro[llave])
            plt.figure(figsize=(10,7))
            plt.pie(sizes, labels=labels, autopct=lambda p : '{:.2f} M'.format(p * sum(sizes) / 100000000), colors=lista_colores[pos], textprops={'fontsize': 24,'color':'white'}, wedgeprops={'linewidth': 4, 'edgecolor': 'none'})
            plt.legend(bbox_to_anchor=(0.5, 0.01), loc='upper center',
                                    ncol=3, borderaxespad=0.0, fontsize=20)
            plt.title(f'{valor}{filial} ({fecha[0]}/{fecha[1]})', color=lista_colores[pos][0], fontsize=25)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}_pie_consumo_m3.png")
            plt.savefig(n_imagen)
            plt.close()
            imagen = Image.open(n_imagen)
            recorte = (0, 0, imagen.width, imagen.height-20)
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
        ax.set_title(f'Consumo GN (Millones m3) por el {grupo_vanti}', color=colors[0],fontsize=25, y=1.02)
        ax.tick_params(axis='x', colors=colors[0],labelsize=15)
        ax.tick_params(axis='y', colors=colors[0],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.08)
        ax.set_yticks([])
        ax.set_yticklabels([])
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        n_imagen = archivo_copia.replace('_reporte_consumo_sumatoria.csv','_consumo.png')
        plt.savefig(n_imagen)
        plt.close()
        informar_imagen(n_imagen)

def grafico_usuarios(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        titulo = f"Cantidad de usuarios (millones) para el {grupo_vanti}"
        nombre = archivo_copia.replace('_reporte_consumo_sumatoria.csv','_usuarios.png')
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
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
        v_max = max(lista_usuarios)*1.01
        fig, ax = plt.subplots(figsize=(18, 12))
        x = range(12)
        bar_width = 0.75
        line1, = ax.plot(lista_periodos, lista_usuarios, marker='o', label='Porcentaje de crecimiento', color="#e78c13")
        line2, = ax.plot(lista_periodos, lista_usuarios, marker='o', label='Nuevos usuarios', color="#0f9324")
        line3, = ax.plot(lista_periodos, lista_usuarios, marker='o', label='Cantidad de usuarios (millones)', color="#1b0fa8")
        for i in range(len(lista_periodos)):
            ax.annotate(f'{lista_usuarios_millones[i]}', xy=(i, lista_usuarios[i]+v_cambio), xytext=(0, 10),
                        textcoords='offset points', ha='center', va='bottom', color="#1b0fa8", fontsize=24)
            ax.annotate(f'{lista_usuarios_nuevos[i]}', xy=(i, lista_usuarios[i] - v_cambio*12), xytext=(0, 10),
                        textcoords='offset points', ha='center', va='bottom', color="#0f9324", fontsize=24)
            ax.annotate(f'{lista_porcentaje[i]}', xy=(i, lista_usuarios[i] - v_cambio*20), xytext=(0, 10),
                        textcoords='offset points', ha='center', va='bottom', color="#e78c13", fontsize=24)
        ax.set_title(titulo, color="#1b0fa8",fontsize=30, y=1.02)
        ax.tick_params(axis='x', colors="#1b0fa8",labelsize=15)
        ax.tick_params(axis='y', colors="#1b0fa8",size=0)
        ax.set_ylim(v_min, v_max)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(bottom=0.18, top=0.93, right=0.991, left=0.01)
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticks(x)
        ax.tick_params(axis='x', labelrotation=35)
        ax.set_xticklabels(lista_periodos, fontsize=22)
        plt.legend(bbox_to_anchor=(0.5, -0.16), loc='upper center',
                                ncol=3, borderaxespad=0.0, fontsize=22)
        ax.set_ylim(v_min, v_max)
        plt.savefig(nombre)
        plt.close()
        informar_imagen(nombre)

def grafica_pie_usuarios(archivo, fecha):
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
        lista_colores = [["#8e007e","#690f67",
                        "#67127c","#481658",
                        "#00186c","#00004f"],
                        ["#95b634","#64731e",
                        "#329542","#006750",
                        "#008489","#005452"]]
        lista_sector_consumo = list(df["Sector de consumo"].unique())
        dic = {"Regulados":{},
                "No regulados":{}}
        dic_total = {"Regulados":0,
                "No regulados":0}
        for sector_consumo in lista_sector_consumo:
            df_sector = df[df["Sector de consumo"] == sector_consumo]
            cantidad = df_sector["Cantidad de usuarios"].sum()
            if cantidad:
                if sector_consumo in dic_estratos:
                    if dic_estratos[sector_consumo] not in dic["Regulados"]:
                        dic["Regulados"][dic_estratos[sector_consumo]] = [0,0]
                    dic["Regulados"][dic_estratos[sector_consumo]][0] += cantidad
                    dic_total["Regulados"] += cantidad
                elif sector_consumo in dic_industrias:
                    if dic_industrias[sector_consumo] not in dic["No regulados"]:
                        dic["No regulados"][dic_industrias[sector_consumo]] = [0,0]
                    dic["No regulados"][dic_industrias[sector_consumo]][0] += cantidad
                    dic_total["No regulados"] += cantidad
        for llave, dic_llave in dic.items():
            lista_labels = list(dic_llave.keys())
            lista_valores = []
            lista_porcentajes = []
            for sector_consumo, lista_sector_consumo in dic_llave.items():
                dic[llave][sector_consumo][1] = round(dic[llave][sector_consumo][0]/dic_total[llave]*100,2)
                lista_valores.append(dic[llave][sector_consumo][0])
                lista_porcentajes.append(dic[llave][sector_consumo][1])
            nueva_lista_labels = []
            for i in range(len(lista_labels)):
                nueva_lista_labels.append(f"{lista_labels[i]} ({round(lista_valores[i]/1e3,1)} m - {lista_porcentajes[i]} %)")
            labels = nueva_lista_labels
            sizes = lista_valores
            plt.figure(figsize=(16,14))
            if llave == "Regulados":
                texto = f"Usuarios residenciales del {grupo_vanti}"
                v_lista_colores = lista_colores[0]
                plt.pie(sizes, labels=labels, textprops={'fontsize': 30,'color':'white'},colors=v_lista_colores, wedgeprops={'linewidth': 4, 'edgecolor': 'none'}, startangle=0, explode=[0.05]*len(lista_labels))
            else:
                texto = f"Usuarios industriales del {grupo_vanti}"
                v_lista_colores = lista_colores[1]
                plt.pie(sizes, labels=labels, textprops={'fontsize': 30,'color':'white'},colors=v_lista_colores, wedgeprops={'linewidth': 4, 'edgecolor': 'none'}, startangle=0)
            plt.legend(bbox_to_anchor=(0.5, 0.018), loc='upper center',
                                    ncol=2, borderaxespad=0.0, fontsize=22)
            plt.title(f'{texto} ({fecha[0]}/{fecha[1]})', fontsize=30, color = v_lista_colores[-1])
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.subplots_adjust(bottom=0.18)
            texto = llave.lower().replace(" ","_")
            n_imagen = archivo_copia.replace("_reporte_consumo_sumatoria.csv", f"_pie_{texto}.png")
            plt.savefig(n_imagen)
            plt.close()
            imagen = Image.open(n_imagen)
            recorte = (50, 55, imagen.width-10, imagen.height-85)
            imagen_recortada = imagen.crop(recorte)
            imagen_recortada.save(n_imagen)
            informar_imagen(n_imagen)

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
        ax.set_title(f'Valor compensado por el {grupo_vanti} (COP)', color=colors[0],fontsize=25, y=1.05)
        ax.tick_params(axis='x', colors=colors[0],labelsize=15)
        ax.tick_params(axis='y', colors=colors[0],size=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        plt.subplots_adjust(left=-0.03, right=1.02, top=0.92, bottom=0.08)
        ax.set_yticks([])
        ax.set_yticklabels([])
        n_imagen = archivo_copia.replace('.csv','.png')
        plt.savefig(n_imagen)
        plt.close()
        informar_imagen(n_imagen)

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
            i+=1
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
        lista_colores = ["#a6194a","#fd8c25","#0391ce"]
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
            data = np.array(list(dic_grafica.values())).T
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
                    ax.text(bar.get_x() + bar.get_width()/2, 100.25, f"{value:.2f}%", color=lista_colores[i], ha="center", va="bottom", fontsize=28, rotation=90)
            ax.set_xticks(x + bar_width)
            ax.set_xticklabels(nueva_lista_periodos, color=lista_colores[1], fontsize=18)
            ax.set_title(f"Indicadores técnicos para la filial {filial}", fontsize=34, color=lista_colores[1], y=1)
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
            plt.savefig(n_imagen)
            plt.close()
            c = 0
            if c == 0:
                c+=1
                imagen = Image.open(n_imagen)
                recorte = (950, 1330, imagen.width-870, imagen.height-20)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(archivo_copia.replace('.csv','_limite.png'))
            imagen = Image.open(n_imagen)
            recorte = (380, 90, imagen.width-300, imagen.height-75)
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
        for sector_consumo in lista_sector_consumo:
            if sector_consumo in dic_estratos:
                df_sector = df_filiales[df_filiales["Sector de consumo"]==sector_consumo]
                lista_cantidad.append(abs(df_sector["Subsidios"].sum()))
                lista_labels.append(dic_estratos[sector_consumo])
        labels = lista_labels
        sizes = lista_cantidad
        colors = ["#053280","#1a6eff"]
        plt.figure(figsize=(11,10))
        plt.pie(sizes, labels=labels, colors=colors, autopct=lambda p : '{:.2f} M'.format(p * sum(lista_cantidad) / 1000000), textprops={'fontsize': 24,'color':'white'}, wedgeprops={'linewidth': 5, 'edgecolor': 'none'},startangle=90, explode=[0.02, 0.02],pctdistance=0.5)
        plt.legend(bbox_to_anchor=(0.5, 0.055), loc='upper center',
                                ncol=2, borderaxespad=0.0, fontsize=24)
        plt.title(f"Subsidios otorgados por el {grupo_vanti} ({mes}/{anio})", fontsize=29, color=colors[0], y=0.95)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        n_imagen = archivo_copia.replace("_reporte_consumo_subsidio_sumatoria.csv", "_pie_subsidio.png")
        plt.savefig(n_imagen)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (0, 100, imagen.width-0, imagen.height-80)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)

def grafica_barras_subsidios(archivo):
    n_archivo = archivo
    if os.path.exists(n_archivo):
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = union_listas_df_fecha(df, sep=True)
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
        lista_colores = ["#37858b","#770752"]
        fig, ax = plt.subplots(figsize=(32,12))
        bar_width = 2
        x = range(0,len(matriz[0])*4,4)
        for i in range(len(lista_labels)):
            if i == 0:
                ax.bar(x, matriz[0], bar_width, label=f'{lista_labels[0]}', color=lista_colores[i])
            else:
                ax.bar(x, matriz[i], bar_width, label=f'{lista_labels[i]}', color=lista_colores[i], bottom=matriz[0])
            for j in range(len(matriz[0])):
                valor = round(matriz[i][j]/1e6,1)
                if i == 0:
                    ax.text(x[j], matriz[i][j]*0.2, f"{valor} M", ha='center', fontsize=23, color="white", rotation=90)
                else:
                    ax.text(x[j], matriz[i-1][j]+(matriz[i][j]*0.3), f"{valor} M", ha='center', fontsize=23, color="white", rotation=90)
        ax.set_xticks(x)
        ax.set_xticklabels(lista_fechas, color=lista_colores[1], fontsize=18)
        ax.set_title(f"Subsidios para el {grupo_vanti}", fontsize=30, color=lista_colores[1], y=1.0)
        ax.legend(bbox_to_anchor=(0.5, -0.095), loc='upper center',
                        ncol=3, borderaxespad=0.0, fontsize=20)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1000000000:.0f} m M'))
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_color(lista_colores[1])
            tick.label1.set_fontsize(20)
            tick.set_pad(17)
        n_imagen = archivo_copia.replace("_reporte_consumo_subsidio_sumatoria.csv", "_subsidios_estratos.png")
        plt.savefig(n_imagen)
        plt.close()
        imagen = Image.open(n_imagen)
        recorte = (200, 60, imagen.width-300, imagen.height)
        imagen_recortada = imagen.crop(recorte)
        imagen_recortada.save(n_imagen)
        informar_imagen(n_imagen)

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
        ax.set_title(f'Contribuciones generadas por el {grupo_vanti} (COP)', color=colors[0],fontsize=29, y=1.03)
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
            fig, ax = plt.subplots(figsize=(24,16))
            for i, (llave, valor) in enumerate(dic_grafica.items()):
                lista_llaves = list(valor.keys())
                lista_valores = list(valor.values())
                x = range(0,len(lista_periodos)*3,3)
                v_max = max(lista_valores[0])
                v_min = min(lista_valores[0])
                if v_max < 15:
                    v_cambio = 2
                else:
                    v_cambio = v_max*0.13
                line2, = ax.plot(x, lista_valores[0], marker='o', label=f"Evento No Controlado ({lista_llaves[1]})", color="#9c0ecf", linewidth=3)
                line1, = ax.plot(x, lista_valores[0], marker='o', label=f"Evento No Controlado ({lista_llaves[0]})", color="#0a1898", linewidth=3)
            for j in range(len(lista_periodos)):
                ax.annotate(f'{lista_valores[1][j]}', xy=(x[j], lista_valores[0][j] + v_cambio*0.4), xytext=(0, 10),
                            textcoords='offset points', ha='center', va='bottom', color="#9c0ecf", fontsize=25)
                ax.annotate(f'{lista_valores[0][j]}', xy=(x[j], lista_valores[0][j] - v_cambio*0.9), xytext=(0, 10),
                            textcoords='offset points', ha='center', va='bottom', color="#0a1898", fontsize=25)
            ax.set_title(f"Eventos No Controlados para {filial}", color="#0a1898",fontsize=30, y=1.02)
            ax.tick_params(axis='x', colors="#0a1898",labelsize=15)
            ax.tick_params(axis='y', colors="#0a1898",size=0)
            if v_max < 15:
                ax.set_ylim(-3, v_max*1.2)
            else:
                ax.set_ylim(v_min*0.7, v_max*1.25)
            for spine in ax.spines.values():
                spine.set_visible(False)
            plt.subplots_adjust(bottom=0.25)
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_xticks(x)
            ax.tick_params(axis='x', labelrotation=35)
            ax.set_xticklabels(lista_periodos, fontsize=22)
            plt.legend(bbox_to_anchor=(0.5, -0.20), loc='upper center',
                                    ncol=2, borderaxespad=0.0, fontsize=24)
            n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}.png")
            plt.savefig(n_imagen)
            plt.close()
            if c == 0:
                c+=1
                imagen = Image.open(n_imagen)
                recorte = (470, 1390, imagen.width-420, imagen.height-130)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(archivo_copia.replace(".csv", f"_limite.png"))
            imagen = Image.open(n_imagen)
            recorte = (270, 95, imagen.width-200, imagen.height-250)
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
                            ax.text(j, base[j]+v_max*0.03, f"{lista_valores[i][j]}", ha='center', fontsize=19, color=lista_colores[-1])
                ax.set_xticks(np.arange(24))
                ax.set_xlabel("Franja horaria", color = lista_colores[0],fontsize=22)
                ax.set_ylabel("Cantidad de eventos", color = lista_colores[0],fontsize=22)
                ax.set_xticklabels(range(24), color=lista_colores[0], fontsize=19)
                ax.set_title(f"Duración eventos {dic_nom_eventos[evento]} por franja horaria para\n{filial} ({fecha[0][0]}/{fecha[0][1]} - {fecha[1][0]}/{fecha[1][1]})", fontsize=25, color=lista_colores[0], y=1.01)
                ax.legend(bbox_to_anchor=(0.5, -0.085), loc='upper center',
                                ncol=3, borderaxespad=0.0, fontsize=15)
                for spine in ax.spines.values():
                    spine.set_visible(False)
                ax.yaxis.set_major_locator(ticker.AutoLocator())
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x:.0f}'))
                for tick in ax.yaxis.get_major_ticks():
                    tick.label1.set_color(lista_colores[0])
                    tick.label1.set_fontsize(19)
                    tick.set_pad(8)
                ax.set_ylim(0, v_max*1.15)
                nombre_evento = evento.replace(" ","_")
                n_imagen = archivo_copia.replace(".csv", f"_{dic_filiales_largo[filial]}_{nombre_evento}.png")
                plt.savefig(n_imagen)
                plt.close()
                c = 0
                if c == 0:
                    c+=1
                    imagen = Image.open(n_imagen)
                    recorte = (570, 1140, imagen.width-540, imagen.height-10)
                    imagen_recortada = imagen.crop(recorte)
                    imagen_recortada.save(archivo_copia.replace(".csv", f"_limite_{nombre_evento}.png"))
                imagen = Image.open(n_imagen)
                recorte = (180, 50, imagen.width-275, imagen.height-55)
                imagen_recortada = imagen.crop(recorte)
                imagen_recortada.save(n_imagen)
                informar_imagen(n_imagen)

def func(pct, allvalues):
    absolute = int(pct / 100. * sum(allvalues))  # Calcula el valor absoluto
    if absolute < 10:
        return ''  # No mostrar porcentaje si es menor a 10
    else:
        return f'{pct:.1f}%'

def mapa_tarifas(n_archivo, fecha):
    x_pie = 800
    x_texto = 1150
    if os.path.exists(n_archivo):
        df_ubicaciones = pd.read_csv(ruta_constantes+"mercado_relevante_ubi.csv", sep=",", encoding="utf-8-sig")
        lista_archivo = n_archivo.split("\\")
        lista_archivo.insert(-1, "Imagenes")
        df = pd.read_csv(n_archivo, sep=",", encoding="utf-8-sig")
        df = df[(df["Anio_reportado"]==int(fecha[0]))&(df["Mes_reportado"]==fecha[1])]
        llaves_por = ["Porcentaje G","Porcentaje T","Porcentaje D", "Porcentaje P_perdidas"]
        for llave in llaves_por:
            df[llave] = df[llave].str.replace(" %", "").astype(float)
        colors = ["#ea7916","#2db6cf","#4eb6a8","#815081","#05106d"]
        colors_pie = ["#5e1cbb","#2fa711","#1029c0","#ca1313"]
        for filial in lista_filiales_corto:
            ruta_mapa_filial = ruta_constantes+f"mapa_{filial.lower()}.png"
            imagen = Image.open(ruta_mapa_filial)
            dibujo = ImageDraw.Draw(imagen)
            ancho, alto = imagen.size
            df_filial = df_ubicaciones[df_ubicaciones["Mapa"]==filial].reset_index(drop=True)
            lista_archivo_limite = lista_archivo.copy()
            lista_archivo[-1] = f"mapa_{filial.lower()}.png"
            lista_archivo_limite[-1] = f"mapa_limite.png"
            archivo_copia = mod_1.lista_a_texto(lista_archivo,"\\")
            archivo_limite = mod_1.lista_a_texto(lista_archivo_limite,"\\")
            radio = 12
            tamanio = 50
            fuente = ImageFont.truetype("arial.ttf", tamanio)
            largo = len(df_filial)
            seperacion = (alto-tamanio*largo)/(largo+1)
            for pos in range(largo):
                texto = df_filial["Nombre"][pos]
                x = df_filial["pos_x"][pos]
                y = df_filial["pos_y"][pos]
                mercado = df_filial["Id_mercado"][pos]
                dibujo.ellipse((x-radio,y-radio,x+radio,y+radio),fill=colors[pos])
                ubi_y = seperacion + (pos*(tamanio+seperacion))
                dibujo.text((x_texto,ubi_y-15), texto, fill=colors[pos], font=fuente)
                df_mercado = df[df["ID_Mercado"]==int(mercado)].reset_index(drop=True)
                if len(df_mercado):
                    cuf = round(df_mercado["Cuf"][0])
                    cuv = round(df_mercado["Cuv"][0])
                    cuf_1000 = cuf%1000
                    if len(str(cuf_1000)) < 3:
                        cuf_1000 = str(cuf_1000)+"0"*(3-len(str(cuf_1000)))
                    cuv_1000 = cuv%1000
                    if len(str(cuv_1000)) < 3:
                        cuv_1000 = str(cuv_1000)+"0"*(3-len(str(cuv_1000)))
                    texto_cuf = f"Cuf: ${cuf//1000}.{cuf_1000}"
                    texto_cuv = f"Cuv: ${cuv//1000}.{cuv_1000}"
                    dibujo.text((x_texto,ubi_y+tamanio+5-15), texto_cuf, fill=colors[pos], font=ImageFont.truetype("arial.ttf", 30))
                    dibujo.text((x_texto,ubi_y+tamanio+35-15), texto_cuv, fill=colors[pos], font=ImageFont.truetype("arial.ttf", 30))
            imagen.save(archivo_copia)
            archivo_copia_apoyo = archivo_copia.replace(".png","_apoyo.png")
            background = Image.open(archivo_copia)
            c = 0
            for pos in range(largo):
                mercado = df_filial["Id_mercado"][pos]
                ubi_y = (seperacion-55) + (pos*(tamanio+seperacion))
                df_mercado = df[df["ID_Mercado"]==int(mercado)].reset_index(drop=True)
                if len(df_mercado):
                    labels = ["Suministro","Transporte","Distribución","Pérdidas"]
                    sizes = []
                    for llave in llaves_por:
                        sizes.append(df_mercado[llave][0])
                    fig, ax = plt.subplots(figsize=(1, 1), dpi=225)
                    ax.pie(sizes, labels=[''] * len(sizes), autopct=lambda pct: func(pct, sizes), colors=colors_pie, startangle=180, textprops={'fontsize': 5,'color':'white'})
                    fig.savefig(archivo_copia_apoyo, transparent=True, bbox_inches='tight')
                    plt.close(fig)
                    pie_chart = Image.open(archivo_copia_apoyo)
                    background.paste(pie_chart, (int(x_pie), int(ubi_y)), pie_chart)
                    background.save(archivo_copia)
                    mod_1.eliminar_archivos([archivo_copia_apoyo])
                    if c == 0:
                        c += 1
                        plt.figure(figsize=(15,15))
                        plt.pie(sizes, labels=labels, colors=colors_pie)
                        plt.legend(bbox_to_anchor=(0.5, 0.01), loc='upper center',
                                                ncol=4, borderaxespad=0.0, fontsize=20)
                        plt.savefig(archivo_limite)
                        plt.close()
                        imagen = Image.open(archivo_limite)
                        recorte = (220, 1310, imagen.width-170, imagen.height-120)
                        imagen_recortada = imagen.crop(recorte)
                        imagen_recortada.save(archivo_limite)
            informar_imagen(archivo_copia)