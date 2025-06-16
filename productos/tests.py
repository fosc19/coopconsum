from django.test import TestCase
from decimal import Decimal
from .models import Categoria, Proveedor, Producto


class CategoriaModelTest(TestCase):
    """Tests per al model Categoria"""
    
    def test_crear_categoria_basic(self):
        """Test creació bàsica d'una categoria"""
        categoria = Categoria.objects.create(
            nombre='Fruites',
            descripcion='Fruites fresques de temporada'
        )
        
        self.assertEqual(categoria.nombre, 'Fruites')
        self.assertEqual(categoria.descripcion, 'Fruites fresques de temporada')
        self.assertIsNone(categoria.parent)  # Categoria principal
        self.assertEqual(str(categoria), 'Fruites')
    
    def test_crear_subcategoria(self):
        """Test creació de subcategoria amb parent"""
        # Crear categoria parent
        categoria_parent = Categoria.objects.create(
            nombre='Alimentació',
            descripcion='Productes alimentaris'
        )
        
        # Crear subcategoria
        subcategoria = Categoria.objects.create(
            nombre='Verdures',
            descripcion='Verdures ecològiques',
            parent=categoria_parent
        )
        
        self.assertEqual(subcategoria.parent, categoria_parent)
        self.assertEqual(subcategoria.nombre, 'Verdures')
        
        # Verificar relació inversa
        subcategorias = categoria_parent.subcategorias.all()
        self.assertIn(subcategoria, subcategorias)
        self.assertEqual(subcategorias.count(), 1)
    
    def test_categoria_sense_descripcion(self):
        """Test categoria amb descripció buida (permès)"""
        categoria = Categoria.objects.create(nombre='Pa')
        
        self.assertEqual(categoria.nombre, 'Pa')
        self.assertEqual(categoria.descripcion, '')  # Blank=True


class ProveedorModelTest(TestCase):
    """Tests per al model Proveedor"""
    
    def test_crear_proveedor_basic(self):
        """Test creació bàsica d'un proveïdor"""
        proveedor = Proveedor.objects.create(
            nombre='Fruiter Local',
            descripcion_corta='El millor fruiter del barri',
            contacto='Joan Martínez',
            email='joan@fruiterlocal.com',
            direccion='Carrer Major, 123'
        )
        
        self.assertEqual(proveedor.nombre, 'Fruiter Local')
        self.assertEqual(proveedor.contacto, 'Joan Martínez')
        self.assertEqual(proveedor.email, 'joan@fruiterlocal.com')
        self.assertEqual(str(proveedor), 'Fruiter Local')
    
    def test_proveedor_visibilitat_defecte(self):
        """Test visibilitat per defecte del proveïdor"""
        proveedor = Proveedor.objects.create(nombre='Test Proveïdor')
        
        self.assertTrue(proveedor.visible_en_web)  # Default True
        self.assertFalse(proveedor.visible_en_inicio)  # Default False
    
    def test_proveedor_configurar_visibilitat(self):
        """Test configuració manual de visibilitat"""
        proveedor = Proveedor.objects.create(
            nombre='Proveïdor Destacat',
            visible_en_web=True,
            visible_en_inicio=True
        )
        
        self.assertTrue(proveedor.visible_en_web)
        self.assertTrue(proveedor.visible_en_inicio)
    
    def test_proveedor_camps_opcionals(self):
        """Test que els camps opcionals funcionen correctament"""
        proveedor = Proveedor.objects.create(nombre='Proveïdor Mínim')
        
        # Camps que poden estar buits
        self.assertEqual(proveedor.descripcion_corta, '')
        self.assertEqual(proveedor.contacto, '')
        self.assertEqual(proveedor.email, '')
        self.assertEqual(proveedor.direccion, '')
        self.assertIsNone(proveedor.imagen)


class ProductoModelTest(TestCase):
    """Tests per al model Producto"""
    
    def setUp(self):
        """Configuració comuna per tots els tests"""
        self.categoria = Categoria.objects.create(
            nombre='Fruites',
            descripcion='Fruites fresques'
        )
        
        self.proveedor = Proveedor.objects.create(
            nombre='Fruiter Test',
            descripcion_corta='Proveïdor de test'
        )
    
    def test_crear_producto_basic(self):
        """Test creació bàsica d'un producte"""
        producto = Producto.objects.create(
            nombre='Taronges',
            descripcion='Taronges de València',
            precio=Decimal('2.50'),
            stock=10,
            categoria=self.categoria,
            proveedor=self.proveedor,
            unidad_venta='kg'
        )
        
        self.assertEqual(producto.nombre, 'Taronges')
        self.assertEqual(producto.precio, Decimal('2.50'))
        self.assertEqual(producto.stock, 10)
        self.assertEqual(producto.categoria, self.categoria)
        self.assertEqual(producto.proveedor, self.proveedor)
        self.assertEqual(producto.unidad_venta, 'kg')
    
    def test_producto_str_representation(self):
        """Test representació string del producte"""
        producto = Producto.objects.create(
            nombre='Pomes',
            precio=Decimal('1.80'),
            categoria=self.categoria,
            proveedor=self.proveedor,
            unidad_venta='kg'
        )
        
        expected_str = 'Pomes (Kilogramo)'
        self.assertEqual(str(producto), expected_str)
    
    def test_producto_unidades_venta(self):
        """Test diferents unitats de venta"""
        # Test unitat
        producto_ud = Producto.objects.create(
            nombre='Llaunes',
            precio=Decimal('1.20'),
            categoria=self.categoria,
            proveedor=self.proveedor,
            unidad_venta='ud'
        )
        self.assertEqual(producto_ud.get_unidad_venta_display(), 'Unidad')
        
        # Test kilogram
        producto_kg = Producto.objects.create(
            nombre='Pomes',
            precio=Decimal('2.00'),
            categoria=self.categoria,
            proveedor=self.proveedor,
            unidad_venta='kg'
        )
        self.assertEqual(producto_kg.get_unidad_venta_display(), 'Kilogramo')
        
        # Test gram
        producto_g = Producto.objects.create(
            nombre='Espècies',
            precio=Decimal('0.50'),
            categoria=self.categoria,
            proveedor=self.proveedor,
            unidad_venta='g'
        )
        self.assertEqual(producto_g.get_unidad_venta_display(), 'Gramo')
        
        # Test litre
        producto_l = Producto.objects.create(
            nombre='Oli oliva',
            precio=Decimal('8.50'),
            categoria=self.categoria,
            proveedor=self.proveedor,
            unidad_venta='l'
        )
        self.assertEqual(producto_l.get_unidad_venta_display(), 'Litre')
    
    def test_producto_camps_per_defecte(self):
        """Test valors per defecte del producte"""
        producto = Producto.objects.create(
            nombre='Producte Test',
            precio=Decimal('5.00'),
            categoria=self.categoria,
            proveedor=self.proveedor
        )
        
        self.assertEqual(producto.stock, 0)  # Default 0
        self.assertEqual(producto.unidad_venta, 'ud')  # Default unitat
        self.assertFalse(producto.es_stock)  # Default False
        self.assertFalse(producto.destacado_en_inicio)  # Default False
        self.assertEqual(producto.descripcion, '')  # Blank=True
        self.assertIsNone(producto.imagen)  # Null=True
    
    def test_producto_amb_configuracio_avançada(self):
        """Test producte amb configuració avançada"""
        producto = Producto.objects.create(
            nombre='Producte Estrella',
            descripcion='El nostre millor producte',
            precio=Decimal('12.99'),
            stock=50,
            categoria=self.categoria,
            proveedor=self.proveedor,
            unidad_venta='kg',
            es_stock=True,
            destacado_en_inicio=True
        )
        
        self.assertTrue(producto.es_stock)
        self.assertTrue(producto.destacado_en_inicio)
        self.assertEqual(producto.descripcion, 'El nostre millor producte')
    
    def test_relacions_categoria_proveedor(self):
        """Test relacions amb categoria i proveïdor"""
        # Crear múltiples productes per la mateixa categoria
        producto1 = Producto.objects.create(
            nombre='Producte 1',
            precio=Decimal('1.00'),
            categoria=self.categoria,
            proveedor=self.proveedor
        )
        
        producto2 = Producto.objects.create(
            nombre='Producte 2',
            precio=Decimal('2.00'),
            categoria=self.categoria,
            proveedor=self.proveedor
        )
        
        # Verificar relació inversa categoria -> productes
        productos_categoria = self.categoria.producto_set.all()
        self.assertEqual(productos_categoria.count(), 2)
        self.assertIn(producto1, productos_categoria)
        self.assertIn(producto2, productos_categoria)
        
        # Verificar relació inversa proveïdor -> productes  
        productos_proveedor = self.proveedor.producto_set.all()
        self.assertEqual(productos_proveedor.count(), 2)
    
    def test_producto_destacats_query(self):
        """Test query per productes destacats"""
        # Crear producte destacat
        producto_destacado = Producto.objects.create(
            nombre='Producte Destacat',
            precio=Decimal('5.00'),
            categoria=self.categoria,
            proveedor=self.proveedor,
            destacado_en_inicio=True
        )
        
        # Crear producte no destacat
        Producto.objects.create(
            nombre='Producte Normal',
            precio=Decimal('3.00'),
            categoria=self.categoria,
            proveedor=self.proveedor,
            destacado_en_inicio=False
        )
        
        # Query per destacats
        productos_destacados = Producto.objects.filter(destacado_en_inicio=True)
        self.assertEqual(productos_destacados.count(), 1)
        self.assertEqual(productos_destacados.first(), producto_destacado)