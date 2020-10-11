from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Keys, Shorten_Urls
from django.contrib.auth.models import User
from django.contrib import messages

# USED_FOR_MAPPING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"

def home(request):
    return render(request, "index.html")

def signup(request):

    if request.method == "POST":
        if request.POST['password'] == request.POST['password2']:
            if request.POST['username'] and request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email = request.POST['email'])
                    return render(request, 'signup.html', { 'error' : 'User already exists'})

                except User.DoesNotExist:
                    User.objects.create_user(
                        username = request.POST['password'],
                        email = request.POST['email'],
                        password = request.POST['password']
                    )
                    messages.success(request, "Signup Sucessful | Login Here")
                    return redirect(login)

            else:
                return render(request, 'signup.html', { 'error' : "Empty Fields"}) 
        else:
            return render(request, 'signup.html', { 'error' : "Password don't match"})
    else:
        return render(request, 'signup.html')


    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def logout(request):
    return render(request, "logout.html")

def shorten(request):
    url = "http://127.0.0.1:8000/"
    original_url = request.GET.get('original_url')
    key = Keys.objects.last()
    url += key.key
    key.delete()
    shorten_url = Shorten_Urls(original_url=original_url, short_url=url)
    shorten_url.save()
    return redirect('/')

def redirection(request, url):
    short_url = "http://127.0.0.1:8000" + request.path
    original_url = Shorten_Urls.objects.get(short_url=short_url)
    return HttpResponseRedirect(original_url.original_url)
