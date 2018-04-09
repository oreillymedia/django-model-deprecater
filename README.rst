Django Model Deprecater README
==============================
.. image:: https://requires.io/enterprise/Safari/django-model-deprecater/requirements.svg?branch=master
     :target: https://requires.io/enterprise/Safari/django-model-deprecater/requirements/?branch=master
     :alt: Requirements Status


.. image:: https://travis-ci.org/oreillymedia/django-model-deprecater.svg?branch=master
    :target: https://travis-ci.org/oreillymedia/django-model-deprecater
    :alt: Build Status


.. image:: https://coveralls.io/repos/github/oreillymedia/django-model-deprecater/badge.svg?branch=master
    :target: https://coveralls.io/github/oreillymedia/django-model-deprecater?branch=master
    :alt: Coverage Status

Django Model Deprecater is a library that aims to make it easier to deprecate models
by raising warnings or errors when a database interaction with the model table is detected.


Use Cases
---------

* You want to easily identify where models are being used and communicate to the team that the model should no longer be supported
* You want to begin to remove the model and want all tests that use the model to fail.


Caveats
-------

* Since the router only knows about database interactions, it will not know about pure python usage of the model yet.

    .. code-block:: python

        x = SomeModel()  # But it would detect the usage once `.save()` or any other database operation is called

Usage
-----


To use this router in Django just add these settings:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_model_deprecater'
    ]

    DATABASE_ROUTERS = ['django_model_deprecater.routers.DeprecatedModelRouter']
    DEPRECATED_MODEL_ROUTER = {
        # Whether to allow migrate if model deprecated
        'check_allow_migrate': False,
        # Whether to allow relations if a model in the auth app is involved
        'check_allow_relation': False,
        'models': {
            # This will raise DeprecatedModelException whenever the router detects interaction with the model table
            'app.V1Thing': DeprecatedModelException,
            # This will throw a DeprecatedWarning with the given string
            'app.V2Thing': 'This model will soon be replaced by app.V3Thing'
        },
    }


Requirements
------------
* Python 2.7, 3.6
* Django 1.8+, 2.0


Setup Locally
-------------

.. code-block:: bash

    $ virtualenv ve --python=python --prompt="(django-model-deprecater)"
    $ pip install -r requirements/base.txt
    $ pip install -r requirements/tests.txt


Run tests
---------

* Note: These tests require the system to either have docker or docker-machine Setup

.. code-block:: bash

    $ tox  # Run the tests for all the environments
    $ tox -e py27-django111  # Run only the tests under Python 2.7 and Django 1.11