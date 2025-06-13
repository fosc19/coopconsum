# coopconsum/settings.py
# Aquest fitxer importa la configuració base i la pot sobrescriure si cal

from .settings_base import *

# Configuració específica per logout
# PROBLEMA IDENTIFICAT: settings_base.py tenia LOGOUT_REDIRECT_URL = '/accounts/login/'
# Això feia que:
# 1. Admin logout redirigís a /accounts/login/ 
# 2. Com que l'usuari encara pot estar autenticat, el login el redirigeix a /socios/ (LOGIN_REDIRECT_URL)
# 3. Això crea confusió perquè sembla que no ha sortit del sistema

# SOLUCIÓ: Configurar LOGOUT_REDIRECT_URL per redirigir a la web pública
LOGOUT_REDIRECT_URL = '/'  # Redirigir a la pàgina d'inici (web pública) després del logout

# Per admin també funciona perfectament amb aquesta configuració
# L'usuari veurà clarament que ha sortit del sistema perquè anirà a la web pública