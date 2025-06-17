# provider_app/models.py
from django.db import models

class MedicalProvider(models.Model):
    """
    Represents a medical provider's basic contact and location information.

    Fields:
        id (int): Primary key
        npi (Decimal): National Provider Identifier (unique, 10-digit)
        phone_number (str): Contact number
        first_name (str): Provider's first name
        last_name (str): Provider's last name
        mailing_street (str): Street address for mailing
        mailing_city (str): City of mailing address
        mailing_state (str): State of mailing address
        mailing_zip_code (str): ZIP code for mailing address
    """
    id = models.AutoField(primary_key=True)
    npi = models.DecimalField(max_digits=10, decimal_places=0, unique=True)
    phone_number = models.CharField(max_length=64,blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    mailing_street = models.CharField(max_length=224, blank=True, null=True)
    mailing_city = models.CharField(max_length=64, blank=True, null=True)
    mailing_state = models.CharField(max_length=64, blank=True, null=True)
    mailing_zip_code = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = "medical_providers"

class Taxonomy(models.Model):
    """
    Represents a taxonomy code and its corresponding specialization.

    Fields:
        id (int): Primary key
        taxonomy_code (str): Unique taxonomy identifier (e.g., "207Q00000X")
        taxonomy_specialization (str): Human-readable medical specialization
    """
    id = models.AutoField(primary_key=True)
    taxonomy_code = models.CharField(max_length=10, unique=True)
    taxonomy_specialization = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "taxonomies"

class NPIToTaxonomy(models.Model):
    """
    Maps a medical provider's NPI to one or more taxonomy codes.

    Fields:
        id (int): Primary key
        npi (ForeignKey): Reference to a MedicalProvider
        taxonomy_code (ForeignKey): Reference to a Taxonomy entry

    Constraints:
        unique_together: Ensures one provider is not mapped multiple times
        to the same taxonomy.
    """
    id = models.AutoField(primary_key=True)
    npi = models.ForeignKey(MedicalProvider, to_field='npi', on_delete=models.CASCADE, db_column='npi')
    taxonomy_code = models.ForeignKey(Taxonomy, to_field='taxonomy_code', on_delete=models.CASCADE, db_column='taxonomy_code')

    class Meta:
        db_table = "npi_to_taxonomies"
        unique_together = (('npi', 'taxonomy_code'),)
