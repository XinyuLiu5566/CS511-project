from django.db import models
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo)
# Create your models here.
config.DATABASE_URL = 'bolt://neo4j:00000000@localhost:11008'

class User(StructuredNode):
    name = StringProperty(unique_index=True)
    gender = StringProperty()

class Company(StructuredNode):
    name = StringProperty(unique_index=True)
    address = StringProperty()
    year = StringProperty()

class App(StructuredNode):
    name = StringProperty(unique_index=True)
    category = StringProperty()
    year = StringProperty()




class AppInfo(models.Model):
    idx = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    app_id = models.CharField(primary_key=True, max_length=255)
    category = models.CharField(max_length=255)
    rating = models.FloatField()
    rating_count = models.FloatField(blank=True, null=True)
    install_number = models.FloatField()
    price = models.FloatField()
    size = models.CharField(max_length=255)
    system_required = models.CharField(max_length=255)
    release_date = models.CharField(max_length=255)
    age_required = models.CharField(max_length=255)
    ad_support = models.CharField(max_length=255)

    def __str__(self):
        return self.app_name + '-' + self.app_id

    class Meta:
        managed = False
        db_table = 'google_store'

class AppInfo_Mongo(models.Model):
    idx = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)
    app_id = models.CharField(primary_key=True, max_length=255)
    category = models.CharField(max_length=255)
    rating = models.FloatField()
    rating_count = models.FloatField(blank=True, null=True)
    install_number = models.FloatField()
    price = models.FloatField()
    size = models.CharField(max_length=255)
    system_required = models.CharField(max_length=255)
    release_date = models.CharField(max_length=255)
    age_required = models.CharField(max_length=255)
    ad_support = models.CharField(max_length=255)
    class Meta:
        db_table = "google_store"