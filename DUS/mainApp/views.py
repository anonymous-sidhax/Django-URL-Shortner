from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from .models import Keys, Shorten_Urls
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm, LoginForm
import accounts.urls
import random
import string

USED_FOR_MAPPING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"


def home(request):
    return render(request, "index.html")

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, "dashboard.html")

# def shortenn(request):
#     url = "http://127.0.0.1:8000/"
#     original_url = request.GET.get('original_url')
#     key = Keys.objects.last()
#     url += key.key
#     key.delete()
#     shorten_url = Shorten_Urls(original_url=original_url, short_url=url)
#     shorten_url.save()
#     return redirect('/')

def redirection(request, url):
    short_url = "http://127.0.0.1:8000" + request.path
    try:
        check = Shorten_Urls.objects.get(short_url=short_url)
        check.visits += 1
        check.save()
        print (short_url)
        return HttpResponseRedirect(check.original_url)
    except Shorten_Urls.DoesNotExist:
        return render(request, 'index.html', {'error' : "error"})

def shorten(request):
    if request.method == "POST":
        if request.POST['original_url'] and request.POST['custom_url']:
            original = request.POST['original_url']
            org_url = Shorten_Urls.objects.filter(original_url=original).exists()
            if org_url:
                url = Shorten_Urls.objects.get(original_url=original)
                context = {
                    "short_url":url,
                }
                messages.error(request, "Short Url already exists. Cannot create custom for it.")
                return render(request, 'index.html', context)
            else:
                original = request.POST['original_url']
                short = 'http://127.0.0.1:8000/' + str(request.POST['custom_url'])
                check = Shorten_Urls.objects.filter(short_url=short)
                print ('check')
                if not check:
                    newurl = Shorten_Urls(
                        original_url=original,
                        short_url=short,
                    )
                    newurl.save()
                    context = {
                        "short_url":short,
                    }
                    return render(request, 'index.html', context)
                else:
                    messages.error(request, "Already Exists")
                    return render(request, 'index.html', { 'error' : 'Custom URL already exists'})
        elif request.POST['original_url']:
            original = request.POST['original_url']
            org_url = Shorten_Urls.objects.filter(original_url=original).exists()
            if org_url:
                url = Shorten_Urls.objects.get(original_url=original)
                context = {
                    "short_url":url,
                }
                return render(request, 'index.html', context)
            else:
                short = 'http://127.0.0.1:8000/'
                key = Keys.objects.last()
                short += key.key
                key.delete()
                newurl = Shorten_Urls (
                            original_url=original,
                            short_url=short,
                        )
                newurl.save()
                context = {
                    "short_url":short,
                }
                return render(request, 'index.html', context)
        else:
            messages.error(request, "Empty Field")
            return redirect('')
    else:
        return redirect('')


def shortening_page(request):
    return render(request, 'shortening.html')

# For generating random string
def random_generate():
    return ''.join(random.choice(USED_FOR_MAPPING) for i in range(3))
