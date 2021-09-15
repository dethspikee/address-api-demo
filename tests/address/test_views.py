import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from address.views import AddressesView
from address.models import User, Address


@pytest.mark.django_db
def test_can_get_all_addresses(add_address, add_user):
    factory = APIRequestFactory()
    view = AddressesView.as_view()
    user = add_user(username="John")
    add_address(user, "test grove", "n213dn", "london", "gbr", True)
    add_address(user, "test grove 2", "n213dn", "london", "gbr", False)
    
    request = factory.get("/api/v1.0/addresses/")
    force_authenticate(request, user)
    response = view(request)

    assert Address.objects.count() == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_addresses_view_returns_401_if_not_logged_in():
    factory = APIRequestFactory()
    view = AddressesView.as_view()
    request = factory.get("/api/v1.0/addresses/")
    response = view(request)
    
    assert response.data["detail"].code == "not_authenticated"
    assert response.status_code == 401
