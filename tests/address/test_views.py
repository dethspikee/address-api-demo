import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from rest_framework.authtoken.models import Token

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
def test_addressview_returns_401_for_unauth(user_instance):
    """
    Unauthenticated users should see 401.
    """
    req = APIRequestFactory().get("/")
    resp = AddressesView.as_view()(req)
    assert resp.status_code == 401


@pytest.mark.django_db
def test_cannot_send_empty_POST(user_instance):
    """
    Creating new address with empty body should return 400.
    """
    req = APIRequestFactory().post("addresses/")
    force_authenticate(req, user_instance)
    resp = AddressesView.as_view()(req)
    assert resp.status_code == 400


@pytest.mark.django_db
def test_can_send_valid_new_address(user_instance, new_address):
    """
    Creating valid address should return 201.
    """
    test_address = {"street": "teststreet", "postcode": "n12332", "country": "GBR",
            "current": False, "town": "London"}
    req = APIRequestFactory().post("addresses/", test_address, format="json")
    force_authenticate(req, user_instance)
    resp = AddressesView.as_view()(req)


@pytest.mark.django_db
def test_cannot_create_another_address_with_current_true(user_instance, new_address):
    """
    Creating valid address should return 201.
    """
    test_address = {"street": "teststreet", "postcode": "n12332", "country": "GBR",
            "current": True, "town": "London"}
    test_address_2 = {"street": "teststreet2", "postcode": "n54431", "country": "GBR",
            "current": True, "town": "London"}
    client = APIClient()
    token = Token.objects.get(user=user_instance)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    resp = client.post("/api/v1.0/addresses/", test_address, format="json")
    resp = client.post("/api/v1.0/addresses/", test_address_2, format="json")
    assert "Cannot" in resp.data["error"].message
    assert isinstance(resp.data["error"], ValidationError)
    assert resp.status_code == 400
