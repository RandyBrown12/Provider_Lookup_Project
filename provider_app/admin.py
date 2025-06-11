from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ProviderRecord, City, ZipCode, FirstName, LastName, Description

admin.site.register(ProviderRecord)
admin.site.register(City)
admin.site.register(ZipCode)
admin.site.register(FirstName)
admin.site.register(LastName)
admin.site.register(Description)
