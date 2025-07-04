from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Socio, CuentaSocio, MovimientoCuenta


class SocioModelTest(TestCase):
    """Tests per al model Socio"""
    
    def setUp(self):
        """Configuració comuna per tots els tests"""
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_crear_socio_basic(self):
        """Test creació bàsica d'un socio"""
        socio = Socio.objects.create(
            nombre='Joan',
            apellido='Martínez', 
            email='joan@example.com',
            telefono='666555444'
        )
        
        self.assertEqual(socio.nombre, 'Joan')
        self.assertEqual(socio.apellido, 'Martínez')
        self.assertEqual(socio.email, 'joan@example.com')
        self.assertEqual(str(socio), 'Joan Martínez')
    
    def test_socio_amb_user(self):
        """Test socio associat a un User de Django"""
        socio = Socio.objects.create(
            user=self.user,
            nombre='Maria',
            apellido='García',
            email='maria@example.com'
        )
        
        self.assertEqual(socio.user, self.user)
        self.assertEqual(socio.user.username, 'test_user')
    
    def test_permisos_per_defecte(self):
        """Test que els permisos estan desactivats per defecte"""
        socio = Socio.objects.create(
            nombre='Pere',
            apellido='López',
            email='pere@example.com'
        )
        
        self.assertFalse(socio.gestiona_stock)
        self.assertFalse(socio.gestiona_productos)
        self.assertFalse(socio.puede_crear_comandas_esporadicas)
    
    def test_activar_permisos(self):
        """Test activació permisos de socio"""
        socio = Socio.objects.create(
            nombre='Anna',
            apellido='Rodríguez',
            email='anna@example.com',
            gestiona_stock=True,
            gestiona_productos=True
        )
        
        self.assertTrue(socio.gestiona_stock)
        self.assertTrue(socio.gestiona_productos)
        self.assertFalse(socio.puede_crear_comandas_esporadicas)


class CuentaSocioModelTest(TestCase):
    """Tests per al model CuentaSocio"""
    
    def setUp(self):
        self.socio = Socio.objects.create(
            nombre='Laura',
            apellido='González',
            email='laura@example.com'
        )
    
    def test_crear_cuenta_automatica(self):
        """Test creació manual de CuentaSocio"""
        # Crear compte manualment
        cuenta = CuentaSocio.objects.create(socio=self.socio)
        self.assertEqual(cuenta.saldo_actual, Decimal('0.00'))
        self.assertEqual(cuenta.socio, self.socio)
    
    def test_str_cuenta_socio(self):
        """Test representació string de CuentaSocio"""
        cuenta = CuentaSocio.objects.create(socio=self.socio)
        expected = f"Cuenta de {self.socio}"
        self.assertEqual(str(cuenta), expected)
    
    def test_modificar_saldo(self):
        """Test modificació manual del saldo"""
        cuenta = CuentaSocio.objects.create(socio=self.socio)
        cuenta.saldo_actual = Decimal('50.00')
        cuenta.save()
        
        cuenta.refresh_from_db()
        self.assertEqual(cuenta.saldo_actual, Decimal('50.00'))


class MovimientoCuentaModelTest(TestCase):
    """Tests per al model MovimientoCuenta"""
    
    def setUp(self):
        self.socio = Socio.objects.create(
            nombre='Carlos',
            apellido='Fernández',
            email='carlos@example.com'
        )
        self.cuenta = CuentaSocio.objects.create(socio=self.socio)
    
    def test_crear_movimiento_ingreso(self):
        """Test creació moviment d'ingrés"""
        movimiento = MovimientoCuenta.objects.create(
            cuenta=self.cuenta,
            tipo_movimiento='ingreso',
            monto=Decimal('25.50'),
            descripcion='Ingrés inicial',
            estado='validado'
        )
        
        self.assertEqual(movimiento.cuenta, self.cuenta)
        self.assertEqual(movimiento.tipo_movimiento, 'ingreso')
        self.assertEqual(movimiento.monto, Decimal('25.50'))
        self.assertEqual(movimiento.estado, 'validado')
        self.assertIsNotNone(movimiento.fecha)
    
    def test_crear_movimiento_egreso(self):
        """Test creació moviment d'egrés"""
        movimiento = MovimientoCuenta.objects.create(
            cuenta=self.cuenta,
            tipo_movimiento='egreso',
            monto=Decimal('15.00'),  # Import positiu, el tipus indica que és egrés
            descripcion='Compra productes',
            estado='pendiente'
        )
        
        self.assertEqual(movimiento.tipo_movimiento, 'egreso')
        self.assertEqual(movimiento.monto, Decimal('15.00'))
        self.assertEqual(movimiento.estado, 'pendiente')
    
    def test_str_movimiento(self):
        """Test representació string de MovimientoCuenta"""
        movimiento = MovimientoCuenta.objects.create(
            cuenta=self.cuenta,
            tipo_movimiento='ingreso',
            monto=Decimal('10.00'),
            descripcion='Test ingrés'
        )
        
        # El __str__ del model ha de mostrar informació útil
        str_repr = str(movimiento)
        self.assertIn('ingreso', str_repr)  # Tipus de moviment
        self.assertIn('10.00', str_repr)   # Import
    
    def test_multiple_movimientos(self):
        """Test múltiples moviments per la mateixa cuenta"""
        # Crear diversos moviments
        MovimientoCuenta.objects.create(
            cuenta=self.cuenta,
            tipo_movimiento='ingreso',
            monto=Decimal('50.00'),
            descripcion='Ingrés inicial',
            estado='validado'
        )
        MovimientoCuenta.objects.create(
            cuenta=self.cuenta,
            tipo_movimiento='egreso', 
            monto=Decimal('20.00'),  # Import positiu
            descripcion='Compra productes',
            estado='validado'
        )
        MovimientoCuenta.objects.create(
            cuenta=self.cuenta,
            tipo_movimiento='egreso',
            monto=Decimal('5.00'),  # Import positiu
            descripcion='Compra petita',
            estado='pendiente'  # Aquest no compta
        )
        
        # Verificar que hi ha 3 moviments totals
        total_movimientos = MovimientoCuenta.objects.filter(cuenta=self.cuenta).count()
        self.assertEqual(total_movimientos, 3)
        
        # Verificar moviments validats
        validados = MovimientoCuenta.objects.filter(
            cuenta=self.cuenta, 
            estado='validado'
        ).count()
        self.assertEqual(validados, 2)