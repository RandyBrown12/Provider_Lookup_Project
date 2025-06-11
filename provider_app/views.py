from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import ProviderRecord
from .serializers import ProviderRecordSerializer

class ProviderSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProviderSearchView(APIView):
    def get(self, request):
        params = request.query_params
        filters = Q()

        first_name = params.get('first_name')
        last_name = params.get('last_name')
        city = params.get('city')
        zip_code = params.get('zip')
        description = params.get('description')

        if not any([first_name, last_name, city, zip_code, description]):
            return render(request, 'search_form.html', {
                'error': "At least one search field is required."
            })

        if first_name:
            filters &= Q(first_name__first_name__icontains=first_name)
        if last_name:
            filters &= Q(last_name__last_name__icontains=last_name)
        if city:
            filters &= Q(city__city__icontains=city)
        if zip_code:
            filters &= Q(zip_code__zip_code__icontains=zip_code)
        if description:
            filters &= Q(description__description_text__icontains=description)

        queryset = ProviderRecord.objects.filter(filters)
        if not queryset.exists():
            return render(request, 'search_form.html', {
                'message': "No results found."
            })

        paginator = ProviderSearchPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProviderRecordSerializer(result_page, many=True)

        return render(request, 'search_form.html', {
            'results':  {'data': serializer.data}
        })

# initial page render
def search_form_view(request):
    return render(request, 'search_form.html')
