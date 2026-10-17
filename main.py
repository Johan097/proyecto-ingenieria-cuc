from abc import ABC, abstractmethod

# --- Interfaces (ISP & DIP) ---
class IFacturaRepository(ABC):
    @abstractmethod
    def guardar(self, factura_id: str, monto: float) -> None:
        pass

class INotificador(ABC):
    @abstractmethod
    def enviar_notificacion(self, mensaje: str, destino: str) -> None:
        pass

# --- Patrón Strategy para Descuentos (OCP) ---
class IEstrategiaDescuento(ABC):
    @abstractmethod
    def calcular_descuento(self, monto: float) -> float:
        pass

class DescuentoVIP(IEstrategiaDescuento):
    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.20  # 20% descuento

class DescuentoRegular(IEstrategiaDescuento):
    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.05  # 5% descuento

# --- Implementaciones Concretas ---
class MySQLFacturaRepository(IFacturaRepository):
    def guardar(self, factura_id: str, monto: float) -> None:
        print(f"[DB] Factura {factura_id} guardada con monto final: ${monto:.2f}")

class EmailNotificador(INotificador):
    def enviar_notificacion(self, mensaje: str, destino: str) -> None:
        print(f"[Email a {destino}]: {mensaje}")

# --- Clase de Servicio con Inyección de Dependencias (SRP & DIP) ---
class ServicioFacturacion:
    def __init__(self, repositorio: IFacturaRepository, notificador: INotificador):
        self._repositorio = repositorio
        self._notificador = notificador

    def procesar_factura(self, factura_id: str, monto_base: float, email: str, estrategia: IEstrategiaDescuento):
        monto_final = monto_base - estrategia.calcular_descuento(monto_base)
        self._repositorio.guardar(factura_id, monto_final)
        self._notificador.enviar_notificacion(f"Factura {factura_id} procesada por ${monto_final:.2f}", email)

if __name__ == "__main__":
    servicio = ServicioFacturacion(MySQLFacturaRepository(), EmailNotificador())
    servicio.procesar_factura("FAC-2026-001", 1000.0, "johan@cuc.edu.co", DescuentoVIP())
