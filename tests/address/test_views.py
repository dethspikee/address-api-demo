import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from address.views import AddressesView
from address.models import User, Address


@pytest.mark.django_db
def test_auth_can_access_view_page(add_address, user_instance):
    """
    Authenticated users should be able to access view listing
    all of their addresses.
    """
    req = APIRequestFactory().get("/")
    force_authenticate(req, user_instance)
    resp = AddressesView.as_view()(req)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_addresses_view_returns_401_if_not_logged_in():
    factory = APIRequestFactory()
    view = AddressesView.as_view()
    request = factory.get("/api/v1.0/addresses/")
    response = view(request)
    
    assert response.data["detail"].code == "not_authenticated"
    assert response.status_code == 401
