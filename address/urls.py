from django.urls import path, include

from .views import AddressView


urlpatterns = [
    path('', AddressView.as_view()),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
