# Configuració optimitzada de Gunicorn per CoopConsum
# Resol problemes de worker timeout i optimitza rendiment

# Configuració de workers
workers = 2  # Adequat per 2GB RAM - evita sobrecàrrega
worker_class = "sync"  # Sync és més estable per Django
timeout = 120  # 4x més que el default (30s) per evitar timeouts
keepalive = 2

# Configuració de connexions
bind = "0.0.0.0:8000"
max_requests = 1000  # Reinicia worker després de 1000 requests (evita memory leaks)
max_requests_jitter = 100  # Randomitza restart per evitar sobrecàrrega simultània

# Configuració de logs per debugging
accesslog = "-"  # Log a stdout per Docker
errorlog = "-"   # Error log a stderr per Docker
loglevel = "info"

# Configuració de seguretat
worker_tmp_dir = "/dev/shm"  # Usar RAM per fitxers temporals (més ràpid)

# Configuració de rendiment
preload_app = True  # Precarrega app per millor rendiment
worker_connections = 1000

# Headers de timeout més generosos
graceful_timeout = 30