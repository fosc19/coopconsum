Estructura recomendada para separar claramente la web pública y la intranet en tu proyecto Django:

coopconsum/                # Proyecto Django principal
├── web/                   # App para la web pública (escaparate/tienda)
│   ├── templates/
│   │   └── web/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── quienes_somos.html
│   │       ├── productores.html
│   │       ├── productor_detalle.html
│   │       ├── productos.html
│   │       ├── producto_detalle.html
│   │       ├── contacto.html
│   │       └── ... (otras secciones públicas)
│   ├── static/
│   │   └── web/
│   │       ├── css/
│   │       │   └── custom.css
│   │       ├── img/
│   │       └── js/
│   ├── views.py
│   ├── urls.py
│   └── ... (otros archivos de la app web)
│
├── socios/                # App para la intranet (panel de socios, gestión interna)
│   ├── templates/
│   │   └── socios/
│   │       └── ... (plantillas de la intranet)
│   ├── static/
│   │   └── socios/
│   ├── views.py
│   ├── urls.py
│   └── ... (otros archivos de la app intranet)
│
├── pedidos/               # App para gestión de pedidos (intranet)
│   └── ...
├── productos/             # App para productos (intranet)
│   └── ...
├── stock/                 # App para stock (intranet)
│   └── ...
├── templates/             # (opcional, para plantillas globales)
│   └── base.html
├── static/                # (opcional, para recursos globales)
│   └── ...
├── manage.py
└── ...

Notas:
- web/ es la app para la web pública (escaparate, tienda, información, contacto, etc).
- socios/, pedidos/, productos/, stock/ son apps para la intranet (gestión interna, panel de socios, etc).
- Cada app tiene sus propias plantillas y recursos estáticos.
- Puedes tener una base.html global o una para cada entorno (web/base.html e intranet/base.html).
- Las urls públicas se definen en web/urls.py y se incluyen en el urls.py principal.
- Las urls de la intranet se definen en las apps correspondientes y se incluyen bajo /socios/, /pedidos/, etc.

¿Quieres que te cree un ejemplo de base.html y home.html para la web pública con Bootstrap 5 y bloques listos para contenido?