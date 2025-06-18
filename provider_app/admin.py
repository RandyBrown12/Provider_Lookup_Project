from django.contrib import admin
from .models import MedicalProvider, NPIToTaxonomy, Taxonomy


admin.site.register(MedicalProvider)
admin.site.register(Taxonomy)
admin.site.register(NPIToTaxonomy)
