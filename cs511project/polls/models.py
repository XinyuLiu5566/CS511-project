from django.db import models

# Create your models here.

class AppInfo(models.Model):
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
        db_table = 'google_playstore'