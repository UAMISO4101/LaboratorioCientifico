import json
import unittest

from django.http.request import HttpRequest
from django.utils import timezone
from django.test import TestCase

from laboratorio.views import (obtenerExperimentos, obtenerExperimentosPorUsuario,
                               obtenerProtocolosPorExperimento, obtenerPPPorProtocolo)

from laboratorio.models import Experimento, ProductoProtocolo, Producto, Protocolo, Tipo, Usuario


class ExperimentosInsumosTestCase(TestCase):

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


    def test_obtenerPPPorProtocolo(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['id'] = 3
        jsonResponse = obtenerPPPorProtocolo(request)
        respuesta = jsonResponse.content
        respuesta = json.loads(respuesta)
        producto = respuesta['producto']
        productoprotocolo = respuesta['productoprotocolo']
        self.assertEquals('ProductoPrueba', producto['nombre'])
        self.assertEquals("10.100", productoprotocolo['fields']['cantidadUtilizada'])

    def test_obtenerProtocolosPorExperimento(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['codigo'] = 'EXP-1'
        jsonResponse = obtenerProtocolosPorExperimento(request)
        respuesta = json.loads(jsonResponse.content)
        respuesta = json.loads(respuesta)
        self.assertEquals(123456, respuesta[0]['fields']['version'])

    def test_obtenerExperimentosPorUsuario(self):
        request = HttpRequest()
        request.method = 'GET'
        request.GET['username'] = 'asistente1'
        jsonResponse = obtenerExperimentosPorUsuario(request)
        respuesta = json.loads(jsonResponse.content)
        respuesta = json.loads(respuesta)
        self.assertEquals('EXP-1', respuesta[0]['fields']['codigo'])

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


if __name__ == '__main__':
    unittest.main()
