from django.shortcuts import render
from sustentabilidad.services import obtener_metricas_consumo

def vista_panel_sustentabilidad(request):
    """Punto B: Vista de Django que procesa métricas y renderiza la plantilla."""
    historial_consumos = [
        {"planta": "Planta Norte", "consumo": 1500.0},
        {"planta": "Planta Sur", "consumo": 3400.0},
        {"planta": "Planta Este", "consumo": 980.0}
    ]

    metricas = obtener_metricas_consumo(historial_consumos)

    contexto = {
        "metricas": metricas,
        "registros": historial_consumos
    }

    return render(request, "sustentabilidad/panel.html", contexto)
