import pytest

from address.models import Address


@pytest.fixture(scope="function")
def add_address():
    def _add_address(user, street, postcode, town, country, current):
        address = Address.objects.create(user=user, street=street,
                postcode=postcode, town=town, country=country, current=current)
        return address
    return _add_address
