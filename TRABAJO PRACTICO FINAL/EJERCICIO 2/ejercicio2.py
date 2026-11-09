import json

# ==========================================
# PUNTO A: Excepción personalizada y Clases POO
# ==========================================

class StockInvalidoError(Exception):
    """Excepción personalizada para cuando el stock toma un valor negativo o inválido."""
    def __init__(self, mensaje="El stock no puede ser un valor negativo."):
        super().__init__(mensaje)


class DispositivoEcologico:
    """Clase base que gestiona dispositivos con validación de stock."""
    def __init__(self, nombre, stock):
        self.nombre = nombre
        self._stock = 0  # Inicializamos usando el setter para validar
        self.stock = stock  # Llama a la propiedad stock

    @property
    def stock(self):
        """Getter para obtener el stock."""
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock):
        """Setter que valida que el stock no sea negativo, lanzando StockInvalidoError."""
        if nuevo_stock < 0:
            raise StockInvalidoError(f"Error en '{self.nombre}': Stock inválido ({nuevo_stock}). No puede ser negativo.")
        self._stock = nuevo_stock

    def obtener_ficha_tecnica(self):
        """Método base para polimorfismo."""
        return f"Dispositivo: {self.nombre} | Stock: {self._stock}"


class PanelSolar(DispositivoEcologico):
    """Clase especializada que hereda de DispositivoEcologico."""
    def __init__(self, nombre, stock, potencia_watts):
        super().__init__(nombre, stock)
        self.potencia_watts = potencia_watts

    def obtener_ficha_tecnica(self):
        """Polimorfismo: sobrescribe el método para incluir la potencia específica."""
        return f"[Panel Solar] {self.nombre} - Potencia: {self.potencia_watts}W - Stock: {self.stock} unidades"


# ==========================================
# PUNTO B: Persistencia y Gestión del Catálogo
# ==========================================

class GestorInventario:
    """Clase encargada de la persistencia de datos en disco."""
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo="catalogo_ecotech.json"):
        """ Serializa y almacena la lista de dispositivos en un archivo JSON."""
        datos_serializables = []
        
        for disp in lista_dispositivos:
            # Convertimos cada objeto a un diccionario adaptado para JSON
            item = {
                "nombre": disp.nombre,
                "stock": disp.stock,
                "tipo": type(disp).__name__,
                "ficha": disp.obtener_ficha_tecnica()
            }
            # Si es un panel solar, guardamos su atributo exclusivo
            if isinstance(disp, PanelSolar):
                item["potencia_watts"] = disp.potencia_watts
                
            datos_serializables.append(item)
            
        # Guardar en el archivo JSON con indentación legible
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_serializables, archivo, indent=4, ensure_ascii=False)
            
        print(f"\n[ÉXITO] Catálogo exportado correctamente a '{ruta_archivo}'")


# ==========================================
# BLOQUE DE PRUEBA Y VALIDACIÓN CONTROLADA
# ==========================================
if __name__ == "__main__":
    print("--- 1. PROBANDO CREACIÓN DE PRODUCTOS VÁLIDOS ---")
    panel1 = PanelSolar("EcoSun 300W", 15, 300)
    panel2 = PanelSolar("EcoSun 500W", 8, 500)
    dispositivo_gen = DispositivoEcologico("Batería Litio", 10)
    
    print(panel1.obtener_ficha_tecnica())
    print(panel2.obtener_ficha_tecnica())
    print(dispositivo_gen.obtener_ficha_tecnica())

    print("\n--- 2. PROBANDO CAPTURA CONTROLADA DE StockInvalidoError ---")
    try:
        print("Intentando asignar stock negativo (-5) al panel...")
        panel1.stock = -5  # Esto debería disparar la excepción
    except StockInvalidoError as e:
        print(f"[CAPTURA DE EXCEPCIÓN EXITOSA]: {e}")

    print("\n--- 3. PERSISTENCIA EN JSON (Punto B) ---")
    # Lista con los productos que sí son válidos
    catalogo_valido = [panel1, panel2, dispositivo_gen]
    
    # Llamamos al gestor para guardar todo en disco
    GestorInventario.guardar_catalogo_json(catalogo_valido)