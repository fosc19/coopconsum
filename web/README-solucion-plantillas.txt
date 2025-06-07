Si ves el error "TemplateDoesNotExist: web/home.html" aunque el archivo existe, revisa lo siguiente en tu settings.py:

1. La app 'web' debe estar en INSTALLED_APPS:
INSTALLED_APPS = [
    ...
    'web',
    ...
]

2. La configuración de TEMPLATES debe tener 'APP_DIRS': True y 'DIRS' puede estar vacío o apuntar a un directorio global de plantillas:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                ...
            ],
        },
    },
]

3. La estructura debe ser:
web/
  templates/
    web/
      base.html
      home.html

4. Reinicia el servidor tras cualquier cambio en settings.py.

Con esto, Django debería encontrar correctamente las plantillas de la app web.