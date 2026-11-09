def limpiar_registro_sensor(registro_raw):
    """
    Punto A: Normalización de Lecturas.
    Toma un diccionario con datos crudos y retorna un diccionario estandarizado.
    """
    # 1. Limpiar el identificador eliminando espacios sobrantes con .strip()
    sensor_id = registro_raw.get("sensor_id", "").strip()
    
    # 2. Procesar la temperatura: quitar letras (como 'C'), espacios y convertir a float
    temp_raw = str(registro_raw.get("temperatura", "0"))
    # Reemplazamos la 'C' o 'c' y espacios vacíos, luego convertimos a float
    temp_limpia = temp_raw.replace("C", "").replace("c", "").strip()
    
    try:
        temperatura = float(temp_limpia)
    except ValueError:
        temperatura = 0.0  # Valor por defecto seguro si viene corrupto
        
    # 3. Validar la ubicación: si no existe o está vacía, asignar un valor por defecto seguro
    ubicacion = registro_raw.get("ubicacion")
    if not ubicacion or not str(ubicacion).strip():
        ubicacion = "Desconocida"
    else:
        ubicacion = str(ubicacion).strip()
        
    # Retornar el nuevo diccionario estandarizado
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Punto B: Monitoreo y Mapeo Estadístico ( generar_resumen_sensores )
    Toma una lista de registros limpios y un umbral.
    Retorna una tupla: (lista_sensores_alerta, promedio_temperatura).
    """
    if not lista_sensores_limpios:
        return [], 0.0
    
    lista_sensores_alerta = []
    suma_temperaturas = 0.0
    
    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
        suma_temperaturas += temp
        
        # Verificar si supera el umbral estipulado
        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])
            
    # Calcular el promedio térmico global
    promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    
    return lista_sensores_alerta, promedio_temperatura



# BLOQUE DE EJECUCIÓN Y PRUEBAS

if __name__ == "__main__":
    # 1. Datos crudos simulados (heterogéneos, con espacios y sufijos)
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.8 c ", "ubicacion": ""}, # Ubicación faltante
        {"sensor_id": "SENSOR-003 ", "temperatura": "19.2C", "ubicacion": "Planta Sur"},
        {"sensor_id": "SENSOR-004", "temperatura": "28.0", "ubicacion": " Laboratorio "}
    ]
    
    print("--- 1. PROCESO DE SANITIZACIÓN (Punto A) ---")
    sensores_limpios = []
    for reg in registros_crudos:
        sensor_limpio = limpiar_registro_sensor(reg)
        sensores_limpios.append(sensor_limpio)
        print(f"Original: {reg} \n-> Limpio:  {sensor_limpio}\n")
        
    # 2. Definir umbral de temperatura para las alertas
    UMBRAL = 25.0
    
    print(f"--- 2. ANÁLISIS ESTADÍSTICO (Punto B) [Umbral > {UMBRAL}°C] ---")
    sensores_alerta, promedio_global = generar_resumen_sensores(sensores_limpios, UMBRAL)
    
    # 3. Impresión formateada del reporte final
    print("\n================ REPORTE CONSOLIDADO ================")
    print(f"Promedio térmico global de la planta : {promedio_global:.2f} °C")
    print(f"Dispositivos que superan el umbral   : {len(sensores_alerta)}")
    print(f"IDs en alerta                        : {sensores_alerta}")
    print("=====================================================")