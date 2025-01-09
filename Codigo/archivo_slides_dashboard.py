import matplotlib.font_manager as font_manager
import os
from PIL import Image, ImageDraw, ImageFont
import json
import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos,ruta_fuentes,ruta_imagenes,fuente_texto,azul_vanti,dic_colores,meta_kpi_sub,dic_ubi_tarifas,dic_distri,dic_colores_distri,dic_ubi_disti
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
ruta_fuentes = mod_rp.v_fuentes()
ruta_imagenes = mod_rp.v_imagenes()
global ruta_fuente,grupo_vanti
grupo_vanti = "Grupo Vanti"
ruta_fuente = ruta_fuentes+"Muli.ttf"
ruta_fuente_negrilla = ruta_fuentes+"Mulish-Bold.ttf"
fuente_texto = font_manager.FontProperties(fname=ruta_fuentes+"Muli.ttf")

def leer_archivos_json(archivo):
    with open(archivo) as file:
            data = json.load(file)
    return data
dic_colores = leer_archivos_json(ruta_constantes+"colores.json")["datos"]
azul_vanti = dic_colores["azul_v"]
meta_kpi_sub = "1,4"
valor_x = 10
dic_ubi_tarifas = {"VANTI":{23:[[(1155-valor_x,660),(1390-valor_x,895)],(1375,695)],
                            113:[[(1155-valor_x,180),(1390-valor_x,415)],(1375,240)],
                            139:[[(0,180),(235,415)],(245,240)],
                            149:[[(0,660),(235,895)],(245,695)]},
                    "GNCB":{106:[[(555-8,800),(790-8,1035)],(818,840)],
                            1825:[[(1120-valor_x,545),(1355,780)],(1395,580)],
                            169:[[(0,545),(235,780)],(266,585)]},
                    "GNCR":{80:[[(1295,625),(1530,860)],(1175,425)],
                            21:[[(150,625),(385,860)],(45,425)]},
                    "GOR":{11:[[(1145-valor_x,550),(1380-valor_x,785)],(1365,580)],
                            9:[[(580-valor_x,800),(815-valor_x,1035)],(810,840)],
                            16:[[(0,550),(235,785)],(250,570)]}}
dic_colores_tarifas = {23:dic_colores["naranja_v"],
                        113:dic_colores["azul_agua_v"],
                        139:dic_colores["verde_v"],
                        149:dic_colores["morado_v"],
                        106:dic_colores["naranja_v"],
                        1825:dic_colores["verde_v"],
                        169:dic_colores["azul_agua_v"],
                        80:dic_colores["verde_v"],
                        21:dic_colores["azul_agua_v"],
                        11:dic_colores["naranja_v"],
                        9:dic_colores["azul_agua_v"],
                        16:dic_colores["verde_v"]}
dic_colores_distri = {"GNCB":dic_colores["naranja_v"],
                "GNCR":dic_colores["morado_v"],
                "LLANOGAS":dic_colores["azul_v"],
                "VANTI":dic_colores["verde_v"],
                "EPM":dic_colores["azul_agua_c_v"],
                "GOR":dic_colores["azul_agua_v"],
                "SURTIGAS":dic_colores["morado_c_v"],
                "EFIGAS":dic_colores["naranja_c_v"],
                "GASCARIBE":dic_colores["rosa_p1"],
                "GDO":dic_colores["amarillo_v"],
                "METROGAS":dic_colores["azul_p3"],
                "ALCANOS":dic_colores["vinotinto"]}
dic_distri = {"GNCB":"Gas Natural Cundiboyacense S.A. ESP.",
                "GNCR":"Gas Nacer S.A. ESP.",
                "LLANOGAS":"Llanogas S.A. ESP.",
                "VANTI":"Vanti S.A. ESP.",
                "EPM":"EPM",
                "GOR":"Gas Natural del Oriente S.A. ESP.",
                "SURTIGAS":"Surtigas S.A. ESP.",
                "EFIGAS":"Efigas S.A. ESP.",
                "GASCARIBE":"Gases del Caribe S.A. ESP.",
                "GDO":"Gases de Occiente S.A. ESP.",
                "METROGAS":"Metrogas de Colombia S.A. ESP.",
                "ALCANOS":"Alcanos de Colombia S.A. ESP."}
dic_ubi_disti = {"GNCB":(415,475),
                "GNCR":(385,290),
                "LLANOGAS":(420,585),
                "VANTI":(360,535),
                "EPM":(305,420),
                "GOR":(405,380),
                "SURTIGAS":(276,286),
                "EFIGAS":(278,506),
                "GASCARIBE":(334,210),
                "GDO":(208,622),
                "METROGAS":(392,432),
                "ALCANOS":(295,655)}

def acortar_nombre(nombre, cantidad=6):
    lista_nombre = nombre.split("\\")
    largo = len(lista_nombre)
    if largo > cantidad:
        texto = ("...\\"+lista_a_texto(lista_nombre[largo-cantidad:], "\\", False)).replace("\\\\","\\")
    else:
        texto = texto.replace("\\\\","\\")
    return texto

def lista_a_texto(lista, separador, salto=False):
    lista = [str(elemento) for elemento in lista]
    texto = separador.join(lista)
    if salto:
        texto += "\n"
    return texto

def conversion_decimales(texto):
    return str(texto).replace(".",",")

def conversion_miles(num):
    try:
        valor = int(num)
        if valor >= 1000:
            return f"{(valor/1e3):.3f}"
        else:
            return str(valor)
    except BaseException:
        return num

def ubicacion_imagen(nueva_imagen, espacio):
    ancho, alto = nueva_imagen.size
    tamanio = (abs(espacio[0][0]-espacio[1][0]),abs(espacio[0][1]-espacio[3][1]))
    if alto > tamanio[1]:
        escalar = tamanio[1]/alto
    else:
        escalar = alto/tamanio[1]
    if int(ancho*escalar) > tamanio[0]:
        nueva_imagen = nueva_imagen.resize((tamanio[0],int(alto*escalar)))
    else:
        nueva_imagen = nueva_imagen.resize((int(ancho*escalar), tamanio[1]))
    ancho, alto = nueva_imagen.size
    posicion = (espacio[0][0]+(abs(espacio[1][0]-espacio[0][0]-ancho)//2),abs(espacio[0][1]))
    return nueva_imagen,posicion

def slide_portada(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide, thread=None):
    try:
        plantilla = ruta_imagenes+"p1.png"
        imagen = Image.open(plantilla)
        dibujo = ImageDraw.Draw(imagen)
        dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
        dibujo.text((360,230), conversion_decimales(dic_metricas["total_ventas"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((920,230), str(dic_metricas["nuevos_usuarios"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1500,260), str(dic_metricas["cantidad_emergencias"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1500,560), str(dic_metricas["tiempo_emergencias"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1380,790), str(dic_metricas["usuarios_eventos"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((1440,890), str(dic_metricas["cantidad_eventos"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((850,790), str(dic_metricas["usuarios_compensados"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        dibujo.text((810,890), "$ "+str(dic_metricas["valor_compensado"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
        valor = conversion_decimales(str(round(100-((dic_metricas["Cumplimientos_SUI"]["Distribuidoras"]["Pendiente"]/dic_metricas["Cumplimientos_SUI"]["Distribuidoras"]["Certificado"])*100),2)))+" %"
        texto_rotado = Image.new('RGBA', (140, 50), (255, 255, 255, 0))
        draw = ImageDraw.Draw(texto_rotado)
        draw.text((0, 0), valor, fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente_negrilla, 30))
        texto_rotado = texto_rotado.rotate(90, expand=True)
        imagen.paste(texto_rotado, (98, 470), texto_rotado)
        ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
        esp = [(170,440),(620,440),(620,670),(170,670)]
        nueva_imagen = ubi_imagen+"porcentaje_cumplimientos_regulatorios_grupo_vanti.png"
        if  os.path.exists(nueva_imagen):
            nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
            nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
            imagen.paste(nueva_imagen, pos, nueva_imagen)
        else:
            if thread:
                thread.message_sent.emit(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}", "red")
            else:
                print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
        esp = [(170,770),(620,770),(620,995),(170,995)]
        nueva_imagen = ubi_imagen+"porcentaje_matriz_requerimientos.png"
        if  os.path.exists(nueva_imagen):
            nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
            nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
            imagen.paste(nueva_imagen, pos, nueva_imagen)
        else:
            if thread:
                thread.message_sent.emit(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}", "red")
            else:
                print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
        ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
        esp = [(730,440),(1180,440),(1180,670),(730,670)]
        nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_grupo_vanti_pie_consumo_m3.png"
        if  os.path.exists(nueva_imagen):
            nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
            nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
            imagen.paste(nueva_imagen, pos, nueva_imagen)
        else:
            if thread:
                thread.message_sent.emit(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}", "red")
            else:
                print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
        imagen.save(ubi+f"slide_{c_slide}.png")
        c_slide += 1
        return c_slide
    except BaseException:
        pass

def cargar_imagen(imagen, nombre_imagen, esp):
    if  os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen)
        nueva_imagen,pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos)
        imagen.save(nombre_imagen)
    else:
        print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")

def slide_def_1(ubi,fecha,fecha_actual, dic_metricas,mes_corte,fecha_anio_anterior,c_slide):
    try:
        lista_plantilla = ["p2","p3","p6","p29","p4","p5"]
        for i in lista_plantilla:
            plantilla = ruta_imagenes+f"{i}.png"
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            color = azul_vanti
            if i == "p2":
                color = "white"
            if i == "p6":
                dibujo.text((1440,525), str(dic_metricas["usuarios"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente_negrilla, 60))
                dibujo.text((1522,990), "* Cifras a "+mes_corte, fill=dic_colores["azul_v"], font=ImageFont.truetype(ruta_fuente, 20))
                dibujo.text((760,1025), f"Último corte: {fecha_anio_anterior}", fill=color, font=ImageFont.truetype(ruta_fuente, 30))
            else:
                dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=color, font=ImageFont.truetype(ruta_fuente, 30))
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_usuarios(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p7.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill="white", font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((1480,240), str(dic_metricas["nuevos_usuarios"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1480,450), str(dic_metricas["porcentaje_crecimiento"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1480,660), str(dic_metricas["usuarios_regulados"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1480,870), str(dic_metricas["usuarios_no_regulados"]), fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 60))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(22,320),(1230,320),(1230,900),(22,900)]
            nueva_imagen = ubi_imagen+texto_fecha+"_usuarios.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_pie_usuarios(ubi,fecha,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p8.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((395,920), str(dic_metricas["usarios_residenciales"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
            dibujo.text((1370,920), str(dic_metricas["usarios_no_residenciales"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(120,190),(900,190),(900,820),(120,820)]
            nueva_imagen = ubi_imagen+texto_fecha+"_pie_regulados.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
            esp = [(990,190),(1890,190),(1890,820),(990,820)]
            nueva_imagen = ubi_imagen+texto_fecha+"_pie_no_regulados.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide +=1
        return c_slide
    except BaseException:
        return c_slide

def dibujar_texto_derecha(posicion_final, texto, fill, font, dibujo):
    bbox = dibujo.textbbox((0, 0), texto, font=font)
    ancho_texto = bbox[2] - bbox[0]
    x_inicial = posicion_final[0] - ancho_texto
    y_inicial = posicion_final[1]
    dibujo.text((x_inicial, y_inicial), texto, fill=fill, font=font)

def slide_consumo(ubi,fecha_actual,ubi_carpeta,texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p9.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujar_texto_derecha((1815,200), str(dic_metricas["Demanda"]["Regulados"]["Residencial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,287), str(dic_metricas["Demanda"]["Regulados"]["Comercial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,375), str(dic_metricas["Demanda"]["Regulados"]["Industrial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,498), str(dic_metricas["Demanda"]["No regulados"]["Industrial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,587), str(dic_metricas["Demanda"]["No regulados"]["GNCV"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,669), str(dic_metricas["Demanda"]["No regulados"]["Comercial"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,750), str(dic_metricas["Demanda"]["No regulados"]["Comercializadoras /\nTransportadores"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            dibujar_texto_derecha((1815,838), str(dic_metricas["Demanda"]["No regulados"]["Termoeléctrico"])+" M", fill="white", font=ImageFont.truetype(ruta_fuente, 22), dibujo=dibujo)
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(25,270),(1330,270),(1330,920),(25,920)]
            nueva_imagen = ubi_imagen+texto_fecha+"_consumo.png"
            if os.path.exists(nueva_imagen):
                nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
                nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
                imagen.paste(nueva_imagen, pos, nueva_imagen)
            else:
                print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def pegar_imagen(nueva_imagen, imagen, esp):
    if os.path.exists(nueva_imagen):
        nueva_imagen = Image.open(nueva_imagen).convert("RGBA")
        nueva_imagen, pos = ubicacion_imagen(nueva_imagen,esp)
        imagen.paste(nueva_imagen, pos, nueva_imagen)
    else:
        print(f"No existe la imagen ...{acortar_nombre(nueva_imagen)}")
    return imagen

def slide_pie_consumo(ubi, fecha_actual, ubi_carpeta, texto_fecha, dic_metricas, c_slide):
    try:
        plantilla = ruta_imagenes+"p10.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((850,520), str(dic_metricas["consumo_mes"])+" M", fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 60))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(120,90),(725,90),(725,520),(120,520)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_VANTI_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = [(120,590),(725,590),(725,1020),(120,1020)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_GNCR_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = [(1150,90),(1720,90),(1720,520),(1150,520)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_GNCB_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = [(1150,590),(1720,590),(1720,1020),(1150,1020)]
            nueva_imagen = ubi_imagen+texto_fecha+"_reporte_consumo_sumatoria_GOR_pie_consumo_m3.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_sub_con(ubi, fecha_actual, ubi_carpeta, texto_fecha, c_slide):
    try:
        plantilla = ruta_imagenes+"p11.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            texto = "El valor de las contribuciones para los Transportadores de gas natural en VANTI S.A. ESP. (Diciembre/2023) fue de 50.2 m M"
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            if "2024" in fecha_actual:
                dibujo.text((75,960), texto, fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 20))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = [(22,150),(1895,150),(1895,895),(22,895)]
            nueva_imagen = ubi_imagen+texto_fecha+"_subsidios_estratos.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def ajustar_coordenadas(coor):
    lista = [(coor[0][0],coor[0][1]),(coor[1][0],coor[0][1]),(coor[1][0],coor[1][1]),(coor[0][0],coor[1][1])]
    return lista

def slide_kpi_sub(ubi, fecha_actual, ubi_carpeta, dic_metricas, c_slide, anio):
    try:
        plantilla = ruta_imagenes+"p12.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((215,295), f"Meta {anio}", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((200,332), grupo_vanti, fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((165,535), "Comportamiento", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((265,575), "MME", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((152,778), "Dueda MME - TAM", fill=dic_colores["azul_p3"], font=ImageFont.truetype(ruta_fuente, 40))
            dibujo.text((255,383), str(meta_kpi_sub), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 55))
            dibujo.text((212,630), str(dic_metricas["kpi_subsidios"][0]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 55))
            dibujo.text((182,824), str(dic_metricas["deuda_subsidios"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 55))
            dibujo.ellipse((335,638,400,708), fill=dic_metricas["kpi_subsidios"][1])
            ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
            esp = ajustar_coordenadas([(525,190),(1900,990)])
            nueva_imagen = ubi_imagen+"KPI_subsidios.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_recla_fact(ubi, fecha_actual, ubi_carpeta, c_slide):
    try:
        plantilla = ruta_imagenes+"p13.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
            esp = ajustar_coordenadas([(35,110),(1010,550)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_VANTI.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = ajustar_coordenadas([(985,110),(1860,550)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_GNCB.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = ajustar_coordenadas([(35,625),(1010,1015)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_GNCR.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            esp = ajustar_coordenadas([(985,625),(1860,1015)])
            nueva_imagen = ubi_imagen+"porcentaje_reclamos_facturacion_10000_GOR.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_compensaciones(ubi, fecha_actual, ubi_carpeta, c_slide, texto_fecha):
    try:
        plantilla = ruta_imagenes+"p14.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill="white", font=ImageFont.truetype(ruta_fuente, 30))
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = ajustar_coordenadas([(32,150),(1885,950)])
            nueva_imagen = ubi_imagen+texto_fecha+"_compilado_compensacion.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_AOM(ubi, anio, mes, fecha_actual, ubi_carpeta, c_slide):
    try:
        plantilla = ruta_imagenes+"p15.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((1690,870), f"Valores en precios\nconstantes {mes}/{anio}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 20))
            ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
            esp = ajustar_coordenadas([(70,105),(1650,955)])
            nueva_imagen = ubi_imagen+"Gastos_AOM.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_desviaciones(ubi, fecha_actual, ubi_carpeta, c_slide, texto_fecha, dic_metricas):
    try:
        plantilla = ruta_imagenes+"p16.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            dibujo.text((338,185), str(dic_metricas["usuarios"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 50))
            dibujo.text((315,390), str(dic_metricas["DS"]["Total"])+" ("+str(dic_metricas["DS"]["Porcentaje"])+")", fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 50))
            dibujar_texto_derecha((736,510), str(dic_metricas["DS"]["Consumos reales"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 46), dibujo=dibujo)
            dibujar_texto_derecha((736,615), str(dic_metricas["DS"]["Error en la lectura"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 46), dibujo=dibujo)
            dibujar_texto_derecha((736,735), str(dic_metricas["DS"]["No se logró visita por impedimento"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 46), dibujo=dibujo)
            dibujar_texto_derecha((736,835), str(dic_metricas["DS"]["No realizó visita"]), fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente, 46), dibujo=dibujo)
            ubi_imagen = ubi_carpeta+"\\00. Comercial\\Imagenes\\"
            esp = ajustar_coordenadas([(755,205),(1900,910)])
            nueva_imagen = ubi_imagen+texto_fecha+"_compilado_DS_metricas_categorias.png"
            imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_def_2(ubi, fecha_actual, c_slide):
    try:
        plantilla = ruta_imagenes+"p17.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_def_3(ubi, fecha_actual, c_slide):
    try:
        plantilla = ruta_imagenes+"p23.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_tarifas(ubi, fecha_actual, ubi_carpeta, texto_fecha, dic_metricas,c_slide):
    try:
        dic_tarifas = dic_metricas["tarifas"]
        lista_plantilla = ["p18","p19","p20","p21","p22"]
        lista_filiales = ["VANTI","GNCB","GNCR","GOR"]
        ubi_imagen = ubi_carpeta+"\\01. Tarifario\\Imagenes\\"
        for i in range(len(lista_plantilla)):
            plantilla = ruta_imagenes+lista_plantilla[i]+".png"
            if os.path.exists(plantilla):
                imagen = Image.open(plantilla)
                dibujo = ImageDraw.Draw(imagen)
                dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
                if i < len(lista_filiales):
                    filial = lista_filiales[i]
                    for llave, valor in dic_tarifas[filial].items():
                        esp = ajustar_coordenadas(dic_ubi_tarifas[filial][int(llave)][0])
                        nueva_imagen = ubi_imagen+texto_fecha+f"_rt_{llave}.png"
                        imagen = pegar_imagen(nueva_imagen, imagen, esp)
                        ubi_texto = dic_ubi_tarifas[filial][int(llave)][1]
                        x = ubi_texto[0]
                        y = ubi_texto[1]
                        for j in range(len(valor[1])):
                            texto = valor[1][j]
                            if j < 2:
                                dibujo.text((x,y), texto, fill=dic_colores_tarifas[int(llave)], font=ImageFont.truetype(ruta_fuente_negrilla, 30))
                            else:
                                dibujo.text((x,y), texto, fill=dic_colores_tarifas[int(llave)], font=ImageFont.truetype(ruta_fuente, 30))
                            y += 50
                else:
                    x1 = 866
                    y1 = 80
                    c = 78
                    x2 = 1735
                    x3 = 1780
                    c_1 = 50
                    c_bola = 1
                    for i,j in dic_metricas["Tarifas_nacionales"].items():
                        dibujo.text((x1,y1), dic_distri[i], fill=azul_vanti, font=ImageFont.truetype(ruta_fuente_negrilla, 28))
                        dibujar_texto_derecha((x2,y1), j["Ciudad"]+": "+j["Tarifa"], fill=dic_colores_distri[i], font=ImageFont.truetype(ruta_fuente, 26), dibujo=dibujo)
                        pos = dic_ubi_disti[i]
                        n_pos = (pos[0]-(j["Bola"]*0.5), pos[1]-(j["Bola"]*0.5))
                        dibujo.ellipse((n_pos[0],n_pos[1],n_pos[0]+(j["Bola"]*c_bola),n_pos[1]+(j["Bola"]*c_bola)), fill=dic_colores_distri[i])
                        if j["Cambio"] == "red":
                            nueva_imagen = ruta_imagenes+"up.png"
                        elif j["Cambio"] == "green":
                            nueva_imagen = ruta_imagenes+"down.png"
                        elif j["Cambio"] == "orange":
                            nueva_imagen = ruta_imagenes+"equal.png"
                        imagen = pegar_imagen(nueva_imagen, imagen, ajustar_coordenadas([(x3,y1),(x3+c_1,y1+c_1)]))
                        y1 += c
                imagen.save(ubi+f"slide_{c_slide}.png")
                c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_indicadores(ubi, fecha_actual, ubi_carpeta, c_slide, texto_fecha, dic_metricas, periodo):
    dic_coordendas = {"VANTI":[[(250,108),(890,535)],(485,190),(400,460)],
                        "GNCB":[[(1175,108),(1800,535)],(1390,190),(1310,460)],
                        "GNCR":[[(250,625),(890,1025)],(485,655),(400,920)],
                        "GOR":[[(1175,625),(1800,1025)],(1390,650),(1310,920)]}
    try:
        plantilla = ruta_imagenes+"p24.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            ubi_imagen = ubi_carpeta+"\\02. Tecnico\\Imagenes\\"
            lista_filiales = ["VANTI","GNCB","GNCR","GOR"]
            for filial in lista_filiales:
                if dic_metricas["indicadores"][filial] > 1:
                    esp = ajustar_coordenadas(dic_coordendas[filial][0])
                    nueva_imagen = ubi_imagen+texto_fecha+f"_indicador_tecnico_{filial}.png"
                    imagen = pegar_imagen(nueva_imagen, imagen, esp)
                else:
                    x = dic_coordendas[filial][1][0]
                    y = dic_coordendas[filial][1][1]
                    dibujo.text((x,y), "100 %", fill=dic_colores["naranja_v"], font=ImageFont.truetype(ruta_fuente_negrilla, 60))
                    y += 70
                    dibujo.text((x,y), "100 %", fill=dic_colores["morado_v"], font=ImageFont.truetype(ruta_fuente_negrilla, 60))
                    y += 70
                    dibujo.text((x,y), "100 %", fill=dic_colores["azul_agua_v"], font=ImageFont.truetype(ruta_fuente_negrilla, 60))
                    dibujo.text((dic_coordendas[filial][2][0],dic_coordendas[filial][2][1]), periodo, fill=dic_colores["azul_v"], font=ImageFont.truetype(ruta_fuente_negrilla, 38))
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_IRST(ubi, ubi_carpeta, c_slide, texto_fecha, periodo,fecha_actual):
    dic_coordendas = {"VANTI":[[(155,130),(925,535)]],
                        "GNCB":[[(1070,130),(1870,535)]],
                        "GNCR":[[(150,645),(930,1020)]],
                        "GOR":[[(1070,645),(1870,1020)]]}
    try:
        lista_plantilla = ["p25","p26","p27"]
        ubi_imagen = ubi_carpeta+"\\02. Tecnico\\Imagenes\\"
        for i in range(len(lista_plantilla)):
            plantilla = ruta_imagenes+lista_plantilla[i]+".png"
            if os.path.exists(plantilla):
                imagen = Image.open(plantilla)
                dibujo = ImageDraw.Draw(imagen)
                if i == 0:
                    dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
                    for filial, valor in dic_coordendas.items():
                        esp = ajustar_coordenadas(valor[0])
                        nueva_imagen = ubi_imagen+texto_fecha+f"_IRST_min_{filial}.png"
                        imagen = pegar_imagen(nueva_imagen, imagen, esp)
                elif i == 1:
                    dibujo.text((358,12), f"TAM - Duración eventos NC por franja horaria ({periodo})", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 42))
                    for filial, valor in dic_coordendas.items():
                        elemento = [(valor[0][0][0]-120,valor[0][0][1]),(valor[0][1][0],valor[0][1][1])]
                        esp = ajustar_coordenadas(elemento)
                        nueva_imagen = ubi_imagen+texto_fecha+f"_IRST_h_{filial}_NC.png"
                        imagen = pegar_imagen(nueva_imagen, imagen, esp)
                elif i == 2:
                    dibujo.text((300,12), f"TAM - Duración eventos Controlados por franja horaria ({periodo})", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 42))
                    for filial, valor in dic_coordendas.items():
                        elemento = [(valor[0][0][0]-120,valor[0][0][1]),(valor[0][1][0],valor[0][1][1])]
                        esp = ajustar_coordenadas(elemento)
                        nueva_imagen = ubi_imagen+texto_fecha+f"_IRST_h_{filial}_C.png"
                        imagen = pegar_imagen(nueva_imagen, imagen, esp)
                imagen.save(ubi+f"slide_{c_slide}.png")
                c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def slide_cumplimientos(ubi, fecha_actual, ubi_carpeta, c_slide):
    dic_coordendas = {"VANTI":[[(80,130),(925,535)]],
                        "GNCB":[[(1010,130),(1870,535)]],
                        "GNCR":[[(80,645),(930,1020)]],
                        "GOR":[[(1010,645),(1870,1020)]]}
    try:
        plantilla = ruta_imagenes+"p28.png"
        if os.path.exists(plantilla):
            imagen = Image.open(plantilla)
            dibujo = ImageDraw.Draw(imagen)
            dibujo.text((760,1025), f"Último corte: {fecha_actual} - {grupo_vanti}", fill=azul_vanti, font=ImageFont.truetype(ruta_fuente, 30))
            ubi_imagen = ubi_carpeta+"\\03. Tecnico\\Imagenes\\"
            for filial, valor in dic_coordendas.items():
                esp = ajustar_coordenadas(dic_coordendas[filial][0])
                ubi_imagen = ubi_carpeta+"\\03. Cumplimientos_Regulatorios\\Imagenes\\"
                nueva_imagen = ubi_imagen+f"porcentaje_cumplimientos_regulatorios_{filial}.png"
                imagen = pegar_imagen(nueva_imagen, imagen, esp)
            imagen.save(ubi+f"slide_{c_slide}.png")
            c_slide += 1
        return c_slide
    except BaseException:
        return c_slide

def crear_slides(ubi, fecha, fecha_completa, fecha_corte, texto_fecha, dic_metricas,mes_corte, fecha_anio_anterior, periodo, thread=None):
    ubi_carpeta = ubi
    ubi += "\\04. Dashboard\\Imagenes\\"
    anio = fecha[0]
    mes = fecha[1].capitalize()[:3]
    fecha = f"{fecha[1]}/{fecha[0]}"
    c_slide = 1
    c_slide = slide_portada(ubi, fecha, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide, thread=thread)
    c_slide = slide_def_1(ubi, fecha, fecha_corte, dic_metricas,mes_corte,fecha_anio_anterior, c_slide)
    c_slide = slide_usuarios(ubi, fecha, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_pie_usuarios(ubi, fecha, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_consumo(ubi, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_pie_consumo(ubi, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_sub_con(ubi, fecha_corte, ubi_carpeta, texto_fecha, c_slide)
    c_slide = slide_kpi_sub(ubi, fecha_corte, ubi_carpeta, dic_metricas, c_slide, anio)
    c_slide = slide_recla_fact(ubi, fecha_corte, ubi_carpeta, c_slide)
    c_slide = slide_compensaciones(ubi, fecha_corte, ubi_carpeta, c_slide, texto_fecha)
    c_slide = slide_AOM(ubi, int(anio)-1, "Dic", fecha_corte, ubi_carpeta, c_slide)
    c_slide = slide_desviaciones(ubi, fecha_corte, ubi_carpeta, c_slide, texto_fecha, dic_metricas)
    c_slide = slide_def_2(ubi, fecha_corte, c_slide)
    c_slide = slide_tarifas(ubi, fecha_corte, ubi_carpeta, texto_fecha, dic_metricas, c_slide)
    c_slide = slide_def_3(ubi, fecha_corte, c_slide)
    c_slide = slide_indicadores(ubi, fecha_corte, ubi_carpeta, c_slide, texto_fecha, dic_metricas, periodo)
    c_slide = slide_IRST(ubi, ubi_carpeta, c_slide, texto_fecha, periodo, fecha_corte)
    c_slide = slide_cumplimientos(ubi, fecha_corte, ubi_carpeta, c_slide)
    # mapa_suspensiones
    ubi = ubi.replace("Imagenes\\", "Imagenes")
    if thread:
        thread.message_sent.emit(f"El Dashboard para el periodo: {fecha_completa} se ha creado en la carpeta {acortar_nombre(ubi)}", "green")
    else:
        print(f"\n\nEl Dashboard para el periodo: {fecha_completa} se ha creado en la carpeta {acortar_nombre(ubi)}\n")
    os.startfile(ubi)