from django.urls import path
from .views import (RefreshCountriesView, CountryListView, CountryDetailView, CountryDeleteView, StatusView, SummaryImageView)

urlpatterns = [
    path('refresh', RefreshCountriesView.as_view(), name='countries-refresh'),
    path('', CountryListView.as_view(), name='countries-list'),
    path('image', SummaryImageView.as_view(), name='countries-image'),
    path('status', StatusView.as_view(), name='countries-status'),
    path('<str:name>', CountryDetailView.as_view(), name='countries-detail'),
    path('<str:name>/delete', CountryDeleteView.as_view(), name='countries-delete'),  # or keep DELETE on detail route
]
