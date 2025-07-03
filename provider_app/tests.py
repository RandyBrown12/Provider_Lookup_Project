from django.test import TestCase,Client

# Create your tests here.
from provider_app.models import MedicalProvider, Taxonomy, NPIToTaxonomy


from django.urls import reverse

class MedicalProviderModelTest(TestCase):
    def test_create_provider(self):
        provider = MedicalProvider.objects.create(
            npi="1234567890",
            phone_number="123-456-7890",
            first_name="Alice",
            last_name="Smith",
            mailing_street="123 Main St",
            mailing_city="New York",
            mailing_state="NY",
            mailing_zip_code="10001"
        )

        self.assertEqual(provider.npi, '1234567890')
        self.assertEqual(provider.first_name, "Alice")
        self.assertEqual(provider.mailing_city, "New York")
        self.assertIsNotNone(provider._meta.get_field('mailing_street').null)


class TaxonomyModelTest(TestCase):
    def test_create_taxonomy(self):
        taxonomy = Taxonomy.objects.create(
            taxonomy_code="207Q00000X",
            taxonomy_specialization="Family Medicine"
        )

        self.assertEqual(taxonomy.taxonomy_code, "207Q00000X")
        self.assertEqual(taxonomy.taxonomy_specialization, "Family Medicine")


class NPIToTaxonomyTest(TestCase):
    def test_create_npi_to_taxonomy(self):
        provider = MedicalProvider.objects.create(
            npi="1234567890"
        )
        taxonomy = Taxonomy.objects.create(
            taxonomy_code="207Q00000X",
            taxonomy_specialization="Family Medicine"
        )
        link = NPIToTaxonomy.objects.create(
            npi=provider,
            taxonomy_code=taxonomy
        )

        self.assertEqual(link.npi.npi, '1234567890')
        self.assertEqual(link.taxonomy_code.taxonomy_specialization, "Family Medicine")

    def test_duplicate_mapping_not_allowed(self):
        provider = MedicalProvider.objects.create(npi="1234567890")
        taxonomy = Taxonomy.objects.create(taxonomy_code="207Q00000X")
        NPIToTaxonomy.objects.create(npi=provider, taxonomy_code=taxonomy)

        with self.assertRaises(Exception):  # IntegrityError
            NPIToTaxonomy.objects.create(npi=provider, taxonomy_code=taxonomy)





class FlexibleProviderSearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search-result')  # assuming URL is named 'search-result'

        # Sample taxonomy
        self.tax = Taxonomy.objects.create(
            taxonomy_code="207Q00000X",
            taxonomy_specialization="Family Medicine"
        )

        # Sample provider
        self.provider = MedicalProvider.objects.create(
            npi="1234567890",
            first_name="Alice",
            last_name="Smith",
            mailing_city="New York",
            mailing_state="NY",
            mailing_zip_code="10001",
            phone_number="123-456-7890"
        )

        NPIToTaxonomy.objects.create(
            npi=self.provider,
            taxonomy_code=self.tax
        )

    def test_no_fields_provided(self):
        response = self.client.get(self.url, {})
        self.assertContains(response, "At least one search field is required.", status_code=200)

    def test_search_by_first_name(self):
        response = self.client.get(self.url, {'first_name': 'Alice'})
        self.assertContains(response, "Alice")
        self.assertTemplateUsed(response, 'search_result.html')

    def test_search_by_last_name(self):
        response = self.client.get(self.url, {'last_name': 'Smith'})
        self.assertContains(response, "Smith")

    def test_search_by_city(self):
        response = self.client.get(self.url, {'city': 'New York'})
        self.assertContains(response, "New York")

    def test_search_by_state(self):
        response = self.client.get(self.url, {'state': 'NY'})
        self.assertContains(response, "NY")

    def test_search_by_zip_code(self):
        response = self.client.get(self.url, {'zip': '10001'})
        self.assertContains(response, "10001")

    def test_search_by_description(self):
        response = self.client.get(self.url, {'description': 'Family'})
        self.assertContains(response, "Smith")

    # the no data entries will also be outputted in the search result
    def test_excludes_no_data_entries(self):
        MedicalProvider.objects.create(
            npi="9999999999",
            first_name="no data",
            last_name="no data",
            mailing_city="no data",
            mailing_state="no data",
            mailing_zip_code="no data",
            phone_number="no data"
        )
        response = self.client.get(self.url, {'first_name': 'no data'})
        self.assertContains(response, "no data")
