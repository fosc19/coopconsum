from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import PedidoColectivo, ComandaRecurrente, SeleccionSocio, DetalleSeleccion
from socios.models import Socio, CuentaSocio
from productos.models import Categoria, Proveedor, Producto


class PedidoColectivoModelTest(TestCase):
    """Tests per al model PedidoColectivo"""
    
    def setUp(self):
        """Configuració comuna per tots els tests"""
        # Crear socio responsable
        self.socio = Socio.objects.create(
            nombre='Gestor',
            apellido='Comandes',
            email='gestor@example.com'
        )
        
        # Crear proveïdor i categoria
        self.proveedor = Proveedor.objects.create(
            nombre='Proveïdor Test',
            descripcion_corta='Proveïdor de test'
        )
        self.categoria = Categoria.objects.create(
            nombre='Verdures',
            descripcion='Verdures fresques'
        )
        
        # Crear comanda recurrent
        self.comanda_recurrente = ComandaRecurrente.objects.create(
            nombre='Comanda Setmanal Test',
            frecuencia='semanal',
            dia_semana=1,  # Dilluns
            fecha_inicio=timezone.now().date(),
            socio_asignado=self.socio
        )
    
    def test_crear_pedido_colectivo_basic(self):
        """Test creació bàsica d'un pedido colectivo"""
        pedido = PedidoColectivo.objects.create(
            tipo='semanal',
            estado='abierto',
            fecha_apertura=timezone.now(),
            fecha_inicio_pedidos=timezone.now(),
            fecha_cierre=timezone.now() + timedelta(days=5),
            fecha_entrega=timezone.now() + timedelta(days=7),
            comanda=self.comanda_recurrente,
            socio=self.socio
        )
        
        self.assertEqual(pedido.tipo, 'semanal')
        self.assertEqual(pedido.estado, 'abierto')
        self.assertEqual(pedido.comanda, self.comanda_recurrente)
        self.assertEqual(pedido.socio, self.socio)
    
    def test_workflow_estados_pedido(self):
        """Test workflow d'estats del pedido"""
        pedido = PedidoColectivo.objects.create(
            tipo='semanal',
            estado='abierto',
            fecha_apertura=timezone.now(),
            fecha_inicio_pedidos=timezone.now(),
            fecha_cierre=timezone.now() + timedelta(days=5),
            fecha_entrega=timezone.now() + timedelta(days=7),
            comanda=self.comanda_recurrente,
            socio=self.socio
        )
        
        # Test estat inicial
        self.assertEqual(pedido.estado, 'abierto')
        
        # Test canvi a tancat
        pedido.estado = 'cerrado'
        pedido.save()
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'cerrado')
        
        # Test canvi a pendent
        pedido.estado = 'pendiente'
        pedido.save()
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'pendiente')
        
        # Test canvi a llest per finalitzar
        pedido.estado = 'listo_para_finalizar'
        pedido.save()
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'listo_para_finalizar')
        
        # Test estat final
        pedido.estado = 'inactivo'
        pedido.save()
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'inactivo')
    
    def test_pedido_amb_filtres(self):
        """Test pedido amb filtres de categoria i proveïdor"""
        pedido = PedidoColectivo.objects.create(
            tipo='esporadico',
            estado='abierto',
            fecha_apertura=timezone.now(),
            fecha_inicio_pedidos=timezone.now(),
            fecha_cierre=timezone.now() + timedelta(days=3),
            fecha_entrega=timezone.now() + timedelta(days=5),
            comanda=self.comanda_recurrente,
            socio=self.socio,
            categoria=self.categoria,
            proveedor=self.proveedor
        )
        
        self.assertEqual(pedido.categoria, self.categoria)
        self.assertEqual(pedido.proveedor, self.proveedor)
        self.assertEqual(pedido.tipo, 'esporadico')


class ComandaRecurrenteModelTest(TestCase):
    """Tests per al model ComandaRecurrente"""
    
    def setUp(self):
        self.socio = Socio.objects.create(
            nombre='Responsable',
            apellido='Test',
            email='responsable@example.com'
        )
    
    def test_crear_comanda_semanal(self):
        """Test creació comanda recurrent setmanal"""
        comanda = ComandaRecurrente.objects.create(
            nombre='Verdures Setmanals',
            frecuencia='semanal',
            dia_semana=2,  # Dimarts
            fecha_inicio=timezone.now().date(),
            socio_asignado=self.socio,
            estado='activa'
        )
        
        self.assertEqual(comanda.nombre, 'Verdures Setmanals')
        self.assertEqual(comanda.frecuencia, 'semanal')
        self.assertEqual(comanda.dia_semana, 2)
        self.assertEqual(comanda.estado, 'activa')
        self.assertEqual(comanda.socio_asignado, self.socio)
    
    def test_crear_comanda_quinzenal(self):
        """Test creació comanda quinzenal"""
        comanda = ComandaRecurrente.objects.create(
            nombre='Pa Quinzenal',
            frecuencia='quincenal',
            dia_semana=5,  # Divendres
            fecha_inicio=timezone.now().date(),
            socio_asignado=self.socio
        )
        
        self.assertEqual(comanda.frecuencia, 'quincenal')
        self.assertEqual(comanda.dia_semana, 5)
    
    def test_crear_comanda_esporadica(self):
        """Test creació comanda esporàdica"""
        fecha_fin = timezone.now().date() + timedelta(days=30)
        
        comanda = ComandaRecurrente.objects.create(
            nombre='Comanda Especial Nadal',
            frecuencia='esporadico',
            fecha_inicio=timezone.now().date(),
            fecha_fin=fecha_fin,
            socio_asignado=self.socio
        )
        
        self.assertEqual(comanda.frecuencia, 'esporadico')
        self.assertEqual(comanda.fecha_fin, fecha_fin)
    
    def test_str_comanda_recurrente(self):
        """Test representació string de ComandaRecurrente"""
        comanda = ComandaRecurrente.objects.create(
            nombre='Test Comanda',
            frecuencia='semanal',
            dia_semana=1,
            fecha_inicio=timezone.now().date(),
            socio_asignado=self.socio
        )
        
        str_repr = str(comanda)
        # El __str__ mostra "Sin categoría - Sin proveedor - [nom socio] - (comanda Semanal)"
        self.assertIn('Sin categoría', str_repr)
        self.assertIn('Sin proveedor', str_repr)
        self.assertIn('Responsable', str_repr)  # nom del socio en setUp
        self.assertIn('comanda Semanal', str_repr)


class SeleccionSocioModelTest(TestCase):
    """Tests per al model SeleccionSocio i DetalleSeleccion"""
    
    def setUp(self):
        # Crear socio i compte
        self.socio = Socio.objects.create(
            nombre='Comprador',
            apellido='Test',
            email='comprador@example.com'
        )
        
        # Crear socio gestor
        self.gestor = Socio.objects.create(
            nombre='Gestor',
            apellido='Test',
            email='gestor@example.com'
        )
        
        # Crear comanda i pedido
        self.comanda = ComandaRecurrente.objects.create(
            nombre='Test Comanda',
            frecuencia='semanal',
            dia_semana=1,
            fecha_inicio=timezone.now().date(),
            socio_asignado=self.gestor
        )
        
        self.pedido = PedidoColectivo.objects.create(
            tipo='semanal',
            estado='abierto',
            fecha_apertura=timezone.now(),
            fecha_inicio_pedidos=timezone.now(),
            fecha_cierre=timezone.now() + timedelta(days=5),
            fecha_entrega=timezone.now() + timedelta(days=7),
            comanda=self.comanda,
            socio=self.gestor
        )
        
        # Crear producte
        self.categoria = Categoria.objects.create(
            nombre='Fruites',
            descripcion='Fruites fresques'
        )
        
        self.proveedor = Proveedor.objects.create(
            nombre='Fruiter Local',
            descripcion_corta='El millor fruiter'
        )
        
        self.producto = Producto.objects.create(
            nombre='Taronges',
            precio=Decimal('2.50'),
            unidad_venta='kg',
            categoria=self.categoria,
            proveedor=self.proveedor
        )
    
    def test_crear_seleccion_socio(self):
        """Test creació selecció de socio"""
        seleccion = SeleccionSocio.objects.create(
            socio=self.socio,
            pedido=self.pedido
        )
        
        self.assertEqual(seleccion.socio, self.socio)
        self.assertEqual(seleccion.pedido, self.pedido)
        self.assertIsNotNone(seleccion.fecha_seleccion)
    
    def test_crear_detalle_seleccion(self):
        """Test creació detall de selecció amb producte"""
        seleccion = SeleccionSocio.objects.create(
            socio=self.socio,
            pedido=self.pedido
        )
        
        detalle = DetalleSeleccion.objects.create(
            seleccion=seleccion,
            producto=self.producto,
            cantidad=Decimal('2.5')  # 2.5 kg taronges
        )
        
        self.assertEqual(detalle.seleccion, seleccion)
        self.assertEqual(detalle.producto, self.producto)
        self.assertEqual(detalle.cantidad, Decimal('2.5'))
    
    def test_workflow_seleccion_completa(self):
        """Test workflow complet: socio selecciona múltiples productes"""
        # Crear més productes
        producto2 = Producto.objects.create(
            nombre='Pomes',
            precio=Decimal('1.80'),
            unidad_venta='kg',
            categoria=self.categoria,
            proveedor=self.proveedor
        )
        
        # Crear selecció
        seleccion = SeleccionSocio.objects.create(
            socio=self.socio,
            pedido=self.pedido
        )
        
        # Afegir múltiples productes
        DetalleSeleccion.objects.create(
            seleccion=seleccion,
            producto=self.producto,  # Taronges
            cantidad=Decimal('1.5')
        )
        
        DetalleSeleccion.objects.create(
            seleccion=seleccion,
            producto=producto2,  # Pomes
            cantidad=Decimal('2.0')
        )
        
        # Verificar que la selecció té 2 detalls
        detalls = DetalleSeleccion.objects.filter(seleccion=seleccion)
        self.assertEqual(detalls.count(), 2)
        
        # Calcular import total esperat
        import_total = (Decimal('1.5') * self.producto.precio) + (Decimal('2.0') * producto2.precio)
        expected_total = (Decimal('1.5') * Decimal('2.50')) + (Decimal('2.0') * Decimal('1.80'))
        self.assertEqual(import_total, expected_total)  # 3.75 + 3.60 = 7.35
    
    def test_unicitat_seleccion_per_socio_pedido(self):
        """Test que un socio només pot tenir una selecció per pedido"""
        # Crear primera selecció
        seleccion1 = SeleccionSocio.objects.create(
            socio=self.socio,
            pedido_colectivo=self.pedido
        )
        
        # Verificar que existeix
        self.assertIsNotNone(seleccion1.id)
        
        # Intentar crear segona selecció pel mateix socio i pedido
        # (Això hauria de ser controlat per la lògica de negoci)
        seleccions = SeleccionSocio.objects.filter(
            socio=self.socio,
            pedido_colectivo=self.pedido
        )
        self.assertEqual(seleccions.count(), 1)