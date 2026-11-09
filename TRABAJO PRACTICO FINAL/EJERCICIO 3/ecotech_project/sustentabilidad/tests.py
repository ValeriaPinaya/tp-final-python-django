from django.test import TestCase
from sustentabilidad.services import calcular_emisiones_carbono

class TestCalculoEmisiones(TestCase):
    """Punto A: Auditoría de Algoritmo de Emisiones con unittest."""

    def test_calculo_nominal_exacto(self):
        """Verifica la exactitud numérica con un valor nominal estándar."""
        resultado = calcular_emisiones_carbono(100, 0.4)
        self.assertEqual(resultado, 40.0)

    def test_calculo_con_factor_personalizado(self):
        """Verifica el cálculo utilizando un factor de emisión alternativo."""
        resultado = calcular_emisiones_carbono(200, 0.5)
        self.assertEqual(resultado, 100.0)

    def test_excepcion_consumo_negativo(self):
        """Verifica que se eleve ValueError si el consumo es negativo."""
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50)
