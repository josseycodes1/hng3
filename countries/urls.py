from django.urls import path
from .views import (Test500ErrorView, RefreshCountriesView, CountryListView, CountryDetailView, SummaryImageView, DebugImageView)

urlpatterns = [
    path('refresh', RefreshCountriesView.as_view(), name='countries-refresh'),
    path('', CountryListView.as_view(), name='countries-list'),
    path('image', SummaryImageView.as_view(), name='countries-image'),
    path('<str:name>', CountryDetailView.as_view(), name='countries-detail'),
    path('debug-image', DebugImageView.as_view(), name='debug-image'),
    path('test-500', Test500ErrorView.as_view(), name='test-500'),
]
