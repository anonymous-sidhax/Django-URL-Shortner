from django.db import models
from django.contrib.auth.models import User


issues_choices = (('Report a bug','Report a bug'),('Feature Request','Feature Request'),('Enhancement','Enhancement'),)

class Keys(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=6)

    def __str__(self):
        return self.key

class Shorten_Urls(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=15, on_delete=models.CASCADE)
    original_url = models.CharField(blank=False, max_length=200)
    short_url = models.CharField(blank=False, max_length=30, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(auto_now=True)
    expire_flag = models.BooleanField(default=False)
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.short_url 



class ContactUsModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    issue = models.CharField(max_length=100, choices=issues_choices, default='Report a bug')
    message = models.TextField()


    def __str__(self):
        return self.name + ' | ' + str(self.message)[:200]