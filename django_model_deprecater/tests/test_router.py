import mock
import pytest

from django_model_deprecater.routers import (
    DeprecatedModelRouter, get_model_path, make_model_path,
    warn_or_raise_on_model,
)
from django_model_deprecater.tests.sampleapp.models import V1Thing, V2Thing

BASE_MOCK_PATH = 'django_model_deprecater.routers'


@pytest.fixture()
def mock_make_model_path():
    mock_path = '{}.make_model_path'.format(BASE_MOCK_PATH)
    with mock.patch(mock_path, autospec=True) as m:
        yield m


@pytest.fixture()
def mock_warn():
    mock_make_model_path = '{}.warnings.warn'.format(BASE_MOCK_PATH)
    with mock.patch(mock_make_model_path, autospec=True) as m:
        yield m


def test_make_model_path_returns_path_for_model():
    thing = V1Thing
    expected = 'sampleapp.V1Thing'
    assert make_model_path(thing) == expected


def test_make_model_path_returns_path_for_instance():
    thing = V1Thing(foo='bar')
    expected = 'sampleapp.V1Thing'
    assert make_model_path(thing) == expected


def test_get_model_path_returns_model_when_argument_is_str():
    expected = 'sampleapp.V1Thing'
    assert get_model_path(expected) == expected


def test_get_model_path_calls_make_model_if_not_str(mock_make_model_path):
    thing = V1Thing(foo='bar')
    assert get_model_path(thing) == mock_make_model_path.return_value


class TestWarnOrRaiseOnModel(object):
    def test_does_not_warn_if_model_not_listed(self, mock_warn):
        warn_or_raise_on_model(V1Thing, {'sampleapp.V2Thing': "A Warning"})
        assert mock_warn.called is False

    def test_warns_if_model_listed(self, mock_warn):
        expected_warning_msg = "A Warning"
        warn_or_raise_on_model(V1Thing, {'sampleapp.V1Thing': "A Warning"})
        mock_warn.assert_called_once_with(
            expected_warning_msg,
            category=DeprecationWarning)

    def test_raises_if_model_listed(self, mock_warn):
        with pytest.raises(ValueError):
            warn_or_raise_on_model(V1Thing, {'sampleapp.V1Thing': ValueError})

    def test_does_nothing_if_not_stiring_or_exception(self, mock_warn):
        warn_or_raise_on_model(V1Thing, {'sampleapp.V1Thing': V2Thing})
        assert mock_warn.called is False


class TestDeprecatedModelRouter(object):
    def setup_method(self):
        w_o_r_path = '{}.warn_or_raise_on_model'.format(BASE_MOCK_PATH)
        self.w_o_r_patcher = mock.patch(w_o_r_path, autospec=True)
        self.mock_w_o_r = self.w_o_r_patcher.start()
        self.router = DeprecatedModelRouter()

    def teardown_method(self):
        self.w_o_r_patcher.stop()

    def test_db_for_read_calls_w_or_r_and_returns_default_db(self):
        db = self.router.db_for_read(V1Thing)

        self.mock_w_o_r.assert_called_once_with(
            V1Thing,
            self.router.deprecated_models)
        assert db == 'default'

    def test_db_for_write_calls_w_or_r_and_returns_default_db(self):
        db = self.router.db_for_write(V1Thing)

        self.mock_w_o_r.assert_called_once_with(
            V1Thing,
            self.router.deprecated_models)
        assert db == 'default'

    def test_allow_relation_does_not_calls_w_or_r_for_models(self):
        thing1 = V1Thing(foo="bar")
        thing2 = V2Thing(bar="baz")
        allow = self.router.allow_relation(thing1, thing2)

        assert allow is True

    def test_allow_relation_calls_w_or_r_for_models_and_returns_true(self):
        self.router.check_relation = True
        thing1 = V1Thing(foo="bar")
        thing2 = V2Thing(bar="baz")
        allow = self.router.allow_relation(thing1, thing2)

        self.mock_w_o_r.assert_has_calls(
            [mock.call(thing1, self.router.deprecated_models),
             mock.call(thing2, self.router.deprecated_models)]
        )
        assert allow is True

    def test_allow_migrate_does_not_call_w_or_r_if_not_checking(self):
        allow = self.router.allow_migrate('default', 'someapp', 'V1Thing')

        assert allow is True
        assert self.mock_w_o_r.called is False

    def test_allow_migrate_calls_w_or_r_if_checking(self):
        self.router.check_migrate = True
        expected_model_path = 'someapp.V1Thing'
        app_label, model_name = expected_model_path.split('.')
        allow = self.router.allow_migrate('default', app_label, model_name)

        assert allow is True
        self.mock_w_o_r.assert_called_once_with(
            expected_model_path, self.router.deprecated_models
        )
