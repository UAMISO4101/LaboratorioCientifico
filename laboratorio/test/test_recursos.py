import tempfile
import unittest
from unittest import skip

import django
django.setup()

from django.http import HttpRequest
from django.test import Client
from PIL import Image

class RecursosTestCase(unittest.TestCase):

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    @skip("Don't want to test")
    def test_crearRecurso(self):

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        response = self.client.post('/laboratorio/guardarInsumo/',
                                    {'codigo': "PRO-test1",
                                     'nombre':"Recurso Test 1",
                                     'descripcion':"Esta es una corta descripcion de este insumo.",
                                     'valor':"50000",
                                     'unidades':"4",
                                     'clasificacion':"Pri",
                                     "medida":"1",
                                     "cantidad":"2",
                                     "imageFile":tmp_file,
                                     "proveedor":"1"}, format='multipart')
        self.assertIn("ok", response.json()["mensaje"])

        response1 = self.client.post('/laboratorio/guardarInsumo/',
                                    {'codigo': "PRO-test2",
                                     'nombre': "Recurso Test 2",
                                     'descripcion': "Esta es una corta descripcion de este insumo.",
                                     'valor': "20000",
                                     'unidades': "2",
                                     'clasificacion': "Kem",
                                     "medida": "3",
                                     "cantidad": "45",
                                     "imageFile": tmp_file,
                                     "proveedor": "2"}, format='multipart')
        self.assertIn("ok", response1.json()["mensaje"])

    @skip("Don't want to test")
    def test_existeRecurso(self):
        #codigo repetido
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        response = self.client.post('/laboratorio/guardarInsumo/',
                                    {'codigo': "PRO-test1",
                                     'nombre': "Recurso Test",
                                     'descripcion': "Esta es una corta descripcion de este insumo.",
                                     'valor': "50000",
                                     'unidades': "4",
                                     'clasificacion': "Pri",
                                     "medida": "1",
                                     "cantidad": "2",
                                     "imageFile": tmp_file,
                                     "proveedor": "1"}, format='multipart')
        self.assertIn("El insumo/reactivo con el codigo o nombre ingresado ya existe.", response.json()["mensaje"])

        #nombre repetido
        response = self.client.post('/laboratorio/guardarInsumo/',
                                    {'codigo': "PRO-test",
                                     'nombre': "Recurso Test 1",
                                     'descripcion': "Esta es una corta descripcion de este insumo.",
                                     'valor': "50000",
                                     'unidades': "4",
                                     'clasificacion': "Pri",
                                     "medida": "1",
                                     "cantidad": "2",
                                     "imageFile": tmp_file,
                                     "proveedor": "1"}, format='multipart')
        self.assertIn("El insumo/reactivo con el codigo o nombre ingresado ya existe.", response.json()["mensaje"])

    @skip("Don't want to test")
    def test_formRegistroCamposVacios(self):
        response = self.client.post('/laboratorio/guardarInsumo/',
                                    {'codigo': "",
                                     'nombre': "",
                                     'descripcion': "",
                                     'valor': "",
                                     'unidades': "",
                                     'clasificacion': "",
                                     "medida": "",
                                     "cantidad": "",
                                     "imageFile": None,
                                     "proveedor": ""}, format='multipart')
        self.assertIn("Todos los campos deben estar debidamente diligenciados", response.json()["mensaje"])

    @skip("Don't want to test")
    def test_editarRecursoExistente(self):
        response = self.client.post('/laboratorio/guardarEdicionInsumo/',
                                    {'codigo': "PRO-test1",
                                     'nombre': "Recurso Test 1",
                                     'descripcion': "Esta es una descripcion editada de este insumo.",
                                     'valor': "60000",
                                     'unidades': "7",
                                     'clasificacion': "Fe",
                                     "medida": "3",
                                     "cantidad": "45",
                                     "imageFile": None,
                                     "proveedor": "2",
                                     "id_producto_guardado":"9"}, format='multipart')
        self.assertIn("ok", response.json()["mensaje"])

    @skip("Don't want to test")
    def test_editarRecursoInexistente(self):
        response = self.client.post('/laboratorio/guardarEdicionInsumo/',
                                    {'codigo': "PRO-test1",
                                     'nombre': "Recurso Test 1",
                                     'descripcion': "Esta es una descripcion editada de este insumo.",
                                     'valor': "60000",
                                     'unidades': "7",
                                     'clasificacion': "Fe",
                                     "medida": "3",
                                     "cantidad": "45",
                                     "imageFile": None,
                                     "proveedor": "2",
                                     "id_producto_guardado": "13"}, format='multipart')
        self.assertIn("El id del insumo/reactivo que se quiere editar no existe", response.json()["mensaje"])

    @skip("Don't want to test")
    def test_editarRecursoFormCamposVacios(self):
        response = self.client.post('/laboratorio/guardarEdicionInsumo/',
                                    {'codigo': "",
                                     'nombre': "",
                                     'descripcion': "",
                                     'valor': "",
                                     'unidades': "",
                                     'clasificacion': "",
                                     "medida": "",
                                     "cantidad": "",
                                     "imageFile": None,
                                     "proveedor": "",
                                     "id_producto_guardado":"9"}, format='multipart')
        self.assertIn("Todos los campos deben estar debidamente diligenciados", response.json()["mensaje"])

    def test_edicionErroneaPorRecursoExistente(self):
        #codigo repetido
        response = self.client.post('/laboratorio/guardarEdicionInsumo/',
                                    {'codigo': "PRO-test2",
                                     'nombre': "Recurso Test",
                                     'descripcion': "Esta es una corta descripcion de este insumo.",
                                     'valor': "50000",
                                     'unidades': "4",
                                     'clasificacion': "Pri",
                                     "medida": "1",
                                     "cantidad": "2",
                                     "imageFile": None,
                                     "proveedor": "1",
                                     "id_producto_guardado": "9"}, format='multipart')
        self.assertIn("El insumo/reactivo con el codigo o nombre ingresado ya existe.", response.json()["mensaje"])

        # nombre repetido
        response = self.client.post('/laboratorio/guardarEdicionInsumo/',
                                    {'codigo': "PRO-test",
                                     'nombre': "Recurso Test 1",
                                     'descripcion': "Esta es una corta descripcion de este insumo.",
                                     'valor': "50000",
                                     'unidades': "4",
                                     'clasificacion': "Pri",
                                     "medida": "1",
                                     "cantidad": "2",
                                     "imageFile": None,
                                     "proveedor": "1",
                                     "id_producto_guardado": "10"}, format='multipart')
        self.assertIn("El insumo/reactivo con el codigo o nombre ingresado ya existe.", response.json()["mensaje"])

if __name__ == '__main__':
    unittest.main()