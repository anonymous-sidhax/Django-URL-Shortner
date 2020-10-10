from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Keys, Shorten_Urls

# USED_FOR_MAPPING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"

def home(request):

    return render(request, "index_siddesh.html")

def shorten(request):
    url = "http://127.0.0.1:8000/"
    org_url = request.GET.get('org_url')
    key = Keys.objects.last()
    url += key.key
    key.delete()
    shorten_url = Shorten_Urls(original_url=org_url, short_url=url)
    shorten_url.save()
    return redirect('/')

def redirection(request, url):
    short_url = "http://127.0.0.1:8000" + request.path
    org_url = Shorten_Urls.objects.get(short_url=short_url)
    return HttpResponseRedirect(org_url.original_url)
