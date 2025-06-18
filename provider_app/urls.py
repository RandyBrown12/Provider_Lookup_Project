from django.urls import path
from .views import FlexibleProviderSearchView, search_form_view
urlpatterns = [
    # Route for displaying the initial search form page
    path('search', FlexibleProviderSearchView.as_view(), name='provider-search'),
    # API-like route for performing flexible provider searches via GET params
    path('', search_form_view,name='search_form'),
    # Route for rendering the search results (same view reused with template)
    path("search_result/", FlexibleProviderSearchView.as_view(), name="search-result")
]


