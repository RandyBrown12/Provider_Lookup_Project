from django.db import models

# Create your models here.
import uuid

class City(models.Model):
    city_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city_id = models.DecimalField(unique=True, max_digits=20, decimal_places=0)
    city = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.city


class ZipCode(models.Model):
    zip_code_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zip_code_id = models.DecimalField(unique=True, max_digits=20, decimal_places=0)
    zip_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.zip_code


class Description(models.Model):
    description_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description_id = models.DecimalField(unique=True, max_digits=20, decimal_places=0)
    description_text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.description_text


class LastName(models.Model):
    last_name_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name_id = models.DecimalField(unique=True, max_digits=20, decimal_places=0)
    last_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.last_name


class FirstName(models.Model):
    first_name_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name_id = models.DecimalField(unique=True, max_digits=20, decimal_places=0)
    first_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.first_name


class ProviderRecord(models.Model):
    provider_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    description = models.ForeignKey(Description, to_field='description_id', on_delete=models.CASCADE)
    city = models.ForeignKey(City, to_field='city_id', on_delete=models.CASCADE)
    first_name = models.ForeignKey(FirstName, to_field='first_name_id', on_delete=models.CASCADE)
    last_name = models.ForeignKey(LastName, to_field='last_name_id', on_delete=models.CASCADE)
    zip_code = models.ForeignKey(ZipCode, to_field='zip_code_id', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'city', 'first_name', 'last_name', 'zip_code', 'description'
        )

    def __str__(self):
        return f"{self.first_name.first_name} {self.last_name.last_name}"
