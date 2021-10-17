from django.db import models

# Create your models here.
class Phone(models.Model):
	app_name = models.CharField(max_length=100)
	app_id = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	class Meta:
		db_table = "google_app_store"
