import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from address.views import AddressesView
from address.models import User, Address


@pytest.mark.django_db
def test_can_get_all_addresses(add_address):
    factory = APIRequestFactory()
    view = AddressesView.as_view()
    user = User.objects.create(username="John")
    add_address(user, "test grove", "n213dn", "london", "gbr", True)
    add_address(user, "test grove 2", "n213dn", "london", "gbr", False)
    
    request = factory.get("/api/v1.0/addresses/")
    force_authenticate(request, user)
    response = view(request)

    assert Address.objects.count() == 2
    assert response.status_code == 200
