from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Keys, Shorten_Urls, ContactUsModel
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from .forms import ConatcUsForm
import accounts.urls
import random
import string
from django.utils import timezone
from datetime import datetime, timedelta


USED_FOR_MAPPING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"

def home(request):

    return render(request, "index.html")

@login_required(login_url='/accounts/login/')
def dashboard(request):
    print(datetime.now())
    print(datetime.now() + timedelta(days=1))
    return render(request, "dashboard.html")

def redirection(request, url):
    short_url = "http://127.0.0.1:8000" + request.path
    try:
        check = Shorten_Urls.objects.get(short_url=short_url)
        if(check.expire_flag == False or datetime.now() < check.expiration_date):
            check.visits += 1
            check.save()
            return HttpResponseRedirect(check.original_url)
        else:
            check.expire_flag = True
            return render(request, 'expired.html')
    except Shorten_Urls.DoesNotExist:
        messages.error(request, "Url you are try to reach is not available. Try a different url or create one.")
        return redirect("/")

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
                if not check:
                    newurl = Shorten_Urls(
                        original_url=original,
                        short_url=short,
                        user=request.user,
                        creation_date=datetime.now(),
                        expiration_date=datetime.now() + timedelta(days=7)
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
<<<<<<< HEAD
                newurl = Shorten_Urls(original_url=original, short_url=short, user=request.user, creation_date=datetime.now(), expiration_date=datetime.now() + timedelta(days=7))
=======
                newurl = Shorten_Urls(original_url=original, short_url=short, user=request.user, creation_date=datetime.now())
>>>>>>> d670ef426e53e9ccf65273385f4e1304e2190fc3
                newurl.save()
                context = {
                    "short_url":short,
                }
                messages.success(request, "Url created successfully. Check below")
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


def contactus(request):
    form = ConatcUsForm()
    if request.method == 'POST':
        form = ConatcUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            issue = form.cleaned_data.get('issue')
            message = form.cleaned_data.get('message')
            
            contatcus = ContactUsModel(name=name, email=email, issue=issue, message=message)
            contatcus.save()
    return render(request, "contactus.html", {'form': form})



def aboutus(request):
    return render(request, "aboutus.html", {})