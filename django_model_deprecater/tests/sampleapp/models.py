from django.db import models


class V1Thing(models.Model):
    foo = models.CharField(max_length=16)


class V2Thing(models.Model):
    bar = models.CharField(max_length=16)


class V3Thing(models.Model):
    baz = models.CharField(max_length=16)