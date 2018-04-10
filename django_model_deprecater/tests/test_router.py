import pytest

from django_model_deprecater.tests.sampleapp.models import V1Thing


@pytest.mark.django_db
def test_a_thing():
    V1Thing.objects.create(foo='ijij')
    assert 1 == 1
