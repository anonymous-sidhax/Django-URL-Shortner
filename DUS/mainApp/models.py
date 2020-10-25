from django.db import models
from django.contrib.auth.models import User

class Keys(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=6)

    def __str__(self):
        return self.key


class ShortenUrl(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=15, on_delete=models.CASCADE)
    original_url = models.CharField(blank=False, max_length=200)
    short_url = models.CharField(blank=False, max_length=30, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(auto_now=False)
    expire_flag = models.BooleanField(default=False)
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.short_url 


class ContactUs(models.Model):
    issues_choices = (('Report a bug','Report a bug'),('Feature Request','Feature Request'),('Enhancement','Enhancement'),)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    issue = models.CharField(max_length=100, choices=issues_choices, default='Report a bug')
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updation_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ' | ' + str(self.message)[:200]


class DashboardStats(models.Model):
    id = models.AutoField(primary_key=True)
    shorten_id = models.ForeignKey(ShortenUrl, default=15, on_delete=models.CASCADE)
    click_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    referrer_url = models.CharField(max_length=255)
    clicks = models.IntegerField(default=0)