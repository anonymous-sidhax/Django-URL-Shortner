from django.db import models

# Create your models here.
class Keys(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=6)

    def __str__(self):
        return self.key

class Shorten_Urls(models.Model):
    id = models.AutoField(primary_key=True)
    original_url = models.CharField(max_length=200)
    short_url = models.CharField(max_length=10)

    def __str__(self):
        return self.short_url
