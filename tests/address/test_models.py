import pytest

from django.db import IntegrityError
from address.models import Address, User


@pytest.mark.django_db
def test_address_model_raises_integrityerror():
    with pytest.raises(IntegrityError):
        Address.objects.create()


@pytest.mark.django_db
def test_can_create_address_instance():
    user = User.objects.create()
    address = Address(user=user, current=False)
    address.save()
