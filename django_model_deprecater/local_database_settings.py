DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'model_deprecater',
        'USER': 'model_deprecater',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '7432',
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 0  # Disable persistent connections
    }
}
