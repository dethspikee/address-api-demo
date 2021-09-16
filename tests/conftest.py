import pytest

from address.models import Address, User


@pytest.fixture(scope="function")
def add_address():
    def _add_address(user, street, postcode, town, country, current):
        address = Address.objects.create(user=user, street=street,
                postcode=postcode, town=town, country=country, current=current)
        return address
    return _add_address


@pytest.fixture(scope="function")
def add_user():
    def _add_user(username):
        user = User.objects.create(username=username)
        return user
    return _add_user


@pytest.fixture(scope="function")
def user_instance():
    user = User.objects.create(username="John")
    yield user
    user.delete()
