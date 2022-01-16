from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Keys, ShortenUrl, ContactUs, DashboardStats
from django.contrib import messages
from .forms import ContactUsForm
from django.utils import timezone
from datetime import datetime, timedelta

HOST = 'https://duspy.herokuapp.com/'
#HOST = 'http://127.0.0.1:8000/'
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
    short_url = HOST[:-1] + request.path
    print (short_url)
    try:
        check = ShortenUrl.objects.get(short_url=short_url)
        print(check)
        if(check.expire_flag == 0 or timezone.now() < check.expiration_date):
            check.visits += 1
            check.save()
            #dashboard_logging(request)

            return HttpResponseRedirect(check.original_url)
        else:
            check.expire_flag = 1
            return render(request, 'expired.html')
    except ShortenUrl.DoesNotExist:
        messages.error(request, "The URL you are trying to reach has been expired or it is not yet created.")
        return redirect("/")

@login_required(login_url='/accounts/login/')
def shorten_for_logged_in_users(request):
    print (request.POST['original_url']) 
    print (request.POST['custom_url'])
    if request.method == "POST":
        if request.POST['original_url'] and request.POST['custom_url']:
            original = request.POST['original_url']
            # org_url = ShortenUrl.objects.filter(user_id = request.user.id , original_url=original).exists()
            # if org_url:
            #     url = ShortenUrl.objects.get(user_id = request.user.id, original_url=original)
            #     if url.expiration_date < datetime.now() or url.expire_flag == 1:
            #         url.expiration_date = datetime.now() + timedelta(days=7)
            #         url.expire_flag = 0
            #         url.save()
            #     context = {
            #         "short_url":url,
            #     }
            #     messages.error(request, "Short URL already exists. Please use the below URL.")
            #     return render(request, 'dashboard.html', context)
            # else:
            original = request.POST['original_url']
            expiry_days = request.POST['expire_days']
            custom_url = request.POST['custom_url']
            if not expiry_days:
                expiry_days = 7

            short = HOST + str(request.POST['custom_url'])
            check = ShortenUrl.objects.filter(short_url=short)
            if not check:
                newurl = ShortenUrl(
                    original_url=original,
                    short_url=short,
                    user_id=request.user.id,
                    creation_date=datetime.now(),
                    expiration_date=datetime.now() + timedelta(days=int(expiry_days))
                )
                newurl.save()
                context = {
                    "short_url":short,
                }
                return render(request, 'index.html', context)
            else:
                messages.error(request, "Custom URL already exists. Please use a different path.")
                return render(request, 'index.html', { 'error' : 'Custom URL already exists'})
        elif request.POST['original_url']:
            original = request.POST['original_url']
            expiry_days = request.POST['expire_days']
            if not expiry_days:
                expiry_days = 7
            org_url = ShortenUrl.objects.filter(user_id = request.user.id, original_url=original).exists()
            if org_url:
                url = ShortenUrl.objects.get(user_id = request.user.id, original_url=original)
                if url.expiration_date < timezone.now() or url.expire_flag == 1:
                    url.expiration_date = datetime.now() + timedelta(days=7)
                    url.expire_flag = 0
                    url.save()
                context = {
                    "short_url":url,
                }
                return render(request, 'index.html', context)
            else:
                key = Keys.objects.last()
                short = HOST + key.key
                print (short)
                print (HOST)
                key.delete()
                newurl = ShortenUrl(user_id = request.user.id, original_url=original, short_url=short, user=request.user, creation_date=datetime.now(), expiration_date=(datetime.now() + timedelta(days=int(expiry_days))))
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

def shorten(request):
    if request.method == "POST":
        if request.POST['original_url']:
            original = request.POST['original_url']
            org_url = ShortenUrl.objects.filter(user_id = 15, original_url=original).exists()
            if org_url:
                url = ShortenUrl.objects.get(user_id = 15, original_url=original)
                if url.expiration_date < timezone.now() or url.expire_flag == 1:
                    url.expiration_date = datetime.now() + timedelta(days=7)
                    url.expire_flag = 0
                    url.save()
                context = {
                    "short_url":url,
                }
                return render(request, 'index.html', context)
            else:
                key = Keys.objects.last()
                short = HOST + key.key
                key.delete()
                newurl = ShortenUrl(user_id = 15, original_url=original, short_url=short, creation_date=datetime.now(), expiration_date=datetime.now() + timedelta(days=7))
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
    #print (os.environ[request.META.get('REMOTE_ADDR')])


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