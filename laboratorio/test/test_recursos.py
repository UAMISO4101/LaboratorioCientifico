import tempfile
import unittest
from unittest import skip

import django
django.setup()

from django.http import HttpRequest
from django.test import Client
from PIL import Image

#Clase de pruebas unitarias para la HU SA-LCINV-3 de registro de recursos
class RecursosTestCase(unittest.TestCase):


    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    #Test para probar el registro en condiciones normales de un recurso
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

    #Test para probar el registro de un recurso cuando el codigo que es ingresado ya existe y cuando
    #el nombre asignado al recurso tambien existe, se debe recibir el mensaje de error
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

    #Test para probar el registro de un recurso cuando los campos que se reciben el request POST estan vacios
    #se debe recibir una cadena de error indicando lo anteriormente mencionado
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

    #Test para probar el la edicion de un recurso existente, el ID del producto es guardado y retornado
    #en la peticion, se debe obtener un mensaje ok
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

    #Test para probar la edicion de un recurso inexistente, al tratar de traer la referencia al producto
    #mencionado se obtiene un error y esto hace que el metodo de edicion falle
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

    #Test para probar la edicion de un recurso cuando los parametros de la peticion llegan vacios,
    #el metodo retorna una cadena de error mostrando lo anteriormente mencionado
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

    #Test para probar la edicion de un recurso/producto en 2 casos: el primero cuando se ingresa un codigo
    #que ya fue asignado a otro recurso/producto por lo que su edicion debe fallar; el segundo cuandos se
    #ingresa un nombre que ya fue asignado a otro recurso/producto por lo que su edicion debe fallar
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