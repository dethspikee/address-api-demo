import pytest
from mixer.backend.django import mixer

from address.models import Address, User


@pytest.fixture(scope="function")
def add_address():
    """
    Factory as fixture for adding new addresses.
    """
    def _add_address(user, street, postcode, town, country, current):
        address = Address.objects.create(user=user, street=street,
                postcode=postcode, town=town, country=country, current=current)
        return address
    return _add_address


@pytest.fixture(scope="function")
def add_user():
    """
    Factory as fixture for adding new users.
    """
    def _add_user(username):
        user = User.objects.create(username=username)
        return user
    return _add_user


@pytest.fixture(scope="function")
def user_instance():
    """
    Create new user using mixer.
    """
    user = mixer.blend(User)
    yield user
    user.delete()
