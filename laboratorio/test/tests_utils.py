import unittest
from unittest import TestCase

from decimal import Decimal

from django.http.request import HttpRequest

from laboratorio.models import Tipo
from laboratorio.utils.utils import utils
from laboratorio.views import convertirUnidad

"""Clase UtilsTest.

Clase encargada de generar las pruebas unitarias para la clase Utils

"""
class UtilsTestCase(TestCase):

    """Metodo que sirve para configuracion inicial de testcase
    """
    def setUp(self):
        tipo = Tipo.objects.create(grupo='CONVERSION_PESO', nombre='g', medidaDestino='Kg', valor=0.0001)
        tipo.save()
        tipo = Tipo.objects.create(grupo='CONVERSION_PESO', nombre='Kg', medidaDestino='g', valor=1000)
        tipo.save()

    """Metodo de prueba para convertir de gramos a kilogramos
    """
    def test_conversion_peso1(self):
        cantidad = 15
        medidaOrigen = "g"
        medidaDestino = "Kg"
        resultado = utils.convertir(cantidad,medidaOrigen,medidaDestino)
        self.assertEquals(resultado, Decimal('0.0015'))

    """Metodo de prueba para convertir de kilogramos a gramos
    """
    def test_conversion_peso2(self):
        cantidad = 15
        medidaOrigen = "Kg"
        medidaDestino = "g"
        resultado = utils.convertir(cantidad,medidaOrigen,medidaDestino)
        self.assertEquals(resultado, Decimal('15000'))


    """Metodo test que verifica conversion.

    Prueba unitaria que verifica la conversion de gramos a Kilogramos desde rest

    La respuesta debe contener la cadena "0.0015", si encontro una bodega

    """
    def test_rest_conversion_peso3(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['cantidad'] = 15
        request.GET['medidaOrigen'] = "g"
        request.GET['medidaDestino'] = "Kg"
        jsonResponse = convertirUnidad(request)
        self.assertIn("0.0015", jsonResponse.content)


"""Metodo principal de test.
"""
if __name__ == '__main__':
    unittest.main()