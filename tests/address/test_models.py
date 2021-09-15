import pytest

from django.db import IntegrityError
from address.models import Address, User


@pytest.mark.django_db
class TestAddressModel:

    def test_address_model_raises_integrityerror_if_missing_params(self):
        with pytest.raises(IntegrityError):
            Address.objects.create()

    def test_can_create_address_instance(self, add_user):
        user = add_user(username="John")
        address_info = {
            "street": "Test street",
            "postcode": "N123FG",
            "town": "London",
            "country": "GBR",
            "current": False,
        }
        address = Address(user=user, **address_info)
        address.save()

        assert address.user == user
        assert address.street == address_info["street"]
        assert address.postcode == address_info["postcode"]
        assert address.town == address_info["town"]
        assert address.country == address_info["country"]
        assert address.current == address_info["current"]
