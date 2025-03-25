# Gunicorn configuration

# Number of worker processes
workers = 4

# Bind to all available network interfaces
bind = "0.0.0.0:8000"

# Logging
errorlog = '-'  # stderr
accesslog = '-'  # stdout
loglevel = 'info'

# Worker class (sync is default, can use gevent for async)
worker_class = 'sync'

# Timeout settings
timeout = 120
keepalive = 5