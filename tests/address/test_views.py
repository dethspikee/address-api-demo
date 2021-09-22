import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from rest_framework.authtoken.models import Token

from address.views import AddressesView, AddressRegister
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
    Creating 2 addresses with "Current" attribute set to "True" should return
    400.
    """
    test_address = {"street": "teststreet", "postcode": "n12332", "country": "GBR",
            "current": True, "town": "London"}
    test_address_2 = {"street": "teststreet2", "postcode": "n54431", "country": "GBR",
            "current": True, "town": "London"}
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + user_instance.auth_token.key)
    resp = client.post("/api/v1.0/addresses/", test_address, format="json")
    resp = client.post("/api/v1.0/addresses/", test_address_2, format="json")
    assert "Cannot" in resp.data["error"].message
    assert isinstance(resp.data["error"], ValidationError)
    assert resp.status_code == 400


@pytest.mark.django_db
def test_address_uniqueness(user_instance, new_address):
    """
    Creating 2 addresses with same attributes should return 400.
    """
    test_address = {"street": "teststreet", "postcode": "n12332", "country": "GBR",
            "current": True, "town": "London"}
    test_address_2 = {"street": "teststreet", "postcode": "n12332", "country": "GBR",
            "current": True, "town": "London"}
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + user_instance.auth_token.key)
    resp = client.post("/api/v1.0/addresses/", test_address, format="json")
    resp = client.post("/api/v1.0/addresses/", test_address_2, format="json")
    error_message = resp.data["error"][0]
    assert "must make a unique set" in error_message
    assert resp.status_code == 400


def test_get_is_not_allowed_for_register_view():
    """
    GET requests to Register View should return 
    'Method not allowed' error with 405 status code.
    """
    req = APIRequestFactory().get("/")
    resp = AddressRegister.as_view()(req)
    message = resp.data["detail"]
    assert "not allowed" in message
    assert resp.status_code == 405
