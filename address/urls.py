from django.urls import path, include
from rest_framework.authtoken import views

from .views import AddressesView, AddressDetail


urlpatterns = [
    path('address/<int:pk>/', AddressDetail.as_view()),
    path('addresses/', AddressesView.as_view()),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api_token/', views.obtain_auth_token),
]
