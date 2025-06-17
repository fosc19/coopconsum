from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta

from eventos.models import EventoCalendario


class EventoCalendarioModelTest(TestCase):
    """Tests per al model EventoCalendario"""

    def setUp(self):
        # Crear usuari per a relació ForeignKey
        self.user = User.objects.create_user(
            username='testuser',
            email='test@cooperativa.local',
            password='testpass123'
        )

    def test_crear_evento_basic(self):
        """Test creació bàsica d'un esdeveniment"""
        evento = EventoCalendario.objects.create(
            titulo='Reunió Cooperativa',
            descripcion='Reunió mensual dels socis',
            fecha=timezone.now() + timedelta(days=7),
            color='#007bff',
            creado_por=self.user,
            compartir_api=True
        )

        self.assertEqual(evento.titulo, 'Reunió Cooperativa')
        self.assertEqual(evento.color, '#007bff')
        self.assertTrue(evento.compartir_api)
        self.assertEqual(evento.creado_por, self.user)

    def test_str_method(self):
        """Test mètode __str__ del model"""
        evento = EventoCalendario.objects.create(
            titulo='Test Esdeveniment',
            fecha=timezone.now(),
            color='#28a745'
        )

        self.assertEqual(str(evento), 'Test Esdeveniment')

    def test_campos_opcionales(self):
        """Test que els camps opcionals funcionen correctament"""
        evento = EventoCalendario.objects.create(
            titulo='Esdeveniment Mínim',
            fecha=timezone.now()
        )

        # Camps amb valors per defecte
        self.assertEqual(evento.color, '#007bff')  # Color per defecte
        self.assertFalse(evento.compartir_api)  # False per defecte

        # Camps opcionals (poden ser NULL)
        self.assertIsNone(evento.descripcion)
        self.assertIsNone(evento.creado_por)

    def test_campos_requerits(self):
        """Test que els camps requerits no poden estar buits"""
        # Test títol requerit
        evento = EventoCalendario(
            fecha=timezone.now()
            # Falta titulo (requerit)
        )
        with self.assertRaises(Exception):
            evento.full_clean()  # Això sí que valida i llança excepció

        # Test fecha requerida
        with self.assertRaises(Exception):
            EventoCalendario.objects.create(
                titulo='Test'
                # Falta fecha (requerida)
            )

    def test_evento_compartir_api(self):
        """Test funcionalitat compartir API"""
        # Esdeveniment públic (compartir_api=True)
        evento_public = EventoCalendario.objects.create(
            titulo='Esdeveniment Públic',
            fecha=date.today(),
            compartir_api=True
        )

        # Esdeveniment privat (compartir_api=False)
        evento_privat = EventoCalendario.objects.create(
            titulo='Esdeveniment Privat',
            fecha=date.today(),
            compartir_api=False
        )

        # Verificar només esdeveniments públics apareixen en API
        esdeveniments_publics = EventoCalendario.objects.filter(compartir_api=True)
        esdeveniments_privats = EventoCalendario.objects.filter(compartir_api=False)

        self.assertEqual(esdeveniments_publics.count(), 1)
        self.assertEqual(esdeveniments_privats.count(), 1)
        self.assertIn(evento_public, esdeveniments_publics)
        self.assertIn(evento_privat, esdeveniments_privats)

    def test_color_hexadecimal(self):
        """Test validació color hexadecimal"""
        colors_valids = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#6f42c1']
        
        for color in colors_valids:
            evento = EventoCalendario.objects.create(
                titulo=f'Test Color {color}',
                fecha=timezone.now(),
                color=color
            )
            self.assertEqual(evento.color, color)

    def test_ordenacion_per_fecha(self):
        """Test que els esdeveniments s'ordenen per data"""
        avui = date.today()
        
        # Crear esdeveniments en ordre aleatori
        event3 = EventoCalendario.objects.create(
            titulo='Tercer Esdeveniment',
            fecha=avui + timedelta(days=3)
        )
        
        event1 = EventoCalendario.objects.create(
            titulo='Primer Esdeveniment', 
            fecha=avui + timedelta(days=1)
        )
        
        event2 = EventoCalendario.objects.create(
            titulo='Segon Esdeveniment',
            fecha=avui + timedelta(days=2)
        )

        # Obtenir tots els esdeveniments (haurien d'estar ordenats per fecha)
        esdeveniments = list(EventoCalendario.objects.all())
        
        self.assertEqual(esdeveniments[0], event1)
        self.assertEqual(esdeveniments[1], event2)
        self.assertEqual(esdeveniments[2], event3)

    def test_fecha_creacion_automatica(self):
        """Test que fecha_creacion es crea automàticament"""
        abans_crear = timezone.now()
        
        evento = EventoCalendario.objects.create(
            titulo='Test Timestamp',
            fecha=date.today()
        )
        
        despres_crear = timezone.now()

        # Verificar que fecha_creacion està en el rang esperat
        self.assertGreaterEqual(evento.fecha_creacion, abans_crear)
        self.assertLessEqual(evento.fecha_creacion, despres_crear)

    def test_verbose_names(self):
        """Test que els verbose names estan correctament configurats"""
        meta = EventoCalendario._meta
        
        self.assertEqual(meta.verbose_name, "Evento de Calendario")
        self.assertEqual(meta.verbose_name_plural, "Eventos de Calendario")

    def test_relacio_amb_user(self):
        """Test relació ForeignKey amb User"""
        evento = EventoCalendario.objects.create(
            titulo='Test Relació User',
            fecha=timezone.now(),
            creado_por=self.user
        )

        # Test relació directa
        self.assertEqual(evento.creado_por, self.user)
        self.assertEqual(evento.creado_por.username, 'testuser')

        # Test relació inversa
        esdeveniments_user = self.user.eventocalendario_set.all()
        self.assertIn(evento, esdeveniments_user)

    def test_set_null_quan_user_esborrat(self):
        """Test que on_delete=SET_NULL funciona correctament"""
        evento = EventoCalendario.objects.create(
            titulo='Test SET_NULL',
            fecha=timezone.now(),
            creado_por=self.user
        )

        # L'esdeveniment té un usuari assignat
        self.assertEqual(evento.creado_por, self.user)

        # Esborrar l'usuari
        user_id = self.user.id
        self.user.delete()

        # Recarregar esdeveniment de la BD
        evento.refresh_from_db()

        # L'esdeveniment ha de mantenir-se però sense usuari
        self.assertIsNone(evento.creado_por)
        self.assertEqual(evento.titulo, 'Test SET_NULL')

    def test_help_text_compartir_api(self):
        """Test que el help_text de compartir_api està correcte"""
        field = EventoCalendario._meta.get_field('compartir_api')
        expected_help = "Si està marcat, aquest event serà visible a l'API pública per altres cooperatives"
        
        self.assertEqual(field.help_text, expected_help)

    def test_max_length_titulo(self):
        """Test longitud màxima del títol"""
        # Títol de 200 caràcters (màxim permès)
        titulo_llarg = 'T' * 200
        
        evento = EventoCalendario.objects.create(
            titulo=titulo_llarg,
            fecha=timezone.now()
        )
        
        self.assertEqual(len(evento.titulo), 200)
        self.assertEqual(evento.titulo, titulo_llarg)

    def test_filtratge_esdeveniments_futurs(self):
        """Test filtratge d'esdeveniments futurs"""
        avui = date.today()
        ahir = avui - timedelta(days=1)
        dema = avui + timedelta(days=1)

        # Crear esdeveniments en passat, present i futur
        EventoCalendario.objects.create(
            titulo='Esdeveniment Passat',
            fecha=ahir
        )

        evento_avui = EventoCalendario.objects.create(
            titulo='Esdeveniment Avui',
            fecha=avui
        )

        evento_futur = EventoCalendario.objects.create(
            titulo='Esdeveniment Futur',
            fecha=dema
        )

        # Filtrar esdeveniments futurs (inclou avui)
        esdeveniments_futurs = EventoCalendario.objects.filter(fecha__gte=avui)
        
        self.assertEqual(esdeveniments_futurs.count(), 2)
        self.assertIn(evento_avui, esdeveniments_futurs)
        self.assertIn(evento_futur, esdeveniments_futurs)