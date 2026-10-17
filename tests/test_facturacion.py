import unittest
from main import ServicioFacturacion, DescuentoVIP

class MockRepo:
    def guardar(self, fid, monto): pass

class MockNotificador:
    def enviar_notificacion(self, msg, dest): pass

class TestServicioFacturacion(unittest.TestCase):
    def test_descuento_vip(self):
        servicio = ServicioFacturacion(MockRepo(), MockNotificador())
        estrategia = DescuentoVIP()
        self.assertEqual(estrategia.calcular_descuento(1000.0), 200.0)

if __name__ == '__main__':
    unittest.main()
