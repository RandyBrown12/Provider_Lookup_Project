from django.urls import path
from .views import ProviderSearchView, search_form_view

urlpatterns = [
    path('search', ProviderSearchView.as_view(), name='provider-search'),
    path('search-form/', search_form_view, name='search_form'),
    path('', search_form_view),
]


