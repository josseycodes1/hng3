from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ['id', 'estimated_gdp', 'last_refreshed_at']
        
        extra_kwargs = {
            'name': {'error_messages': {'blank': 'is required', 'null': 'is required'}},
            'population': {'error_messages': {'null': 'is required'}},
            'currency_code': {'error_messages': {'blank': 'is required', 'null': 'is required'}},
        }

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
