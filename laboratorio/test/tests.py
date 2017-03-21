import json
import unittest

from django.http.request import HttpRequest

from laboratorio.views import crearBodega, obtenerBodega


class BodegaTestCase(unittest.TestCase):

    def test_1_crear_bodega(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["serial"] = "prueba1"
        request.POST["nombre"] = "prueba1"
        request.POST["niveles"] = "1"
        request.POST["secciones"] = "1"
        request.POST["temperatura_minima"] = "4"
        request.POST["temperatura_media"] = "5"
        request.POST["ubicacion"] = "prueba1"
        request.POST["tipo_bodega"] = "1"
        request.POST["responsable"] = "1"
        jsonResponse = crearBodega(request)
        self.assertIn("ok", jsonResponse.content)
        request = HttpRequest()
        request.method = 'POST'
        request.POST["serial"] = "prueba2"
        request.POST["nombre"] = "prueba2"
        request.POST["niveles"] = "1"
        request.POST["secciones"] = "1"
        request.POST["temperatura_minima"] = "4"
        request.POST["temperatura_media"] = "5"
        request.POST["ubicacion"] = "prueba2"
        request.POST["tipo_bodega"] = "1"
        request.POST["responsable"] = "1"
        jsonResponse = crearBodega(request)
        self.assertIn("ok", jsonResponse.content)

    def test_2_existe_bodega(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["serial"] = "prueba1"
        request.POST["nombre"] = "prueba1"
        request.POST["niveles"] = "1"
        request.POST["secciones"] = "1"
        request.POST["temperatura_minima"] = "4"
        request.POST["temperatura_media"] = "5"
        request.POST["ubicacion"] = "prueba1"
        request.POST["tipo_bodega"] = "1"
        request.POST["responsable"] = "1"
        jsonResponse = crearBodega(request)
        self.assertIn("ya existe", jsonResponse.content)

    def test_3_actualizar_bodega_guardada_serial_repetido(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["id_bodega_guardada"] = "2"
        request.POST["serial"] = "prueba1"
        request.POST["nombre"] = "prueba1"
        request.POST["niveles"] = "1"
        request.POST["secciones"] = "1"
        request.POST["temperatura_minima"] = "4"
        request.POST["temperatura_media"] = "5"
        request.POST["ubicacion"] = "prueba1"
        request.POST["tipo_bodega"] = "1"
        request.POST["responsable"] = "1"
        jsonResponse = crearBodega(request)
        self.assertIn("ya existe", jsonResponse.content)

    def test_4_actualizar_bodega_guardada_serial_no_repetido(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["id_bodega_guardada"] = "1"
        request.POST["serial"] = "prueba12"
        request.POST["nombre"] = "prueba12"
        request.POST["niveles"] = "5"
        request.POST["secciones"] = "1"
        request.POST["temperatura_minima"] = "4"
        request.POST["temperatura_media"] = "5"
        request.POST["ubicacion"] = "prueba1"
        request.POST["tipo_bodega"] = "2"
        request.POST["responsable"] = "2"
        jsonResponse = crearBodega(request)
        self.assertIn("ok", jsonResponse.content)
        request = HttpRequest()
        request.method = 'GET'
        request.GET["id_bodega"] = "1"
        jsonResponse = obtenerBodega(request)
        bodega = json.loads(jsonResponse.content)
        bodega = json.loads(bodega["bodega"])
        self.assertEquals("prueba12", bodega["fields"]["serial"])

if __name__ == '__main__':
    unittest.main()
