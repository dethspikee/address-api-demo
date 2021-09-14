import pytest

from django.db import IntegrityError
from address.models import Address, User


class TestAddressModel:

    @pytest.mark.django_db
    def test_address_model_raises_integrityerror(self):
        with pytest.raises(IntegrityError):
            Address.objects.create()


    @pytest.mark.django_db
    def test_can_create_address_instance(self):
        user = User.objects.create()
        address = Address(user=user, current=False)
        address.save()
