from django.db import models


class TestResource(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)


class NestedResource(models.Model):
    resource = models.ForeignKey(TestResource)
    name = models.CharField(max_length=255)
