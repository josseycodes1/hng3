from django.shortcuts import render, get_object_or_404
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.http import FileResponse
import io
import random
import logging
from datetime import datetime, timezone
import requests
from .models import Country
from .serializers import CountrySerializer
from .utils import generate_summary_image
import requests
from PIL import Image, ImageDraw
from .models import Country
from .serializers import CountrySerializer
from .utils import generate_summary_image
from rest_framework import status

logger = logging.getLogger(__name__)

RESTCOUNTRIES_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_URL = "https://open.er-api.com/v6/latest/USD"


def fetch_external(url, timeout=10):
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        logger.exception("External API fetch failed for %s", url)
        raise


class RefreshCountriesView(APIView):
    """
    POST /countries/refresh
    Fetch countries and exchange rates, then upsert to DB and generate summary image.
    """
    def post(self, request):
        # Fetch external data
        try:
            countries_data = fetch_external(RESTCOUNTRIES_URL)
        except Exception:
            return Response(
                {"error": "External data source unavailable", "details": "Could not fetch data from REST Countries"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            rates_data = fetch_external(EXCHANGE_URL)
            rates_map = rates_data.get("rates", {}) or {}
        except Exception:
            return Response(
                {"error": "External data source unavailable", "details": "Could not fetch data from Exchange Rates"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Process inside transaction: rollback on any exception
        try:
            with transaction.atomic():
                for c in countries_data:
                    name = c.get("name")
                    capital = c.get("capital")
                    region = c.get("region")
                    population = c.get("population") or 0
                    flag_url = c.get("flag")
                    currencies = c.get("currencies") or []

                    # currency handling
                    if currencies and isinstance(currencies, list) and len(currencies) > 0:
                        cur0 = currencies[0]
                        currency_code = cur0.get("code") if isinstance(cur0, dict) else None
                    else:
                        currency_code = None

                    exchange_rate = None
                    estimated_gdp = 0.0
                    if currency_code:
                        exchange_rate = rates_map.get(currency_code)
                    if exchange_rate:
                        multiplier = random.uniform(1000, 2000)
                        try:
                            estimated_gdp = float(population) * multiplier / float(exchange_rate)
                        except Exception:
                            estimated_gdp = 0.0
                    else:
                        exchange_rate = None
                        estimated_gdp = 0.0

                    # Case-insensitive upsert: try to find existing by name (iexact), else create
                    existing = Country.objects.filter(name__iexact=name).first()
                    if existing:
                        existing.name = name
                        existing.capital = capital
                        existing.region = region
                        existing.population = population
                        existing.currency_code = currency_code
                        existing.exchange_rate = float(exchange_rate) if exchange_rate is not None else None
                        existing.estimated_gdp = float(estimated_gdp)
                        existing.flag_url = flag_url
                        existing.save()
                    else:
                        Country.objects.create(
                            name=name,
                            capital=capital,
                            region=region,
                            population=population,
                            currency_code=currency_code,
                            exchange_rate=float(exchange_rate) if exchange_rate is not None else None,
                            estimated_gdp=float(estimated_gdp),
                            flag_url=flag_url,
                        )
            # commit happened
        except Exception:
            logger.exception("Failed during DB upsert in refresh")
            # transaction.atomic() will rollback automatically
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # generate the summary image (outside the transaction)
        try:
            img_path = generate_summary_image()  # should save to cache/summary.png by default
        except Exception:
            logger.exception("Failed to generate summary image")

        total = Country.objects.count()
        last = Country.objects.order_by("-last_refreshed_at").first()
        return Response(
            {
                "message": "Refreshed",
                "total_countries": total,
                "last_refreshed_at": last.last_refreshed_at.isoformat() if last else None,
            }
        )


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["estimated_gdp", "population", "name"]

    def get_queryset(self):
        qs = super().get_queryset()
        region = self.request.query_params.get("region")
        currency = self.request.query_params.get("currency")
        sort = self.request.query_params.get("sort")
        if region:
            qs = qs.filter(region__iexact=region)
        if currency:
            qs = qs.filter(currency_code__iexact=currency)
        if sort == "gdp_desc":
            qs = qs.order_by("-estimated_gdp")
        elif sort == "gdp_asc":
            qs = qs.order_by("estimated_gdp")
        return qs


class CountryDetailView(generics.RetrieveAPIView):
    lookup_field = "name"
    lookup_url_kwarg = "name"
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_object(self):
        name = self.kwargs["name"]
        obj = get_object_or_404(Country, name__iexact=name)
        return obj


class CountryDeleteView(APIView):
    def delete(self, request, name):
        obj = Country.objects.filter(name__iexact=name).first()
        if not obj:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StatusView(APIView):
    def get(self, request):
        total = Country.objects.count()
        last = Country.objects.order_by("-last_refreshed_at").first()
        return Response(
            {"total_countries": total, "last_refreshed_at": last.last_refreshed_at.isoformat() if last else None}
        )


class SummaryImageView(APIView):
    def get(self, request):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "summary.png")
        if not os.path.exists(path):
            return Response({"error": "Summary image not found"}, status=status.HTTP_404_NOT_FOUND)
        return FileResponse(open(path, "rb"), content_type="image/png")
