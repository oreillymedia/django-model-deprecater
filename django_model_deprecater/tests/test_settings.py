from django_model_deprecater.local_database_settings import DATABASES  # noqa: F401,E501 isort:skip

INSTALLED_APPS = [
    'django_model_deprecater',
    'django_model_deprecater.tests.sampleapp'
]


DATABASE_ROUTERS = ['django_model_deprecater.routers.DeprecatedModelRouter']
DEPRECATED_MODEL_ROUTER = {
    # Whether to allow migrate if model deprecated
    'check_allow_migrate': False,
    # Whether to allow relations if a model in the auth app is involved
    'check_allow_relation': False,
    'models': {},
}

SECRET_KEY = 'asecretkey'
