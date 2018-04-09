import pytest

from django_model_deprecater.tests.sampleapp.models import V1Thing, V2Thing, V3Thing


@pytest.mark.django_db
def test_a_thing():
    x = V1Thing.objects.create(foo='ijij')
    assert 1 == 1