import os
import sys
import json
import ruta_principal as mod_rp
global ruta_principal, ruta_codigo, ruta_constantes, ruta_nuevo_sui, ruta_archivos
ruta_principal = mod_rp.v_ruta_principal()
ruta_constantes = mod_rp.v_constantes()
ruta_nuevo_sui = mod_rp.v_nuevo_sui()
ruta_codigo = mod_rp.v_codigo()
ruta_archivos = mod_rp.v_archivos()
sys.path.append(os.path.abspath(ruta_codigo))
import modulo as mod_1

def almacenar_json(diccionario, nombre_archivo):
        with open(nombre_archivo, 'w') as file:
                json.dump(diccionario, file, indent=4)
def leer_archivos_json(archivo):
        with open(archivo) as file:
                data = json.load(file)
        return data

def creacion_directorio_carpetas_principales():
        lista_anios_txt = ["Compilado"]
        with open(ruta_constantes+"Anios.txt", 'r') as archivo:
                        lineas = archivo.readlines()
        l1 = [str(linea.strip()) for linea in lineas][1:]
        lista_anios_txt.extend(l1)
        carpetas = {"carpeta_1":["NUEVO SUI"], # Carpeta general
                        "carpeta_2":["Reportes Nuevo SUI"], # Carpeta principal
                        "carpeta_3":lista_anios_txt, #Años registrados
                        "carpeta_4":["VANTI",
                                "GNCB",
                                "GNCR",
                                "GOR",
                                "CALIDAD"], # Empresas asociadas
                        "carpeta_5":["Compilado",
                                "Enero",
                                "Febrero",
                                "Marzo",
                                "Abril",
                                "Mayo",
                                "Junio",
                                "Julio",
                                "Agosto",
                                "Septiembre",
                                "Octubre",
                                "Noviembre",
                                "Diciembre"], # Separación por meses
                        "carpeta_6":{"Comercial":["GRTT2","GRC1","GRC2","GRC3","GRC4","GRC5","GRC6","RSGN","GRC8"],
                                "Tarifario":["GRT1","GRT2","GRT3"],
                                "Tecnico":["GRS1", "GRCS1", "GRCS2", "GRCS3", "GRCS4", "GRCS5", "GRCS6",
                                                "GRCS7", "GRCS8","GRCS9"]}} # Tipos de reporte
        almacenar_json(carpetas, ruta_constantes+"carpetas.json")
        carpetas_1 = {"carpeta_1":["NUEVO SUI"], # Carpeta general
                        "carpeta_2":["Reportes Nuevo SUI",
                                        "Seguimiento",
                                        "ANS",
                                        "Reportes CREG",
                                        "Reportes DANE",
                                        "Reportes SH",
                                        "Reportes Naturgas",
                                        "Validador y Lineamientos",
                                        "Monitoreo y Control",
                                        "Tableau",
                                        "Tablas Maestras"], # Carpeta principal
                        "carpeta_3":lista_anios_txt, #Años registrados
                        "carpeta_4":["VANTI",
                                "GNCB",
                                "GNCR",
                                "GOR",
                                "CALIDAD"]}
        almacenar_json(carpetas_1, ruta_constantes+"carpetas_1.json")
        carpetas_2 = {"carpeta_1":["NUEVO SUI"], # Carpeta general
                        "carpeta_2":["Reportes Nuevo SUI"], # Carpeta principal
                        "carpeta_3":lista_anios_txt, #Años registrados
                        "carpeta_4":["VANTI",
                                "GNCB",
                                "GNCR",
                                "GOR",
                                "CALIDAD",
                                "REPORTES_GENERADOS_APLICATIVO"], # Empresas asociadas
                        "carpeta_5":["Compilado",
                                "Enero",
                                "Febrero",
                                "Marzo",
                                "Abril",
                                "Mayo",
                                "Junio",
                                "Julio",
                                "Agosto",
                                "Septiembre",
                                "Octubre",
                                "Noviembre",
                                "Diciembre"]}
        almacenar_json(carpetas_2, ruta_constantes+"carpetas_2.json")
        carpetas_3 = {"carpeta_1":["NUEVO SUI"], # Carpeta general
                        "carpeta_2":["Reportes Nuevo SUI"], # Carpeta principal
                        "carpeta_3":lista_anios_txt, #Años registrados
                        "carpeta_4":["VANTI",
                                "GNCB",
                                "GNCR",
                                "GOR",
                                "CALIDAD"], # Filiales asociadas
                        "carpeta_5":["Compilado",
                                "Enero",
                                "Febrero",
                                "Marzo",
                                "Abril",
                                "Mayo",
                                "Junio",
                                "Julio",
                                "Agosto",
                                "Septiembre",
                                "Octubre",
                                "Noviembre",
                                "Diciembre"], # Separación por meses
                        "carpeta_7":["Comercial","Tarifario","Tecnico","Cumplimientos_Regulatorios"]} # Tipos de reporte
        almacenar_json(carpetas_3, ruta_constantes+"carpetas_3.json")

def cambiar_diccionario(anio):
        try:
                with open(ruta_constantes+"Anios.txt", 'a') as file:
                        file.write(anio + '\n')
        except IOError:
                pass

def guardar_diccionario_ruta(diccionario,nombre):
        n_archivo = ruta_constantes+nombre+".json"
        almacenar_json(diccionario, n_archivo)

def variables_reportes(reporte):
        n_archivo = reporte
        if reporte == "GRT1":
                generales_no_float = ["ID_Mercado","Metodologia","Tipo_gas","Tipo_usuario","Rango","Piso_rango","Techo_rango","Vendedor_excedente_suministro","PMS","Cglp","CTT","CP",
                        "CTTG","IVE_aplicado_gestor_transporte","IVE_aplicado_comercializador_transporte","Vendedor_Excedente_Transporte"]
                generales_float = ["Cuv","Cuf","G","T","D","FPC","Cv","Cc","Cf","P_perdidas","CCG",
                                "V","TRM","d","Qreal","CTCG","IVE_aplicado_gestor_suministro","IVE_aplicado_comercializador_suministro","T_GLP_por_duetos","TVm_GLP","A",
                        "Costo_Transporte","Tmo","Qo","TVm_GNC","Pm","QGNC","P_densidad","Fv","Qc","lm-1","lm-2","Qf","Dm","Q_rango","DAUNR","DAUR","Cons1","Cons2","CUEq1","CUEq2",
                        "Tarifa_1","Tarifa_2","S1","S2","IP_o","IPC_m-1","IPP_o","IPP_m-1","D(AUR)kmJ"]
                generales_hora = []
                generales_fecha = []
                seleccionados = ["ID_Mercado","Metodologia","Tipo_gas","Tipo_usuario","Rango","Piso_rango","Techo_rango",
                                "Cuf","Cuv","G","T","D","FPC","P_perdidas","Tarifa_1","Tarifa_2","S1","S2"]
                generales_carga = ["ID_Mercado","Metodologia","Tipo_gas","Tipo_usuario","Rango","Piso_rango","Techo_rango","Cuv","Cuf","G","T","D","FPC","Cv","Cc","Cf","P_perdidas","CCG",
                        "V","TRM","d","Qreal","CTCG","IVE_aplicado_gestor_suministro","IVE_aplicado_comercializador_suministro","Vendedor_excedente_suministro","PMS","Cglp","CTT","CP",
                        "CTTG","IVE_aplicado_gestor_transporte","IVE_aplicado_comercializador_transporte","Vendedor_Excedente_Transporte","T_GLP_por_duetos","TVm_GLP","A",
                        "Costo_Transporte","Tmo","Qo","TVm_GNC","Pm","QGNC","P_densidad","Fv","Qc","lm-1","lm-2","Qf","Dm","Q_rango","DAUNR","DAUR","Cons1","Cons2","CUEq1","CUEq2",
                        "Tarifa_1","Tarifa_2","S1","S2","IP_o","IPC_m-1","IPP_o","IPP_m-1","D(AUR)kmJ"]
                generales_presentacion = ["ID Mercado","Metodología","Tipo de gas","Tipo de usuario","Rango","Piso rango (m3)","Techo rango (m3)","Cuv ($/m3)","Cuf ($/factura)","G ($/m3)",
                                "T o Tm ponderado (cuando aplique) $/m3","D ($/m3)","fPC","Cv ($/m3)","Cc ($/m3)","Cf ($/factura)","P de perdidas (expresar en decimales)","CCG (USD)",
                                "V (m3)","TRM","d","Qreal (MBTU)","CTCG (USD)","IVE aplicado al gestor en suministro (USD)","IVE aplicado al comercializador en suministro (USD)",
                                "Vendedor de excedente de suministro","PMS","Cglp","CTT (USD)","CP (USD)","CTTG (USD)","IVE aplicado al gestor en transporte (USD)",
                                "IVE aplicado al comercializador en transporte (USD)","Vendedor de Excedente de Transporte","T de GLP por duetos","TVm de GLP","A ($/m3)",
                                "Costo Transporte ($/m3)","Tmo ($/m3)","Qo (m3)","TVm de GNC ($/m3)","Pm ($/m3)","QGNC (m3)","P de densidad","Fv","Qc","lm-1","lm-2","Qf",
                                "Dm ($/m3)","Q por rango (m3)","DAUNR ($/m3)","DAUR ($/m3)","Cons1 (m3)","Cons2 (m3)","CUEq1 ($/m3)","CUEq2 ($/m3)","Tarifa 1 ($/m3)",
                                "Tarifa 2 ($/m3)","%S1","%S2","IPC o","IPC m-1","IPP o","IPP m-1","D(AUR)kmJ"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRT3":
                generales_carga = ["ID_Mercado","K","PV","SA","VR","CUvR","CUvA","CUvAm-1","r","rEA","Meses"]
                generales_presentacion = ["ID Mercado","K","PV","SA","VR","CUvR","CUvA","CUvAm-1","r","rEA","Meses"]
                generales_float = ["PV","r","rEA"]
                generales_no_float = ["ID_Mercado","K","SA","VR","CUvR","CUvA","CUvAm-1","Meses"]
                generales_hora = []
                generales_fecha = []
                seleccionados = ["PV","r","rEA","ID_Mercado","K","SA","VR","CUvR","CUvA","CUvAm-1","Meses"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRC1":
                generales_no_float = ['NIU', 'Tipo_gas', 'ID_factura', 'Tipo_factura', 'Predios_condiciones_especiales', 'Tipo_lectura',
                        'Lectura_actual', 'Numero_dias_facturados','Consumo','Tipo_revision_instalacion_interna', 'Descripcion_otros']
                generales_float = ['Factor_poder_calorfico_fpc',
                                'Lectura_anterior', 'Factor_correccion_utilizado','Cuv_cargo_aplicado_consumo', 'Facturacion_consumo', 'Facturacion_cargo_fijo', 'Valor_mora_acumulado', 'Intereses_mora_acumulado',
                                'Valor_subsidio_contribucion', 'Porcentaje_subsidio_contribucion_aplicado', 'Valor_cuota_conexion', 'Intereses_financiacion_conexion', 'Suspension_reconexion',
                                'Corte_reinstalacion','Valor_otros_conceptos', 'Valor_intereses_otros_conceptos',
                                'Refacturacion_consumos', 'Valor_refacturacion', 'Valor_refacturacion_subsidio_contribucion','Valor_total_facturado']
                generales_hora = []
                generales_fecha = ['Fecha_expedicion_factura', 'Fecha_inicio_periodo_facturacion',
                                'Fecha_terminacion_periodo_facturacion','Fecha_lectura_anterior', 'Fecha_lectura_actual', 'Fecha_limite_pago', 'Fecha_suspension', 'Fecha_revision']
                seleccionados = ['NIU', 'ID_factura', 'Tipo_factura', 'Fecha_expedicion_factura', 'Fecha_inicio_periodo_facturacion',
                                'Fecha_terminacion_periodo_facturacion', 'Tipo_lectura', 'Factor_poder_calorfico_fpc',
                                'Lectura_anterior', 'Fecha_lectura_anterior', 'Lectura_actual', 'Fecha_lectura_actual', 'Numero_dias_facturados', 'Factor_correccion_utilizado',
                                'Consumo', 'Cuv_cargo_aplicado_consumo', 'Facturacion_consumo', 'Facturacion_cargo_fijo',
                                'Valor_subsidio_contribucion', 'Porcentaje_subsidio_contribucion_aplicado', 'Valor_cuota_conexion', 'Suspension_reconexion',
                                'Corte_reinstalacion', 'Tipo_revision_instalacion_interna', 'Fecha_revision', 'Valor_otros_conceptos', 'Descripcion_otros',
                                'Refacturacion_consumos', 'Valor_refacturacion', 'Valor_refacturacion_subsidio_contribucion','Valor_total_facturado']
                generales_carga = ['NIU', 'Tipo_gas', 'ID_factura', 'Tipo_factura', 'Fecha_expedicion_factura', 'Fecha_inicio_periodo_facturacion',
                        'Fecha_terminacion_periodo_facturacion', 'Predios_condiciones_especiales', 'Tipo_lectura', 'Factor_poder_calorfico_fpc',
                        'Lectura_anterior', 'Fecha_lectura_anterior', 'Lectura_actual', 'Fecha_lectura_actual', 'Numero_dias_facturados', 'Factor_correccion_utilizado',
                        'Consumo', 'Cuv_cargo_aplicado_consumo', 'Facturacion_consumo', 'Facturacion_cargo_fijo', 'Valor_mora_acumulado', 'Intereses_mora_acumulado',
                        'Valor_subsidio_contribucion', 'Porcentaje_subsidio_contribucion_aplicado', 'Valor_cuota_conexion', 'Intereses_financiacion_conexion', 'Suspension_reconexion',
                        'Corte_reinstalacion', 'Tipo_revision_instalacion_interna', 'Fecha_revision', 'Valor_otros_conceptos', 'Valor_intereses_otros_conceptos', 'Descripcion_otros',
                        'Refacturacion_consumos', 'Valor_refacturacion', 'Valor_refacturacion_subsidio_contribucion', 'Fecha_limite_pago', 'Fecha_suspension', 'Valor_total_facturado']
                generales_presentacion = ['NIU', 'Tipo de gas', 'ID factura', 'Tipo de factura', 'Fecha de expedición de la factura', 'Fecha de inicio periodo de facturación',
                                'Fecha de terminación del periodo de facturación', 'Predios en condiciones especiales', 'Tipo de lectura', 'Factor de poder calorífico  FPC',
                                'Lectura anterior', 'Fecha de lectura anterior', 'Lectura actual', 'Fecha de lectura actual', 'Número de días facturados', 'Factor de corrección utilizado',
                                'Consumo', 'Cuv cargo aplicado por consumo', 'Facturación por consumo', 'Facturación por cargo fijo', 'Valor por mora acumulado', 'Intereses por mora acumulado',
                                'Valor del subsidio o contribución', 'Porcentaje de subsidio o contribución aplicado', 'Valor cuota de conexión', 'Intereses financiación conexión', 'Suspensión y reconexión',
                                'Corte y reinstalación', 'Tipo revisión instalación interna', 'Fecha de la revisión', 'Valor otros conceptos', 'Valor intereses de otros conceptos', 'Descripción otros',
                                'Refacturación de consumos', 'Valor refacturación', 'Valor refacturación subsidio o contribución', 'Fecha límite pago', 'Fecha de suspensión', 'Valor total facturado']
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRC2":
                generales_carga = ["ID_Factura","Concepto_general_factura","NIT","Actividad_comprador","Tipo_gas",
                                        "Conexion_red","Fecha_expedicion_factura","Fecha_inicio_periodo_facturacion","Dias_facturados",
                                        "Sector_consumo","Tipo_contrato","Mercado","Procedencia_gas","Suministro","Precio_facturacion_suministro",
                                        "Poder_calorifico_bruto","Facturacion_por_suministro","Facturacion_por_remuneracion_gestor_mercado",
                                        "Punto_entrega_energia_comprador","Codigo_DANE_punto_entrega_energia_comprado",
                                        "Transporte","Componente_fijo_pareja_cargos","Facturacion_por_demanda_volumen","Facturacion_por_demanda_capacidad",
                                        "Tarifa","Cuota_fomento","Servicio Transporte","Codigo punto entrada","Codigo punto salida","Codigo_tramo_entrada",
                                        "Codigo_tramo_salida","Codigo_DANE_punto_entrada","Codigo_DANE_punto_salida","NIU","Cargo_distribucion",
                                        "Cargo_comercializacion","Volumen","Numero_operacion_suministro_Segas_utilizado",
                                        "Numero_operacion_transporte_Segas_utilizado","Codigo_DANE","Ubicacion","Informacion_predial_utilizada","Cedula_catastral",
                                        "Direccion","Altitud","Longitud","Latitud","Numero_operacion_Segas","Cantidad_refacturacion","Valor_refacturacion",
                                        "Valor_contribucion","Otros","Valor_total_facturado","TRM"]
                generales_presentacion = ["ID Factura","Concepto general de la factura","NIT","Actividad del comprador","Tipo de gas",
                                        "Conexión red","Fecha de expedición de la factura","Fecha de inicio periodo de facturación","Días facturados",
                                        "Sector de consumo","Tipo de contrato","Mercado","Procedencia del gas","Suministro","Precio de facturación de suministro",
                                        "Poder calorífico bruto","Facturación por suministro","Facturación por remuneración al gestor del mercado",
                                        "Punto entrega de la energía al comprador","Código DANE punto de entrega de la energía al comprado",
                                        "Transporte","Componente fijo de la pareja de cargos","Facturación por demanda de volumen","Facturación por demanda de capacidad",
                                        "Tarifa ($/kpc)","Cuota de fomento","Servicio Transporte","Código punto entrada","Código punto salida","Código tramo entrada",
                                        "Código tramo salida","Código DANE punto entrada","Código DANE punto salida","NIU","Cargo de distribución",
                                        "Cargo de comercializacion","Volumen","Número de operación de suministro segas utilizado",
                                        "Número de operación de transporte Segas utilizado","Código DANE","Ubicación","Información predial utilizada","Cédula catastral",
                                        "Dirección","Altitud","Longitud","Latitud","Número de operación en Segas","Cantidad refacturación","Valor refacturación",
                                        "Valor de la Contribución","Otros","Valor total facturado","TRM"]
                generales_no_float = ["ID_Factura","Concepto_general_factura","NIT","Actividad_comprador","Tipo_gas",
                                        "Conexion_red","Dias_facturados",
                                        "Sector_consumo","Tipo_contrato","Mercado","Procedencia_gas","Suministro"
                                        ,"Facturacion_por_suministro","Facturacion_por_remuneracion_gestor_mercado",
                                        "Punto_entrega_energia_comprador","Codigo_DANE_punto_entrega_energia_comprado",
                                        "Transporte","Componente_fijo_pareja_cargos","Facturacion_por_demanda_volumen","Facturacion_por_demanda_capacidad",
                                        "Cuota_fomento","Servicio Transporte","Codigo punto entrada","Codigo punto salida","Codigo_tramo_entrada",
                                        "Codigo_tramo_salida","Codigo_DANE_punto_entrada","Codigo_DANE_punto_salida","NIU","Volumen","Numero_operacion_suministro_Segas_utilizado",
                                        "Numero_operacion_transporte_Segas_utilizado","Codigo_DANE","Ubicacion","Informacion_predial_utilizada","Cedula_catastral",
                                        "Direccion","Altitud","Numero_operacion_Segas","Cantidad_refacturacion","Valor_refacturacion",
                                        "Valor_contribucion","Otros","Valor_total_facturado"]
                generales_float = ["Precio_facturacion_suministro","Poder_calorifico_bruto","Tarifa","Cargo_distribucion",
                                        "Cargo_comercializacion","Longitud","Latitud","TRM"]
                generales_hora = []
                generales_fecha = ["Fecha_expedicion_factura","Fecha_inicio_periodo_facturacion"]
                seleccionados = ["ID_Factura","Concepto_general_factura","NIT","Actividad_comprador",
                                        "Conexion_red","Fecha_expedicion_factura","Fecha_inicio_periodo_facturacion",
                                        "Sector_consumo","Tipo_contrato","Mercado","Procedencia_gas","Suministro","Precio_facturacion_suministro",
                                        "Poder_calorifico_bruto","Facturacion_por_suministro","Facturacion_por_remuneracion_gestor_mercado",
                                        "Punto_entrega_energia_comprador","Codigo_DANE_punto_entrega_energia_comprado",
                                        "Transporte","Componente_fijo_pareja_cargos","Facturacion_por_demanda_volumen","Facturacion_por_demanda_capacidad",
                                        "Tarifa","Cuota_fomento","Servicio Transporte","NIU","Cargo_distribucion",
                                        "Cargo_comercializacion","Volumen","Numero_operacion_suministro_Segas_utilizado",
                                        "Numero_operacion_transporte_Segas_utilizado","Codigo_DANE","Ubicacion",
                                        "Altitud","Longitud","Latitud","Numero_operacion_Segas","Cantidad_refacturacion","Valor_refacturacion",
                                        "Valor_contribucion","Otros","Valor_total_facturado","TRM"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRC3":
                generales_carga = ["NIU","Tipo_gas","Tipo_sector_consumo","ID_Factura","Periodo_compensado",
                                        "Anio","DES","CI","Demanda_promedio","Valor_compensado","Codigo_causal"]
                generales_presentacion = ["NIU","Tipo de gas","Tipo sector de consumo","ID Factura","Periodo compensado",
                                        "Año","DES","CI","Demanda promedio","Valor compensado","Código causal"]
                seleccionados = ["NIU","Tipo_sector_consumo","ID_Factura","Periodo_compensado",
                                        "Anio","CI","Valor_compensado","Codigo_causal","Demanda_promedio"]
                generales_no_float = ["NIU","Tipo_gas","Tipo_sector_consumo","ID_Factura","Periodo_compensado",
                                        "Anio","CI","Valor_compensado","Codigo_causal"]
                generales_float = ["Demanda_promedio"]
                generales_hora = ["DES"]
                generales_fecha = []
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRCS1":
                generales_carga = ["Radicado_recibido","Tipo_gas","NIU","Tipo_evento","Tipo_solicitud","Fecha_solicitud","Hora_solicitud","Fecha_llegada_servicio_tecnico","Hora_llegada_servicio_tecnico",
                                "Observaciones"]
                generales_presentacion = ["Radicado recibido","Tipo de gas","NIU","Tipo evento","Tipo solicitud","Fecha solicitud","Hora solicitud","Fecha de llegada del servicio técnico","Hora de llegada del servicio técnico",
                                        "Observaciones"]
                generales_no_float = ["Radicado recibido","Tipo_gas","NIU","Tipo_evento","Tipo_solicitud",
                                "Observaciones"]
                generales_float = []
                generales_hora = ["Hora_solicitud","Hora_llegada_servicio_tecnico"]
                generales_fecha = ["Fecha_solicitud", "Fecha_llegada_servicio_tecnico"]
                seleccionados = ["Radicado_recibido","Tipo_gas","NIU","Tipo_evento","Tipo_solicitud","Fecha_solicitud","Hora_solicitud","Fecha_llegada_servicio_tecnico","Hora_llegada_servicio_tecnico",
                                "Observaciones"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRCS2":
                generales_carga = ["Tipo_gas","IPLI","IO","IRST_EG","IRST_IN","IRST_CL",
                                "IRST_IS",
                                "IRST_0","DES_IS",
                                "Suscriptores_DES_IS","Cantidad_eventos_DES_IS",
                                "DES_ER",
                                "Suscriptores_DES_ER",
                                "Cantidad_eventos_DES_ER","DES_NER",
                                "Suscriptores_DES_NER",
                                "Cantidad_eventos_DES_NER"]
                generales_presentacion = ["Tipo de gas","IPLI (índice de Presión en Líneas Individuales)","IO (índice de Odorización)","IRST - EG (índice de Respuesta a Servicio Técnico - Escape de Gas)",
                                        "IRST - IN (índice de Respuesta a Servicio - Técnico - Incendio)","IRST -CL (índice de Respuesta a Servicio Técnico - Calidad de la Llama)",
                                        "IRST - IS (índice de Respuesta a Servicio Técnico - interrupción del Servicio)",
                                        "IRST -0 (índice de Respuesta a Servicio Técnico - Otros)","DES - IS (Duración Equivalente de interrupción en Interés del Servicio)",
                                        "Suscriptores DES - IS (Suscriptores con interrupciones en Interés del Servicio)","Cantidad de eventos DES - IS",
                                        "DES - ER (Duración Equivalente de Interrupción del Servicio por eventos Eximentes de Responsabilidad)",
                                        "Suscriptores DES - ER (Suscriptores con interrupción del servicio por eventos Eximentes de Responsabilidad)",
                                        "Cantidad de eventos DES - ER","DES - NER (Duración Equivalente de Interrupción del Servicio por eventos No Eximentes de Responsabilidad)",
                                        "Suscriptores DES - NER (Suscriptores con interrupción del servicio por eventos No Eximentes de Responsabilidad)",
                                        "Cantidad de eventos DES - NER"]
                generales_no_float = ["Tipo_gas",
                                "Suscriptores_DES_IS","Cantidad_eventos_DES_IS",
                                "Suscriptores_DES_ER",
                                "Cantidad_eventos_DES_ER",
                                "Suscriptores_DES_NER",
                                "Cantidad_eventos_DES_NER"]
                generales_float = ["IPLI","IO","IRST_EG","IRST_IN","IRST_CL",
                                "IRST_IS",
                                "IRST_0"]
                generales_hora = ["DES_IS","DES_ER","DES_NER"]
                generales_fecha = []
                seleccionados = ["IPLI","IO","IRST_EG","Tipo_gas","DES_ER","Suscriptores_DES_ER","Cantidad_eventos_DES_ER","DES_NER",
                                "Suscriptores_DES_NER","Cantidad_eventos_DES_NER"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRCS3":
                generales_carga = ["NIU","Fecha_medicion","Hora_medicion","Tipo_gas","Presion_medida","Metodo","Sustancia_odorante",
                                "Nivel_concentracion_minimo","Nivel_concentracion_medido","Observaciones"]
                generales_presentacion = ["NIU","Fecha de medición","Hora de medición","Tipo de Gas","Presion Medida (mbar)","Método","Sustancia Odorante",
                                        "Nivel de Concentración Mínimo","Nivel de Concentración Medido ( mg/m³ )","Observaciones"]
                seleccionados = ["NIU","Fecha_medicion","Hora_medicion","Tipo_gas","Metodo","Sustancia_odorante",
                                "Observaciones"]
                generales_no_float = ["NIU","Tipo_gas","Metodo","Sustancia_odorante","Observaciones"]
                generales_float = ["Presion_medida","Nivel_concentracion_minimo","Nivel_concentracion_medido"]
                generales_hora = ["Hora_medicion"]
                generales_fecha = ["Fecha_medicion"]
                seleccionados = ["NIU","Fecha_medicion","Hora_medicion","Tipo_gas","Metodo","Sustancia_odorante",
                                "Observaciones","Presion_medida","Nivel_concentracion_minimo","Nivel_concentracion_medido"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRS1":
                generales_carga = ["ID_Mercado","Codigo_DANE","Suspension_programada","Codigo_evento","Tipo_gas","Fecha_inicio_suspension",
                                        "Hora_inicio_suspension","Fecha_final_suspension","Hora_final_suspension","Tipo_suspension","Origen_suspension",
                                        "Genero_compensacion","Numero_suscriptores_afectados","Medio_comunicacion","Fecha_publicacion","Observaciones"]
                generales_presentacion = ["ID Mercado","Código DANE","¿Suspensión fue programada?","Código de evento","Tipo de Gas","Fecha de inicio de la suspensión",
                                        "Hora de inicio de la suspensión","Fecha final de la suspensión","Hora final de la suspensión","Tipo de suspensión","Origen de la suspensión",
                                        "Generó compensación","Numero de Suscriptores afectados","Medio de comunicación","Fecha de publicacion","Observaciones"]
                generales_no_float = ["ID_Mercado","Codigo_DANE","Suspension_programada","Codigo_evento","Tipo_gas",
                                        "Tipo_suspension","Origen_suspension",
                                        "Genero_compensacion","Numero_suscriptores_afectados","Medio_comunicacion","Observaciones"]
                generales_float = []
                generales_hora = ["Hora_inicio_suspension","Hora_final_suspension"]
                generales_fecha = ["Fecha_inicio_suspension","Fecha_final_suspension","Fecha_publicacion"]
                seleccionados = ["ID_Mercado","Codigo_DANE","Suspension_programada","Codigo_evento","Tipo_gas","Fecha_inicio_suspension",
                                "Hora_inicio_suspension","Fecha_final_suspension","Hora_final_suspension","Tipo_suspension","Origen_suspension",
                                "Genero_compensacion","Numero_suscriptores_afectados","Fecha_publicacion"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRCS7":
                generales_no_float = ["NIU","Grupo","Numero_medidor","Tipo_revision","Numero_certificado","Empresa_certificacion","Codigo_acreditacion_ONAC"]
                generales_float = []
                generales_hora = []
                generales_fecha = ["Fecha_revision"]
                seleccionados = ["NIU","Grupo","Numero_medidor","Tipo_revision","Numero_certificado","Empresa_certificacion"]
                generales_carga = ["NIU","Grupo","Numero_medidor","Tipo_revision","Fecha_revision","Numero_certificado","Empresa_certificacion","Codigo_acreditacion_ONAC"]
                generales_presentacion = ["NIU","Grupo","Número de medidor","Tipo de revisión","Fecha de revisión","Número de certificado","Empresa de certificación","Código de acreditación ONAC"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRCS9":
                generales_no_float = ["NIU","Caso","Numero_medidor","Numero_certificado","Empresa_certificacion","Codigo_acreditacion_ONAC","Observaciones"]
                generales_float = []
                generales_hora = []
                generales_fecha = ["Fecha_revision"]
                seleccionados = ["NIU","Caso","Numero_medidor","Fecha_revision","Numero_certificado","Empresa_certificacion"]
                generales_carga = ["NIU","Caso","Numero_medidor","Fecha_revision","Numero_certificado","Empresa_certificacion","Codigo_acreditacion_ONAC","Observaciones"]
                generales_presentacion = ["NIU","Caso","Número de medidor","Fecha de revisión","Número de certificado","Empresa de certificación","Código de acreditación ONAC","Observaciones"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "GRTT2":
                generales_carga = ["NIU","Tipo_usuario","ID_Comercializador","ID_Mercado","Codigo_DANE","Ubicacion","Direccion","Informacion_predial_actualizada",
                                "Cedula_Catastral","Estrato","Altitud","Longitud","Latitud","Estado","Fecha_ajuste"]
                generales_presentacion = ["NIU","Tipo usuario","ID Comercializador","ID Mercado","Código DANE","Ubicación","Dirección","Información Predial Actualizada",
                                        "Cédula Catastral","Estrato","Altitud","Longitud","Latitud","Estado","Fecha ajuste"]
                generales_no_float = ["NIU","Tipo_usuario","ID_Comercializador","ID_Mercado","Codigo_DANE","Ubicacion","Direccion","Informacion_predial_actualizada",
                                        "Cedula_Catastral","Estrato","Altitud","Estado"]
                generales_float = ["Longitud","Latitud"]
                generales_hora = []
                generales_fecha = ["Fecha ajuste"]
                seleccionados = ["Longitud","Latitud","NIU","Tipo_usuario","ID_Comercializador","ID_Mercado","Codigo_DANE",
                                "Estrato","Altitud","Estado","Direccion","Cedula_Catastral"]
                total = len(generales_float)+len(generales_no_float)+len(generales_hora)+len(generales_fecha)
                datos = {"generales":dict(zip(generales_carga, generales_presentacion)),
                        "generales_no_float":generales_no_float,
                        "generales_float":generales_float,
                        "generales_hora":generales_hora,
                        "generales_fecha":generales_fecha,
                        "seleccionados": seleccionados,
                        "cantidad_columnas":total}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "reportes_disponibles":
                desc = reporte
                data = {"Tarifario":["GRT1",
                                "GRT3"],
                        "Comercial":[
                                "GRC1",
                                "GRC2",
                                "GRC3",
                                "GRTT2"],
                        "Tecnico":["GRCS1",
                                "GRCS2",
                                "GRCS3",
                                "GRCS7",
                                "GRCS9",
                                "GRS1"]}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tablas_disponibles":
                desc = reporte
                data = ["tabla_1",
                "tabla_2",
                "tabla_5",
                "tabla_29",
                "tabla_31",
                "tabla_30",
                "tabla_32",
                "tabla_35",
                "tabla_71",
                "tabla_15",
                "tabla_3",
                "tabla_72",
                "tabla_8",
                "tabla_11",
                "tabla_13",
                "tabla_17",
                "tabla_18"]
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_nit":
                desc = "NIT"
                data = {"VANTI S.A. ESP.":"800007813-5",
                        "GAS NATURAL DEL CESAR S.A. ESP.":"804000551-3",
                        "GAS NATURAL CUNDIBOYACENCE S.A. ESP.":"830045472-8",
                        "GAS NATURAL DE ORIENTE S.A. ESP.":"890205952-7"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_empresa":
                desc = "Empresas"
                data = {"VANTI":"VANTI S.A. ESP.",
                        "GNCB":"GAS NATURAL CUNDIBOYACENCE S.A. ESP.",
                        "GNCR":"GAS NATURAL DEL CESAR S.A. ESP.",
                        "GOR":"GAS NATURAL DE ORIENTE S.A. ESP."}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_1":
                desc = "Tipo de Gas"
                data = {"1":"Gas Natural GN",
                        "2":"Gas Natural Comprimido GNC",
                        "3":"Gas Licuado de Petróleo GLP",
                        "4":"Aire Propanado AP",
                        "5":"Gas Metano en Depósitos de Carbón GMDC"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_2":
                desc = "Tipo de Factura"
                data = {"1":"Normal",
                        "2":"Refacturación",
                        "3":"Normal y refacturación"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_5":
                desc = "Tipo de Lectura"
                data = {"1":"Real",
                        "2":"Estimada",
                        "3":"Medición prepaga",
                        "4":"Sin Lectura"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_29":
                desc = "Tipo de usuario estructura tarifaria"
                data = {"1":"Residencial",
                        "2":"Comercial",
                        "3":"Industrial",
                        "4":"Gas Natural Vehicular",
                        "5":"Cogeneración",
                        "6":"Autogeneración",
                        "7":"Otro"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_31":
                desc = "Grupo de suscriptores"
                data = {"1":"Usuarios residenciales pertenecientes a los estratos 1 y 2",
                        "2":"Usuarios regulados diferentes a los residenciales de los Estratos 1 y 2",
                        "3":"Totalidad de usuarios regulados"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_30":
                desc = "Si / No"
                data = {"1":"Si",
                        "2":"No"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_32":
                desc = "Tipo de suspensión"
                data = {"1":"IS",
                        "2":"ER",
                        "3":"NER"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_35":
                desc = "Tipo de evento servicio técnico"
                data = {"1":"Escape de gas",
                        "2":"Incendio",
                        "3":"Calidad de la llama",
                        "4":"Interrupción del servicio",
                        "5":"Otros"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_71":
                desc = "Clasificación usuario"
                data = {"1":"Regulado",
                        "2":"No Regulado"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_15":
                desc = "Ubicación"
                data = {"1":"Rural Disperso",
                        "2":"Urbano",
                        "3":"Centro Poblado"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_3":
                desc = "Sector de Consumo usuarios regulados"
                data = {"1":"Residencial Bajo - Bajo",
                        "2":"Residencial Bajo",
                        "3":"Residencial Medio - Bajo",
                        "4":"Residencial Medio",
                        "5":"Residencial Medio - Alto",
                        "6":"Residencial Alto",
                        "7":"Comercial",
                        "8":"Industrial",
                        "9":"Oficial",
                        "10":"Especial Asistencial - EA",
                        "11":"Especial Educativo - ED",
                        "12":"Usuario Exento - UE",
                        "13":"Industrial Exento - IE",
                        "14":"Zonas comunes",
                        "15":"Distrito de riego",
                        "16":"Provisional"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_72":
                desc = "Estado suscriptor"
                data = {"1":"Activo",
                        "2":"Inactivo"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_8":
                desc = "Actividad del comprador"
                data = {"1":"Comercializador",
                        "2":"Distribuidor - Comercializador",
                        "3":"Productor - Comercializador",
                        "4":"Transportador",
                        "5":"Usuario No Regulado",
                        "6":"Generador térmico",}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_11":
                desc = "Sector de consumo usuarios no regulados"
                data = {"1":"Comercial",
                        "2":"Comercializadoras de gas natural",
                        "3":"Transportadores de gas natural",
                        "4":"GNCV",
                        "5":"Petroquímica",
                        "6":"Industrial",
                        "7":"Oficiales",
                        "8":"Termoeléctrico",
                        "9":"Refinería"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_13":
                desc = "Mercado"
                data = {"1":"Primario",
                        "2":"Secundario",
                        "3":"Comercialización minorista"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_17":
                desc = "Tipo sector consumo",
                data = {"1":"Residencial",
                        "2":"No Residencial"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "tabla_18":
                desc = "Mes"
                data = {"1":"Enero",
                        "2":"Febrero",
                        "3":"Marzo",
                        "4":"Abril",
                        "5":"Mayo",
                        "6":"Junio",
                        "7":"Julio",
                        "8":"Agosto",
                        "9":"Septiembre",
                        "10":"Octubre",
                        "11":"Noviembre",
                        "12":"Diciembre"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "meses_abre":
                desc = "Mes"
                data = {"ENE":"Enero",
                        "FEB":"Febrero",
                        "MAR":"Marzo",
                        "ABR":"Abril",
                        "MAY":"Mayo",
                        "JUN":"Junio",
                        "JUL":"Julio",
                        "AGO":"Agosto",
                        "SEP":"Septiembre",
                        "OCT":"Octubre",
                        "NOV":"Noviembre",
                        "DIC":"Diciembre"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "anios":
                with open(ruta_constantes+"Anios.txt", 'r') as archivo:
                        lineas = archivo.readlines()
                lista_anios_txt = [linea.strip() for linea in lineas]
                desc = "Anios"
                data = {}
                for i in range(1,len(lista_anios_txt)):
                        data[str(i)] = lista_anios_txt[i]
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "trimestres":
                desc = "Trimestres"
                data = {"1":"TRIM_1",
                        "2":"TRIM_2",
                        "3":"TRIM_3",
                        "4":"TRIM_4"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "sectores_consumo":
                desc = "Sectores_consumo_clasificados"
                data = {"Regulados":{"Residencial Bajo - Bajo":"Residencial",
                                        "Residencial Bajo":"Residencial",
                                        "Residencial Medio - Bajo":"Residencial",
                                        "Residencial Medio":"Residencial",
                                        "Residencial Medio - Alto":"Residencial",
                                        "Residencial Alto":"Residencial",
                                        "Comercial":"Comercial",
                                        "Industrial":"Industrial",
                                        "Oficial":"Comercial",
                                        "Especial Asistencial - EA":"Comercial",
                                        "Especial Educativo - ED":"Comercial",
                                        "Usuario Exento - UE":"Residencial",
                                        "Industrial Exento - IE":"Industrial",
                                        "Zonas comunes":"Comercial",
                                        "Provisional":"Residencial"},
                        "No Regulados":{"Comercial":"Comercial",
                                        "Comercializadoras de gas natural":"Comercializadoras de gas natural",
                                        "Transportadores de gas natural":"Transportadores de gas natural",
                                        "GNCV":"GNCV",
                                        "Petroquímica":"Petroquímica",
                                        "Industrial":"Industrial",
                                        "Oficiales":"Oficiales",
                                        "Termoeléctrico":"Termoeléctrico",
                                        "Refinería":"Refinería"}}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "trimestre_mes":
                desc = "Trimestre_mes"
                data = {"Enero":"TRIM_3",
                        "Febrero":"TRIM_4",
                        "Marzo":"TRIM_4",
                        "Abril":"TRIM_4",
                        "Mayo":"TRIM_1",
                        "Junio":"TRIM_1",
                        "Julio":"TRIM_1",
                        "Agosto":"TRIM_2",
                        "Septiembre":"TRIM_2",
                        "Octubre":"TRIM_2",
                        "Noviembre":"TRIM_3",
                        "Diciembre":"TRIM_3"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "sector_consumo_estrato":
                desc = "Sector_consumo_a_estrato"
                data = {"Residencial Bajo - Bajo":"Estrato 1",
                        "Residencial Bajo":"Estrato 2",
                        "Residencial Medio - Bajo":"Estrato 3",
                        "Residencial Medio":"Estrato 4",
                        "Residencial Medio - Alto":"Estrato 5",
                        "Residencial Alto":"Estrato 6"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)
        elif reporte == "categoria_matriz_requerimientos":
                desc = "Categorias_matriz_requerimientos"
                data = {"AEGR":"Otros",
                        "ALCALDIAS":"Entidades gubernamentales",
                        "CONSEJO DE BOGOTÁ":"Entidades gubernamentales",
                        "CREG":"CREG",
                        "DANE":"Entidades gubernamentales",
                        "MME":"Entidades gubernamentales",
                        "MUNICIPIOS":"Entidades gubernamentales",
                        "OTROS":"Otros",
                        "SECRETARIA DEL HABITAD":"Entidades gubernamentales",
                        "SSPD":"SSPD",
                        "UPME":"Entidades gubernamentales",
                        "VANTI ESP SA":"Otros"}
                datos = {"descripcion":desc,
                        "datos":data}
                guardar_diccionario_ruta(datos, n_archivo)

def crear_archivos_json_principales():
        variables_reportes("GRT1")
        variables_reportes("GRT3")
        variables_reportes("GRC1")
        variables_reportes("GRC2")
        variables_reportes("GRC3")
        variables_reportes("GRCS1")
        variables_reportes("GRCS2")
        variables_reportes("GRCS3")
        variables_reportes("GRCS7")
        variables_reportes("GRCS9")
        variables_reportes("GRS1")
        variables_reportes("GRTT2")
        variables_reportes("tabla_nit")
        variables_reportes("tabla_empresa")
        variables_reportes("reportes_disponibles")
        variables_reportes("tablas_disponibles")
        variables_reportes("tabla_1")
        variables_reportes("tabla_2")
        variables_reportes("tabla_5")
        variables_reportes("tabla_29")
        variables_reportes("tabla_31")
        variables_reportes("tabla_30")
        variables_reportes("tabla_32")
        variables_reportes("tabla_35")
        variables_reportes("tabla_71")
        variables_reportes("tabla_15")
        variables_reportes("tabla_3")
        variables_reportes("tabla_72")
        variables_reportes("tabla_8")
        variables_reportes("tabla_11")
        variables_reportes("tabla_13")
        variables_reportes("tabla_17")
        variables_reportes("tabla_18")
        variables_reportes("anios")
        variables_reportes("trimestres")
        variables_reportes("meses_abre")
        variables_reportes("sectores_consumo")
        variables_reportes("trimestre_mes")
        variables_reportes("sector_consumo_estrato")
        variables_reportes("categoria_matriz_requerimientos")
        creacion_directorio_carpetas_principales()
