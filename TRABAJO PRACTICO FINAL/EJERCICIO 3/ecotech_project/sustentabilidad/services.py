def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    """Algoritmo de cálculo de huella de carbono industrial."""
    if consumo_kwh < 0:
        raise ValueError("El consumo en kWh no puede ser negativo.")
    return consumo_kwh * factor_emision


def obtener_metricas_consumo(registros):
    """Procesa un historial de consumos por planta industrial."""
    if not registros:
        return {"total_emisiones": 0.0, "planta_mayor_consumo": "Ninguna"}

    total_global_emisiones = 0.0
    mayor_consumo = -1
    planta_mayor = ""

    for reg in registros:
        planta = reg.get("planta", "Desconocida")
        consumo = reg.get("consumo", 0.0)
        
        emision = calcular_emisiones_carbono(consumo)
        total_global_emisiones += emision

        if consumo > mayor_consumo:
            mayor_consumo = consumo
            planta_mayor = planta

    return {
        "total_emisiones": total_global_emisiones,
        "planta_mayor_consumo": planta_mayor
    }