# 📋 Guía para Crear Repositorio Público en GitHub

## 🎯 Objetivo
Crear un repositorio público en GitHub para que otras cooperativas puedan usar nuestro código y contribuir al proyecto.

## 📝 Pasos a Seguir

### 1. **Preparar el Repositorio Local**

#### Limpiar archivos sensibles
Antes de hacer público el repositorio, asegúrate de que estos archivos estén en `.gitignore`:
```
# Configuración sensible - NO subir a producción
coopconsum/settings.py
coopconsum/settings_local.py
coopconsum/settings_production.py
*.env
.env.*
db.sqlite3
media/
```

#### Crear archivos de documentación
- [x] `README.md` - Descripción principal del proyecto
- [x] `API_COOPERATIVAS.md` - Documentación de la API
- [x] `README_API.md` - Estado y ejemplos de la API
- [ ] `INSTALL.md` - Guía de instalación paso a paso
- [ ] `CONTRIBUTING.md` - Cómo contribuir al proyecto
- [ ] `LICENSE` - Licencia del proyecto (recomendado: MIT)

### 2. **Crear el Repositorio en GitHub**

#### Opción A: Desde GitHub Web
1. Ve a [github.com](https://github.com)
2. Haz clic en "New repository"
3. Configura:
   - **Repository name**: `lacivada-cooperativa`
   - **Description**: `Sistema de gestión para cooperativas de consumo - Código abierto`
   - **Visibility**: ✅ Public
   - **Initialize**: ❌ No añadir README (ya lo tienes)
4. Haz clic en "Create repository"

#### Opción B: Desde línea de comandos
```bash
# En tu directorio local
git remote add origin https://github.com/fosc19/lacivada-cooperativa.git
git branch -M main
git push -u origin main
```

### 3. **Configurar el Repositorio**

#### Añadir topics/etiquetas
En GitHub, ve a Settings > General > Topics y añade:
- `cooperativa`
- `django`
- `python`
- `open-source`
- `cooperative`
- `agroecology`
- `api`

#### Configurar README principal
Crear un `README.md` atractivo con:
- Logo de la cooperativa
- Descripción del proyecto
- Capturas de pantalla
- Guía de instalación rápida
- Enlaces a documentación
- Información de contacto

#### Configurar Issues y Discussions
- Habilitar Issues para reportar bugs
- Habilitar Discussions para preguntas de la comunidad
- Crear templates para issues

### 4. **Estructura Recomendada del Repositorio Público**

```
lacivada-cooperativa/
├── README.md                    # Descripción principal
├── LICENSE                      # Licencia MIT
├── INSTALL.md                   # Guía de instalación
├── CONTRIBUTING.md              # Guía para contribuir
├── requirements.txt             # Dependencias Python
├── docker-compose.yml           # Configuración Docker (futuro)
├── .env.example                 # Plantilla de configuración
├── docs/                        # Documentación adicional
│   ├── API_COOPERATIVAS.md
│   ├── README_API.md
│   └── DEPLOYMENT.md
├── scripts/                     # Scripts de instalación
│   ├── install.sh
│   └── setup_database.py
└── [resto del código Django]
```

### 5. **Contenido del README.md Principal**

```markdown
# 🌱 La Civada - Sistema de Gestión para Cooperativas

> Sistema completo de gestión para cooperativas de consumo responsable

## ✨ Características

- 👥 **Gestión de Socios**: Cuentas, movimientos, saldos
- 🛒 **Sistema de Pedidos**: Comandas colectivas y esporádicas  
- 📦 **Gestión de Stock**: Control de inventario
- 🏪 **Catálogo Web**: Página pública con productos
- 🤝 **API Pública**: Compartir datos entre cooperativas
- 📅 **Calendario**: Eventos y actividades

## 🚀 Instalación Rápida

```bash
git clone https://github.com/fosc19/lacivada-cooperativa.git
cd lacivada-cooperativa
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📖 Documentación

- [Guía de Instalación](INSTALL.md)
- [API para Cooperativas](docs/API_COOPERATIVAS.md)
- [Cómo Contribuir](CONTRIBUTING.md)

## 🌐 Demo

- **Web**: https://lacivada.com
- **API**: https://lacivada.com/api/

## 🤝 Comunidad

¿Tienes una cooperativa? ¡Únete a la red!
- Email: cooperatives@lacivada.com
- Issues: Para reportar bugs
- Discussions: Para preguntas y ideas

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)
```

### 6. **Actualizar la Página Web**

Una vez creado el repositorio, actualizar el enlace en:
- `web/templates/web/cooperatives.html` línea con `href="#"`
- Cambiar por: `href="https://github.com/fosc19/lacivada-cooperativa"`

### 7. **Promoción del Proyecto**

#### En redes sociales
- Anunciar en redes de la cooperativa
- Compartir en grupos de cooperativas
- Contactar con otras cooperativas conocidas

#### En comunidades técnicas
- Publicar en foros de Django
- Compartir en comunidades de código abierto
- Presentar en eventos de cooperativismo

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Archivos sensibles en `.gitignore`
- [ ] README.md atractivo creado
- [ ] Documentación completa
- [ ] Enlaces actualizados en la web
- [ ] Topics/etiquetas configuradas
- [ ] Issues y Discussions habilitadas
- [ ] Licencia MIT añadida

## 🎉 ¡Listo!

Una vez completados estos pasos, tu proyecto estará disponible públicamente y otras cooperativas podrán:
- Descargar y usar el código
- Contribuir con mejoras
- Reportar bugs
- Hacer preguntas
- Crear una red de cooperativas colaborativas

---

**¿Necesitas ayuda?** Contacta con el equipo técnico de La Civada.