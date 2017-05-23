import unittest

from django.utils import timezone
from django.test import TestCase, Client

from laboratorio.models import Tipo, Ajuste

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


    def test_aprobar_ajuste(self):
        """
        Metodo test aprobar ajustes.

        Prueba unitaria que verifica la aprobacion de un ajuste de pedido
        el metodo a verificar de view es: aprobar_ajuste.

        La respuesta debe contener una orden con el estado "Aprobada" y un comentario.
        """
        #response = self.client.generic('GET','/laboratorio/aprobarAjuste?id_a=1')
        #self.assertIn("ok", response.json()["mensaje"])
        #self.assertEquals("Aprobada", Ajuste.objects.get(id=1).estado.nombre)


if __name__ == '__main__':
    unittest.main()
