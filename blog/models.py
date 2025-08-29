from django.conf import settings
from django.db import models
from django.utils import timezone

class Builder(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubAssembly(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Sub Assembly"
        verbose_name_plural = "Sub Assemblies"


    def __str__(self):
        return self.name


class BuildRecord(models.Model):
    builder = models.ForeignKey(Builder, on_delete=models.CASCADE, related_name='builds')
    subassembly = models.ForeignKey(SubAssembly, on_delete=models.CASCADE, related_name='builds')
    time_minutes = models.FloatField()
    build_date = models.DateField() #auto_now_add=True - I removed this so we can enter the date in ourselves
    signed_off_by = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"{self.builder} - {self.subassembly} - {self.time_minutes:.2f}m"
