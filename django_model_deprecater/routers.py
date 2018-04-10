# encoding: utf-8
from __future__ import absolute_import, division, unicode_literals

import logging
import warnings

import six
from django.conf import settings
from django.db import models

log = logging.getLogger(__name__)


def make_model_path(model_or_instance):
    if isinstance(model_or_instance, models.Model):
        model = model_or_instance
    else:
        model = model_or_instance._meta.model

    return '{}.{}'.format(model._meta.app_label, model._meta.object_name)


def get_model_path(model, warning_models):
    """Get a warning message for a given model representation

    A model representation may be one of the following:
        - a 'model path' string, like 'starling.SafariTopic'
        - a reference to a Model class
        - a reference to an instance of a Model class
    """
    # use string representations as-is, without further validation
    if isinstance(model, six.string_types):
        return model

    return make_model_path(model)


def warn_or_raise_on_model(model, warning_models):
    model_path = get_model_path(model, warning_models)
    w_or_e = warning_models.get(model_path)

    # short-circuit here, no need for more overhead if it's not needed
    if w_or_e is None:
        return

    # if w_or_e is a string, treat it as a warning
    elif isinstance(w_or_e, six.string_types):
        warnings.warn(w_or_e)

    # if w_or_e is a sub-class of Exception, create and raise it
    elif w_or_e and issubclass(w_or_e, Exception):
        raise w_or_e(model_path)


class DeprecatedModelRouter(object):
    """
    A Django database router that watches for deprecated models and either
    warns or raises an exception.

    This is meant as a development tool, to be used with tests, and likely
    should not be used outside of development or testing environments.
    """
    deprecated_models = settings.DEPRECATED_MODEL_ROUTER['models']
    check_migrate = settings.DEPRECATED_MODEL_ROUTER['check_allow_migrate']
    check_relation = settings.DEPRECATED_MODEL_ROUTER['check_allow_relation']

    def db_for_read(self, model, **hints):
        """Attempts to read auth models go to auth_db."""
        warn_or_raise_on_model(model, self.deprecated_models)
        return 'default'

    def db_for_write(self, model, **hints):
        """Attempts to write auth models go to auth_db."""
        warn_or_raise_on_model(model, self.deprecated_models)
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the auth app is involved."""
        if self.check_relation:
            # these may raise exceptions, we're explicitly not catching them
            warn_or_raise_on_model(obj1, self.deprecated_models)
            warn_or_raise_on_model(obj1, self.deprecated_models)
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrate if model not deprecated"""
        if self.check_migrate and app_label and model_name:
            model_path = '{}.{}'.format(app_label, model_name)
            # this may raise exceptions, we're explicitly not catching it
            warn_or_raise_on_model(model_path, self.deprecated_models)
        return True
