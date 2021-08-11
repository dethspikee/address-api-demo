from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import AddressView


router = SimpleRouter()
router.register('', AddressView, basename='addresses')


urlpatterns = router.urls
