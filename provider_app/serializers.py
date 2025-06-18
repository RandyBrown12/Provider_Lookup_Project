from rest_framework import serializers
from .models import MedicalProvider, Taxonomy, NPIToTaxonomy

class ProviderRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for MedicalProvider instances with extended fields for display.

    Includes:
    - Renamed fields (e.g., 'mailing_city' → 'city')
    - Computed fields for taxonomy code, specialization, and primary address
    """
    city = serializers.CharField(source='mailing_city')
    state = serializers.CharField(source='mailing_state')
    zip_code = serializers.CharField(source='mailing_zip_code')
    phone = serializers.CharField(source='phone_number')
    taxonomy = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    primary_address = serializers.SerializerMethodField()

    class Meta:
        model = MedicalProvider
        fields = ['first_name', 'last_name', 'city', 'state', 'zip_code', 'phone', 'taxonomy', 'description','primary_address']

    def get_taxonomy(self, obj):
        """
        Retrieve taxonomy code for the provider.

        Args:
            obj (MedicalProvider): The provider instance.

        Returns:
            str: Taxonomy code (e.g., "207Q00000X") or 'N/A' if not found.
        """
        entry = NPIToTaxonomy.objects.filter(npi=obj).select_related('taxonomy_code').first()
        return entry.taxonomy_code.taxonomy_code if entry else 'N/A'

    def get_description(self, obj):
        """
        Retrieve taxonomy specialization description.

        Args:
            obj (MedicalProvider): The provider instance.

        Returns:
            str: Human-readable specialization (e.g., "Family Medicine") or 'N/A'.
        """
        entry = NPIToTaxonomy.objects.filter(npi=obj).select_related('taxonomy_code').first()
        return entry.taxonomy_code.taxonomy_specialization if entry else 'N/A'
    def get_primary_address(self, obj):
        """
        Concatenate provider's primary mailing address into one string.

        Args:
            obj (MedicalProvider): The provider instance.

        Returns:
            str: Full address in format "Street, City, State, ZIP".
        """
        components = [
            obj.mailing_street,
            obj.mailing_city,
            obj.mailing_state,
            obj.mailing_zip_code
        ]
        return ', '.join(filter(None, components))

