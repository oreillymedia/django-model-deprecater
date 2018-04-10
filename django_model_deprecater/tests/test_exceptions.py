from django_model_deprecater.exceptions import DeprecatedModelException


def test_exception_message_contains_base_message():
    e = DeprecatedModelException("Foo")
    expected_msg = e.base_msg.format("Foo")
    assert expected_msg == str(e)


def test_exception_message_contains_extra_message():
    e = DeprecatedModelException("Foo", extra_msg="Bar")
    assert "Bar" in str(e)
