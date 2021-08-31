from django.urls import path, include
from rest_framework.authtoken import views
from drf_yasg.utils import swagger_auto_schema

from .views import AddressesView, AddressDetail

decorated_token_view = swagger_auto_schema(
            method="POST",
            security=[{"Basic": []}],
            operation_description="Generate API Token"
        )(views.obtain_auth_token)


urlpatterns = [
    path('address/<int:pk>/', AddressDetail.as_view()),
    path('addresses/', AddressesView.as_view()),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api_token/', views.obtain_auth_token),
]
