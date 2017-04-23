import unittest

from django.utils import timezone
from django.test import TestCase, Client

from laboratorio.models import Tipo, OrdenPedido, ComentarioOrden

class AprobacionOrdenesTestCase(TestCase):
    """
    Clase AprobacionOrdenesTestCase.

    Clase encargada de generar las pruebas unitarias para aprobacion de ordenes de pedido y comentarios.
    """

    def setUp(self):
        """
        Metodo setUp que crea los datos asociados a las entidades que se van a probar.

        Se crean dos usuarios, cuatro tipos, una orden.
        """
        # Every test needs a client.
        self.client = Client()

        enAprobacion = Tipo.objects.create(grupo='ORDENPEDIDO', nombre='En aprobacion')
        enAprobacion.save()

        aprobada = Tipo.objects.create(grupo='ORDENPEDIDO', nombre='Aprobada')
        aprobada.save()

        rechazada = Tipo.objects.create(grupo='ORDENPEDIDO', nombre='Rechazada')
        rechazada.save()

        enProveedor = Tipo.objects.create(grupo='ORDENPEDIDO', nombre='En proveedor')
        enProveedor.save()

        ordenParaAprobar = OrdenPedido(estado=enAprobacion)
        ordenParaAprobar.save()
        ordenParaRechazar = OrdenPedido(estado=enAprobacion)
        ordenParaRechazar.save()
        ordenConComentario = OrdenPedido(estado=aprobada)
        ordenConComentario.save()

        comentario = ComentarioOrden(comentario="Un comentario", timestamp=timezone.now(), orden=ordenConComentario)
        comentario.save()

    def test_aprobar_orden(self):
        """
        Metodo test aprobar orden.

        Prueba unitaria que verifica la aprobacion de una orden de pedido
        el metodo a verificar de view es: aprobar_orden.

        La respuesta debe contener una orden con el estado "Aprobada" y un comentario.
        """
        response = self.client.generic('POST','/laboratorio/aprobarOrden/',
                                    '{"id_op": 1, "comentario": "Comentario Aprobado"}')
        self.assertIn("ok", response.json()["mensaje"])
        self.assertEquals("Aprobada", OrdenPedido.objects.get(id=1).estado.nombre)
        self.assertEquals("Comentario Aprobado", OrdenPedido.objects.get(id=1).op_comentarios.first().comentario)

    def test_rechazar_orden(self):
        """
        Metodo test rechazar orden.

        Prueba unitaria que verifica el rechazo de una orden de pedido
        el metodo a verificar de view es: rechazar_orden.

        La respuesta debe contener una orden con el estado "Rechazada" y un comentario.
        """
        response = self.client.generic('POST', '/laboratorio/rechazarOrden/',
                                       '{"id_op": 2, "comentario": "Comentario Rechazado"}')
        self.assertIn("ok", response.json()["mensaje"])
        self.assertEquals("Rechazada", OrdenPedido.objects.get(id=2).estado.nombre)
        self.assertEquals("Comentario Rechazado", OrdenPedido.objects.get(id=2).op_comentarios.first().comentario)

    def test_comentario_orden(self):
        """
        Metodo test obtener comentarios orden.

        Prueba unitaria para obtener los comentarios de una orden de pedido
        el metodo a verificar de view es: obtener_comentarios_orden.

        La respuesta debe contener un comentario.
        """
        response = self.client.get('/laboratorio/obtenerComentariosOrden/',
                                       {"id_op": 3})
        self.assertIn("Un comentario", response.json())


    def test_cambiar_aprobada_en_proveedor(self):
        """
        Metodo test cambiar a estado En proveedor.

        Prueba unitaria que verifica el paso a En proveedor
        el metodo a verificar de view es: cambiar_aprobada_en_proveedor.

        La respuesta debe contener un comentario.
        """
        response = self.client.post('/laboratorio/enProveedor/',
                                       {"id_op": 3}, format="multipart")
        self.assertIn("ok", response.json()["mensaje"])
        self.assertEquals("En proveedor", OrdenPedido.objects.get(id=3).estado.nombre)


if __name__ == '__main__':
    """Metodo principal de test."""
    unittest.main()
