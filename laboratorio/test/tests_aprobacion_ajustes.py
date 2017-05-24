import unittest

from django.test import TestCase, Client
from django.utils import timezone

from laboratorio.models import Tipo, Ajuste, Bodega, DetalleProductos, ConteoInventario, Usuario

class AprobacionAjustesTestCase(TestCase):
    """
    Clase AprobacionAjustesTestCase.

    Clase encargada de generar las pruebas unitarias para aprobacion de ajustes.
    """

    def setUp(self):
        """
        Metodo setUp que crea los datos asociados a las entidades que se van a probar.

        tipo asociado a estados de la aprobacion del ajuste.
        """
        # Every test needs a client.
        self.client = Client()

        enAprobacion = Tipo.objects.create(grupo='AJUSTE', nombre='En aprobacion')
        enAprobacion.save()

        aprobada = Tipo.objects.create(grupo='AJUSTE', nombre='Aprobada')
        aprobada.save()

        estado = Tipo.objects.create(grupo='STATUSCONTEO', nombre='Ejecutada')
        tipoDiferencia = Tipo.objects.create(grupo='TIPODIFERENCIA', nombre='Exceso')

        bodega = Bodega.objects.create()
        conteoInvetario = ConteoInventario.objects.create(estado=estado, fecha_creacion=timezone.now())
        detalleProducto = DetalleProductos.objects.create(conteoinventario=conteoInvetario)
        Ajuste.objects.create(diferencia_cantidad=1, tipo_diferencia=tipoDiferencia,
                                       estado=enAprobacion, bodega=bodega, detalle_productos=detalleProducto)

        Tipo.objects.create(nombre='Ajuste Inventario', grupo='TIPOTRX')
        Tipo.objects.create(nombre='Ejecutada', grupo='STATUSTRX')
        Usuario(first_name="prueba").save()

    def test_aprobar_ajuste(self):
        """
        Metodo test aprobar ajustes.

        Prueba unitaria que verifica la aprobacion de un ajuste de pedido
        el metodo a verificar de view es: aprobar_ajuste.

        La respuesta debe contener una orden con el estado "Aprobada" y un comentario.
        """
        response = self.client.post('/laboratorio/aprobarAjuste/', {"id_a": 1}, format='multipart')
        self.assertIn("ok", response.json()["mensaje"])
        self.assertEquals("Aprobada", Ajuste.objects.get(id=1).estado.nombre)


if __name__ == '__main__':
    unittest.main()
