import os.path
import datetime

from django_model_deprecater.local_database_settings import DATABASES
from django_model_deprecater.exceptions import DeprecatedModelException

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
    'models': {
        # This will raise DeprecatedModelException whenever the router detects interaction with the model table
        'django_model_deprecater.tests.sampleapp.V1Thing': DeprecatedModelException,
        # This will throw a DeprecatedWarning with the given string
        'django_model_deprecater.tests.sampleapp.V2Thing': 'This model will soon be replaced by django_model_deprecater.V3Thing'
    },
}

SECRET_KEY = 'asecretkey'