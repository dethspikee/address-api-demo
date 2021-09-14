import pytest

from django.db import IntegrityError
from address.models import Address


@pytest.mark.django_db
def test_address_model():
    with pytest.raises(IntegrityError):
        Address.objects.create()
