from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import MedicalProvider, Taxonomy, NPIToTaxonomy

from .serializers import ProviderRecordSerializer
from django.shortcuts import render
from .pagination import StandardResultsPagination



class FlexibleProviderSearchView(APIView):
    """
    Handle flexible search for medical providers based on various query parameters.

    Supports search by:
    - First name
    - Last name
    - City
    - State
    - Zip code
    - Taxonomy specialization description

    Renders the search result template with valid provider matches.

    Example usage:
        GET /providers?first_name=John&city=New+York

    Template:
        - search_form.html (for errors or no input)
        - search_result.html (for valid results)
    """

    def get(self, request):
        """
        Process GET request with optional query parameters and return search results.

        Query Parameters:
            first_name (str): Provider's first name (optional)
            last_name (str): Provider's last name (optional)
            city (str): Mailing city (optional)
            state (str): Mailing state (optional)
            zip_code (str): Mailing ZIP code (optional)
            description (str): Taxonomy specialization description (optional)

        Returns:
            HttpResponse: Rendered HTML page with search results or error message
        """


        # Get all query params
        first = request.query_params.get('first_name', '').strip()
        last = request.query_params.get('last_name', '').strip()
        city = request.query_params.get('city', '').strip()
        state = request.query_params.get('state', '').strip()
        zip_code = request.query_params.get('zip_code', '').strip()
        description = request.query_params.get('description', '').strip()

        # At least one field is required
        if not any([first, last, city, zip_code, description]):
            return render(request, 'search_form.html', {
                'error': "At least one search field is required."
            })

        # Base queryset
        queryset = MedicalProvider.objects.all()

        if first:
            queryset = queryset.filter(first_name__iexact=first)
        if last:
            queryset = queryset.filter(last_name__iexact=last)
        if city:
            queryset = queryset.filter(mailing_city__iexact=city)
        if zip_code:
            queryset = queryset.filter(mailing_zip_code__iexact=zip_code)
        if state:
            queryset = queryset.filter(mailing_state__iexact=state)

        # If taxonomy description provided
        if description:
            #return the taxonomy that matches the description
            matching_taxonomies = Taxonomy.objects.filter(
                taxonomy_specialization__istartswith=description
            )
            matching_npis =  NPIToTaxonomy.objects.filter(
                taxonomy_code__in=matching_taxonomies
            ).values_list('npi', flat=True)
            queryset = queryset.filter(npi__in=matching_npis)

        queryset = queryset.exclude(first_name__iexact='no data') \
                           .exclude(last_name__iexact='no data') \
                           .exclude(phone_number__iexact='no data') \
                           .exclude(mailing_city__iexact='no data') \
                           .exclude(mailing_state__iexact='no data') \
                           .exclude(mailing_zip_code__iexact='no data')

        queryset = queryset.distinct()

        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProviderRecordSerializer(page, many=True)



        return render(request, 'search_result.html', {
            'results': {'data': serializer.data,
                        'count': paginator.page.paginator.count,
                        'has_next': paginator.page.has_next(),
                        'has_previous': paginator.page.has_previous(),
                        'current_page': paginator.page.number,
                        'next_page_number': paginator.page.next_page_number() if paginator.page.has_next() else None,
                        'previous_page_number': paginator.page.previous_page_number() if paginator.page.has_previous() else None,
}
        })


def search_form_view(request):
    """
    Render the initial search form page.

    Returns:
        HttpResponse: The rendered search_form.html page
    """
    return render(request, 'search_form.html')