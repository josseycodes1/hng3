from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ['id', 'estimated_gdp', 'last_refreshed_at']

    def validate(self, data):
        errors = {}
        if not data.get('name'):
            errors['name'] = 'is required'
        if 'population' in data and (data.get('population') is None):
            errors['population'] = 'is required'
       
        if data.get('currency_code') in ("", None):
            errors['currency_code'] = 'is required'
        if errors:
            raise serializers.ValidationError(errors)
        return data
