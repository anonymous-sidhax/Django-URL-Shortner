from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Keys, ShortenUrl, ContactUs, DashboardStats
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from .forms import ContactUsForm
import accounts.urls
import random
import string
from django.utils import timezone
from datetime import datetime, timedelta
import os

USED_FOR_MAPPING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"

def get_url():
	print(len(USED_FOR_MAPPING))
	res = set()
	for i in range(pow(64,3)):
		n = i
		curr = ""
		for j in range(3):
			curr+=USED_FOR_MAPPING[n%64]
			n//= 64
		res.add(curr)

	return res




def home(request):
#     res = get_url()
#     for it in res:
#         k = Keys(key=it)
#         k.save()
    return render(request, "index.html")

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, "dashboard.html")

def redirection(request, url):
    short_url = "https://duspy.herokuapp.com/" + request.path
    try:
        check = ShortenUrl.objects.get(short_url=short_url)
        if(check.expire_flag == False or datetime.now() < check.expiration_date):
            check.visits += 1
            check.save()
            dashboard_logging(request)

            return HttpResponseRedirect(check.original_url)
        else:
            check.expire_flag = True
            return render(request, 'expired.html')
    except ShortenUrl.DoesNotExist:
        messages.error(request, "The URL you are trying to reach has been expired or it is not yet created.")
        return redirect("/")

@login_required(login_url='/accounts/login/')
def shorten_for_logged_in_users(request):
    if request.method == "POST":
        if request.POST['original_url'] and request.POST['custom_url']:
            original = request.POST['original_url']
            org_url = ShortenUrl.objects.filter(original_url=original).exists()
            if org_url:
                url = ShortenUrl.objects.get(original_url=original)
                context = {
                    "short_url":url,
                }
                messages.error(request, "Short URL already exists. Please use the below URL.")
                return render(request, 'dashboard.html', context)
            else:
                original = request.POST['original_url']
                expiry_days = request.POST['expire_days']
                if not expiry_days:
                    expiry_days = 7

                short = 'https://duspy.herokuapp.com/' + str(request.POST['custom_url'])
                check = ShortenUrl.objects.filter(short_url=short)
                if not check:
                    newurl = ShortenUrl(
                        original_url=original,
                        short_url=short,
                        user=request.user,
                        creation_date=datetime.now(),
                        expiration_date=datetime.now() + timedelta(days=expiry_days)
                    )
                    newurl.save()
                    context = {
                        "short_url":short,
                    }
                    return render(request, 'dashboard.html', context)
                else:
                    messages.error(request, "Custom URL already exists. Please use a different path.")
                    return render(request, 'dashboard.html.html', { 'error' : 'Custom URL already exists'})
        elif request.POST['original_url']:
            original = request.POST['original_url']
            expiry_days = request.POST['expire_days']
            if not expiry_days:
                expiry_days = 7
            org_url = ShortenUrl.objects.filter(original_url=original).exists()
            if org_url:
                url = ShortenUrl.objects.get(original_url=original)
                context = {
                    "short_url":url,
                }
                return render(request, 'dashboard.html', context)
            else:
                short = 'https://duspy.herokuapp.com/'
                key = Keys.objects.last()
                short += key.key
                key.delete()
                newurl = ShortenUrl(original_url=original, short_url=short, user=request.user, creation_date=datetime.now(), expiration_date=(datetime.now() + timedelta(days=int(expiry_days))))
                newurl.save()
                context = {
                    "short_url":short,
                }
                messages.success(request, "URL created successfully. Check below")
                return render(request, 'dashboard.html', context)
        else:
            messages.error(request, "Empty Field")
            return redirect('')
    else:
        return redirect('')

def shorten(request):
    if request.method == "POST":
        if request.POST['original_url']:
            original = request.POST['original_url']
            org_url = ShortenUrl.objects.filter(original_url=original).exists()
            if org_url:
                url = ShortenUrl.objects.get(original_url=original)
                context = {
                    "short_url":url,
                }
                return render(request, 'index.html', context)
            else:
                short = 'https://duspy.herokuapp.com/'
                key = Keys.objects.last()
                short += key.key
                key.delete()
                newurl = ShortenUrl(original_url=original, short_url=short, user=request.user, creation_date=datetime.now(), expiration_date=datetime.now() + timedelta(days=7))
                newurl.save()
                context = {
                    "short_url":short,
                }
                messages.success(request, "URL created successfully. Check below")
                return render(request, 'index.html', context)
        else:
            messages.error(request, "Empty Field")
            return redirect('')
    else:
        return redirect('')


def contactus(request):
    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            issue = form.cleaned_data.get('issue')
            message = form.cleaned_data.get('message')
            
            contactus = ContactUs(name=name, email=email, issue=issue, message=message)
            contactus.save()
            messages.success(request, "Your message has been submitted sucessfully.")
        else:
            messages.error(request, "You are missing out on a field. Please fill the complete form before submitting.") 
    form = ContactUsForm()
    return render(request, "contactus.html", {'form': form})
                        
def aboutus(request):
    return render(request, "aboutus.html", {})




###########################################   
#       For Logging Dashboard Stats       #
###########################################


def dashboard_logging(request):
    a = get_ip(request)
    print (a)
    print (os.environ[request.META.get('REMOTE_ADDR')])


def get_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


    # g = GeoIP2()
    # ip = request.META.get('REMOTE_ADDR', None)
    # if ip:
    #     city = g.city(ip)['city']
    # else:
    #     city = 'Rome' # default city

    # return 
