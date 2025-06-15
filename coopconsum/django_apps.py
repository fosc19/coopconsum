"""
Configuracions personalitzades per apps de Django
per controlar l'ordre al menú admin
"""
from django.contrib.auth.apps import AuthConfig


class CustomAuthConfig(AuthConfig):
    verbose_name = "0. Autenticació i autorització"