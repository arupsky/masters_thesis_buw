from django.db import models
from model_utils.models import SoftDeletableModel, SoftDeletableManager, TimeStampedModel


# Create your models here.

class Auditable(SoftDeletableModel, TimeStampedModel):
    objects = models.Manager()
    soft_manager = SoftDeletableManager()

    class Meta:
        abstract = True


class DiameterInfo(Auditable):
    file_name = models.CharField(max_length=250)
    file_path = models.CharField(max_length=250, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    diameter = models.FloatField(default=0)
    participant_index = models.CharField(max_length=10, blank=True, null=True)
    phone_brand = models.CharField(max_length=100, blank=True, null=True)
    phone_model = models.CharField(max_length=100, blank=True, null=True)
    sleep_time = models.CharField(max_length=20, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    verdict = models.CharField(max_length=100, blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'diameter_info'
