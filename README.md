# 🤝 CoopConsum - Sistema de Gestión para Cooperativas

Sistema completo de gestión para cooperativas de consumo responsable, desarrollado con Django. Incluye gestión de socios, pedidos, proveedores, productos y una API pública para compartir información entre cooperativas.

## ✨ Características

- 👥 **Gestión de Socios**: Registro, perfiles y administración de miembros
- 📦 **Sistema de Pedidos**: Comandas colectivas y gestión de pedidos
- 🏪 **Gestión de Proveedores**: Catálogo de proveedores locales y ecológicos
- 🛒 **Catálogo de Productos**: Organización por categorías con precios
- 🌐 **Web Pública**: Sitio web con información y catálogo público
- 🔗 **API REST**: Intercambio de datos entre cooperativas
- 📱 **Responsive**: Diseño adaptado a móviles y tablets

## 🚀 Instalación Rápida

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/coopconsum.git
cd coopconsum
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar settings**
```bash
# Copiar el archivo de configuración de ejemplo
cp coopconsum/settings_example.py coopconsum/settings.py
# Editar settings.py con tus configuraciones específicas
```

5. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

¡Ya puedes acceder a http://localhost:8000!

## 📚 Documentación

### Estructura del Proyecto

```
coopconsum/
├── socios/          # Gestión de socios y usuarios
├── pedidos/         # Sistema de pedidos y comandas
├── web/             # Sitio web público
├── api/             # API REST para cooperativas
├── templates/       # Plantillas HTML
├── static/          # Archivos CSS, JS, imágenes
├── media/           # Archivos subidos por usuarios
└── coopconsum/      # Configuración principal
```

### API Pública

La API permite a otras cooperativas acceder a información pública:

- **Proveedores**: `GET /api/proveedores/`
- **Productos**: `GET /api/productos/`
- **Categorías**: `GET /api/categorias/`

Ejemplo de uso:
```bash
# Obtener lista de proveedores
curl http://localhost:8000/api/proveedores/

# Buscar productos ecológicos
curl http://localhost:8000/api/productos/?search=ecològic
```

## 🛠️ Configuración

### Variables de Entorno

Crea un archivo `.env` o configura directamente en `settings.py`:

```python
SECRET_KEY = 'tu-clave-secreta-aqui'
DEBUG = False  # Para producción
ALLOWED_HOSTS = ['tu-dominio.com']

# Base de datos (ejemplo PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'coopconsum_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### CORS para API

Para permitir acceso desde otros dominios:

```python
CORS_ALLOWED_ORIGINS = [
    "https://tu-cooperativa.com",
    "https://otra-cooperativa.org",
]
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🌱 Filosofía del Proyecto

Este sistema nace de la necesidad de las cooperativas de consumo de tener herramientas digitales que respeten sus valores:

- **Código Abierto**: Transparencia total y posibilidad de adaptación
- **Cooperación**: API para compartir información entre cooperativas
- **Sostenibilidad**: Enfoque en productos locales y ecológicos
- **Comunidad**: Desarrollado por y para cooperativas

## 📞 Soporte

- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/coopconsum/wiki)
- **Issues**: [Reportar problemas](https://github.com/tu-usuario/coopconsum/issues)
- **Discusiones**: [Foro de la comunidad](https://github.com/tu-usuario/coopconsum/discussions)

## 🏆 Cooperativas que lo usan

- La Civada (Barcelona) - Cooperativa pionera en el desarrollo

¿Tu cooperativa usa CoopConsum? ¡Añádete a la lista!

---

**Desarrollado con ❤️ por la comunidad cooperativa**