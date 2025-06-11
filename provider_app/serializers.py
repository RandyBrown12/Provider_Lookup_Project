# provider_app/serializers.py
from rest_framework import serializers
from .models import ProviderRecord

class ProviderRecordSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='first_name.first_name')
    last_name = serializers.CharField(source='last_name.last_name')
    description = serializers.CharField(source='description.description_text')
    city = serializers.CharField(source='city.city')
    zip_code = serializers.CharField(source='zip_code.zip_code')
    phone = serializers.CharField(default='')  # Add if you have a phone field or remove this line

    class Meta:
        model = ProviderRecord
        fields = ['first_name', 'last_name', 'description', 'city', 'zip_code', 'phone']
