from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from datetime import date, timezone
from django.utils import timezone as django_timezone

from productos.models import Categoria, Proveedor, Producto
from eventos.models import EventoCalendario
from web.models import ConfiguracioWeb


class APIInfoViewTest(APITestCase):
    """Tests per a la vista d'informació de l'API"""

    def setUp(self):
        # Crear configuració web per test
        # Usar only() per evitar camps que podrien no existir en BD test
        existing = ConfiguracioWeb.objects.first()
        if existing:
            self.config = existing
        else:
            # Crear amb només el camp essencial
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO web_configuracioweb (nom_cooperativa) VALUES (%s) RETURNING id",
                    ['Test Cooperativa']
                )
                config_id = cursor.fetchone()[0]
            self.config = ConfiguracioWeb.objects.get(id=config_id)

    def test_api_info_endpoint(self):
        """Test endpoint informació bàsica API"""
        url = reverse('api_info')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('nom', response.data)
        self.assertIn('Test Cooperativa', response.data['nom'])
        self.assertIn('versio', response.data)
        self.assertIn('endpoints', response.data)
        
        # Verificar endpoints disponibles
        endpoints = response.data['endpoints']
        self.assertIn('proveedores', endpoints)
        self.assertIn('productos', endpoints)
        self.assertIn('categorias', endpoints)
        self.assertIn('eventos', endpoints)

    def test_api_info_sense_configuracio(self):
        """Test API info quan no hi ha ConfiguracioWeb"""
        # Eliminar configuració
        ConfiguracioWeb.objects.all().delete()
        
        url = reverse('api_info')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('CoopConsum', response.data['nom'])  # Nom per defecte


class ProveedorAPITest(APITestCase):
    """Tests per a l'API de proveïdors"""

    def setUp(self):
        # Crear proveïdors amb diferents visibilitats
        self.proveedor_visible = Proveedor.objects.create(
            nombre='Proveïdor Visible',
            descripcion_corta='Proveïdor públic',
            contacto='Test Contact',
            email='visible@test.com',
            visible_en_web=True,
            visible_en_inicio=True
        )
        
        self.proveedor_no_visible = Proveedor.objects.create(
            nombre='Proveïdor Privat',
            descripcion_corta='Proveïdor privat',
            visible_en_web=False
        )

    def test_list_proveedores_només_visibles(self):
        """Test que només retorna proveïdors visibles en web"""
        url = reverse('proveedor-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Proveïdor Visible')

    def test_detall_proveedor_visible(self):
        """Test detall d'un proveïdor visible"""
        url = reverse('proveedor-detail', kwargs={'pk': self.proveedor_visible.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Proveïdor Visible')
        self.assertEqual(response.data['email'], 'visible@test.com')
        self.assertTrue(response.data['visible_en_web'])

    def test_detall_proveedor_no_visible_404(self):
        """Test que proveïdor no visible retorna 404"""
        url = reverse('proveedor-detail', kwargs={'pk': self.proveedor_no_visible.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtrar_proveedores_per_visible_inicio(self):
        """Test filtratge per visible_en_inicio"""
        url = reverse('proveedor-list')
        response = self.client.get(url, {'visible_en_inicio': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Proveïdor Visible')

    def test_cercar_proveedores_per_nom(self):
        """Test cerca per nom de proveïdor"""
        url = reverse('proveedor-list')
        response = self.client.get(url, {'search': 'Visible'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class CategoriaAPITest(APITestCase):
    """Tests per a l'API de categories"""

    def setUp(self):
        # Crear categoria principal i subcategoria
        self.categoria_principal = Categoria.objects.create(
            nombre='Alimentació',
            descripcion='Productes alimentaris'
        )
        
        self.subcategoria = Categoria.objects.create(
            nombre='Fruites',
            descripcion='Fruites fresques',
            parent=self.categoria_principal
        )

    def test_list_categorias(self):
        """Test llistat de totes les categories"""
        url = reverse('categoria-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verificar que estan ordenades per nom
        noms = [cat['nombre'] for cat in response.data['results']]
        self.assertEqual(noms, ['Alimentació', 'Fruites'])

    def test_detall_categoria(self):
        """Test detall d'una categoria"""
        url = reverse('categoria-detail', kwargs={'pk': self.categoria_principal.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Alimentació')
        self.assertEqual(response.data['descripcion'], 'Productes alimentaris')

    def test_cercar_categorias_per_nom(self):
        """Test cerca de categories per nom"""
        url = reverse('categoria-list')
        response = self.client.get(url, {'search': 'Fruites'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Fruites')


class ProductoAPITest(APITestCase):
    """Tests per a l'API de productes"""

    def setUp(self):
        # Crear categoria
        self.categoria = Categoria.objects.create(
            nombre='Verdures',
            descripcion='Verdures fresques'
        )
        
        # Crear proveïdor visible i no visible
        self.proveedor_visible = Proveedor.objects.create(
            nombre='Verdurer Local',
            visible_en_web=True
        )
        
        self.proveedor_no_visible = Proveedor.objects.create(
            nombre='Proveïdor Privat',
            visible_en_web=False
        )
        
        # Crear productes
        self.producto_visible = Producto.objects.create(
            nombre='Tomàquets',
            descripcion='Tomàquets de temporada',
            precio=Decimal('2.50'),
            categoria=self.categoria,
            proveedor=self.proveedor_visible,
            unidad_venta='kg',
            es_stock=False,
            destacado_en_inicio=True
        )
        
        self.producto_no_visible = Producto.objects.create(
            nombre='Producte Privat',
            precio=Decimal('1.00'),
            categoria=self.categoria,
            proveedor=self.proveedor_no_visible,
            unidad_venta='ud'
        )

    def test_list_productos_només_visibles(self):
        """Test que només retorna productes de proveïdors visibles"""
        url = reverse('producto-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Tomàquets')

    def test_detall_producto_no_inclou_preu(self):
        """Test que el detall del producte no inclou el preu per seguretat"""
        url = reverse('producto-detail', kwargs={'pk': self.producto_visible.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('precio', response.data)
        self.assertIn('nombre', response.data)
        self.assertIn('categoria', response.data)
        self.assertIn('proveedor', response.data)

    def test_producto_amb_relacions_completes(self):
        """Test que el producte inclou dades completes de categoria i proveïdor"""
        url = reverse('producto-detail', kwargs={'pk': self.producto_visible.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar dades de categoria
        categoria = response.data['categoria']
        self.assertEqual(categoria['nombre'], 'Verdures')
        self.assertEqual(categoria['descripcion'], 'Verdures fresques')
        
        # Verificar dades de proveïdor
        proveedor = response.data['proveedor']
        self.assertEqual(proveedor['nombre'], 'Verdurer Local')
        self.assertTrue(proveedor['visible_en_web'])

    def test_unidad_venta_display(self):
        """Test que inclou la representació llegible de la unitat de venta"""
        url = reverse('producto-detail', kwargs={'pk': self.producto_visible.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unidad_venta'], 'kg')
        self.assertEqual(response.data['unidad_venta_display'], 'Kilogramo')

    def test_filtrar_per_categoria(self):
        """Test filtratge de productes per categoria"""
        url = reverse('producto-list')
        response = self.client.get(url, {'categoria': self.categoria.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filtrar_per_destacado_inicio(self):
        """Test filtratge per productes destacats a l'inici"""
        url = reverse('producto-list')
        response = self.client.get(url, {'destacado_en_inicio': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Tomàquets')

    def test_cercar_per_nom_producto(self):
        """Test cerca de productes per nom"""
        url = reverse('producto-list')
        response = self.client.get(url, {'search': 'Tomàquets'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_cercar_per_nom_proveedor(self):
        """Test cerca de productes per nom de proveïdor"""
        url = reverse('producto-list')
        response = self.client.get(url, {'search': 'Verdurer'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class EventoAPITest(APITestCase):
    """Tests per a l'API d'esdeveniments"""

    def setUp(self):
        # Crear esdeveniments amb diferents configuracions de compartició
        self.evento_public = EventoCalendario.objects.create(
            titulo='Esdeveniment Públic',
            descripcion='Esdeveniment compartit via API',
            fecha=date.today(),
            color='#28a745',
            compartir_api=True
        )
        
        self.evento_privat = EventoCalendario.objects.create(
            titulo='Esdeveniment Privat',
            descripcion='Esdeveniment intern',
            fecha=date.today(),
            color='#dc3545',
            compartir_api=False
        )

    def test_list_eventos_només_publics(self):
        """Test que només retorna esdeveniments marcats per compartir en API"""
        url = reverse('evento-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['titulo'], 'Esdeveniment Públic')

    def test_detall_evento_public(self):
        """Test detall d'un esdeveniment públic"""
        url = reverse('evento-detail', kwargs={'pk': self.evento_public.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], 'Esdeveniment Públic')
        self.assertEqual(response.data['color'], '#28a745')

    def test_detall_evento_privat_404(self):
        """Test que esdeveniment privat retorna 404"""
        url = reverse('evento-detail', kwargs={'pk': self.evento_privat.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtrar_eventos_per_color(self):
        """Test filtratge d'esdeveniments per color"""
        url = reverse('evento-list')
        response = self.client.get(url, {'color': '#28a745'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_cercar_eventos_per_titulo(self):
        """Test cerca d'esdeveniments per títol"""
        url = reverse('evento-list')
        response = self.client.get(url, {'search': 'Públic'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class APIPaginacioTest(APITestCase):
    """Tests per verificar la paginació de l'API"""

    def setUp(self):
        # Crear molts proveïdors per testar paginació
        self.categoria = Categoria.objects.create(nombre='Test', descripcion='Test')
        
        # Crear 25 proveïdors visibles (més que la pàgina per defecte de 20)
        for i in range(25):
            Proveedor.objects.create(
                nombre=f'Proveïdor {i:02d}',
                visible_en_web=True
            )

    def test_paginacio_proveedores(self):
        """Test que la paginació funciona correctament"""
        url = reverse('proveedor-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar estructura de paginació
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Verificar que mostra 20 elements per pàgina
        self.assertEqual(len(response.data['results']), 20)
        self.assertEqual(response.data['count'], 25)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_segona_pagina(self):
        """Test navegació a la segona pàgina"""
        url = reverse('proveedor-list')
        response = self.client.get(url, {'page': 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # 25 - 20 = 5
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])


class APIMethodsTest(APITestCase):
    """Tests per verificar que l'API és només de lectura"""

    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre='Test Proveïdor',
            visible_en_web=True
        )

    def test_post_no_permès(self):
        """Test que POST no està permès"""
        url = reverse('proveedor-list')
        data = {'nombre': 'Nou Proveïdor'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_no_permès(self):
        """Test que PUT no està permès"""
        url = reverse('proveedor-detail', kwargs={'pk': self.proveedor.pk})
        data = {'nombre': 'Proveïdor Modificat'}
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_no_permès(self):
        """Test que DELETE no està permès"""
        url = reverse('proveedor-detail', kwargs={'pk': self.proveedor.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_no_permès(self):
        """Test que PATCH no està permès"""
        url = reverse('proveedor-detail', kwargs={'pk': self.proveedor.pk})
        data = {'nombre': 'Parcialment Modificat'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)