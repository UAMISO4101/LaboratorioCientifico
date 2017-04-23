import json
import unittest

from django.http.request import HttpRequest
from django.utils import timezone
from django.test import TestCase

from laboratorio.views import (obtenerExperimentos, obtenerExperimentosPorUsuario,
                               obtenerProtocolosPorExperimento, obtenerPPPorProtocolo)

from laboratorio.models import Experimento, ProductoProtocolo, Producto, Protocolo, Tipo, Usuario

"""Clase ExperimentosInsumosTestCase.

Clase encargada de generar las pruebas unitarias para visualizacion de insumos por experimentos.

"""
class ExperimentosInsumosTestCase(TestCase):

    """Metodo setUp que crea los datos asociados a las entidades que se van a probar
        Se crea un usuario, un tipo, un protocolo, un producto, un experimento y un productoprotocolo
       """
    def setUp(self):
        usuario = Usuario.objects.create(username='asistente1')
        usuario.save()
        tipo = Tipo.objects.create(grupo='peso', nombre='gramos')
        tipo.save()
        protocolo = Protocolo.objects.create(version=123456,nombre='Protocolo Prueba',fecha=timezone.now(),
                                             descripcion='Protocolo de prueba')
        protocolo.save()
        producto = Producto.objects.create(codigo='PP-1', nombre='ProductoPrueba', descripcion='Producto de prueba',
                                           valorUnitario=100, unidadesExistentes=10,
                                           clasificacion=('Otros', 'Moleculas genericas'),unidad_medida=tipo)
        producto.save()
        experimento = Experimento.objects.create(codigo='EXP-1',nombre='Experimento de prueba', fecha=timezone.now(),
                                                estado='En progreso')
        experimento.save()
        experimento.asignado.add(usuario)
        experimento.protocolo.add(protocolo)
        experimento.save()
        productoProtocolo = ProductoProtocolo.objects.create(descripcion='', cantidadUtilizada=10.1, protocolo=protocolo,
                                                             producto=producto)
        productoProtocolo.save()

    """Metodo test obtener ProductoPortocolo por Protocolo.

    Prueba unitaria que verifica la obtencion de los ProductosProtocolo de un protocolo paricular
    el metodo a verificar de view es: obtenerPPPorProtocolo

    La respuesta debe contener un producto con el nombre "ProductoPrueba",
    y un productoprotocolo con una cantidadUtilizada de 10.100

    """
    def test_obtenerPPPorProtocolo(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['id'] = 1
        jsonResponse = obtenerPPPorProtocolo(request)
        respuesta = jsonResponse.content
        respuesta = json.loads(respuesta)
        producto = respuesta['producto']
        productoprotocolo = respuesta['productoprotocolo']
        self.assertEquals('ProductoPrueba', producto['nombre'])
        self.assertEquals("10.100", productoprotocolo['fields']['cantidadUtilizada'])

    """Metodo test obtener ProductoPortocolo por Protocolo.

    Prueba unitaria que verifica la obtencion de los protocolos por experimento
    el metodo a verificar de view es: obtenerProtocolosPorExperimento

    La respuesta debe contener el protocolo con la version "123456"

    """
    def test_obtenerProtocolosPorExperimento(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['codigo'] = 'EXP-1'
        jsonResponse = obtenerProtocolosPorExperimento(request)
        respuesta = json.loads(jsonResponse.content)
        respuesta = json.loads(respuesta)
        self.assertEquals(123456, respuesta[0]['fields']['version'])

    """Metodo test obtener experimentos por Usuario.

    Prueba unitaria que verifica la obtencion de experimentos por usuario
    el metodo a verificar de view es: obtenerExperimentosPorUsuario

    La respuesta debe contener el expeimento con el codigo "EXP-1", el parametro de la consulta
    es el username del usuario "asistente1"

    """
    def test_obtenerExperimentosPorUsuario(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['username'] = 'asistente1'
        jsonResponse = obtenerExperimentosPorUsuario(request)
        respuesta = json.loads(jsonResponse.content)
        respuesta = json.loads(respuesta)
        self.assertEquals('EXP-1', respuesta[0]['fields']['codigo'])

    """Metodo test obtener experimentos en la aplicacion.

    Prueba unitaria que verifica la obtencion de experimentos de la aplicacion
    el metodo a verificar de view es: obtenerExperimentos

    La respuesta debe contener el experimento con el codigo "EXP-1", y su asignado debe tener el username
    "asistente1"

    """
    def test_obtenerExperimentos(self):
        request = HttpRequest()
        request.method = 'GET'
        jsonResponse = obtenerExperimentos(request)
        respuesta = jsonResponse.content
        respuesta = json.loads(respuesta)
        asignado = respuesta[0]['asignado']
        experimento = respuesta[0]['experimento']
        self.assertEquals('asistente1', asignado['username'])
        self.assertEquals('EXP-1', experimento['fields']['codigo'])

"""Metodo principal de test.
"""
if __name__ == '__main__':
    unittest.main()
