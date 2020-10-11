from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Keys, Shorten_Urls
from django.contrib.auth.models import User
from django.contrib import messages

import random
import string

USED_FOR_MAPPING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"

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

def shortenn(request):
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

def shorten(request):
    if request.method == "POST":
        print('POST')
        if request.POST['original_url'] and request.POST['custom_url']:
            print ('custom')
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
                return redirect('/')
            else:
                messages.error(request, "Already Exists")
                return render(request, 'index.html', { 'error' : 'Custom URL already exists'})
        elif request.POST['original_url']:
            original = request.POST['original_url']
            short = 'http://127.0.0.1:8000/'
            '''present = False

            while not present:
                short = random_generate()
                check = Shorten_Urls.objects.filter(short_url=short)
                if not check:
                    newurl = Shorten_Urls(
                        original_url=original,
                        short_url=short,
                    )
                    newurl.save()
                    return redirect('/')
                else:
                    continue
                    '''
            key = Keys.objects.last()
            short += key.key
            key.delete()
            newurl = Shorten_Urls (
                        original_url=original,
                        short_url=short,
                    )
            newurl.save()
            return redirect('/')
        else:
            messages.error(request, "Empty Field")
            return redirect('')
    else:
        return redirect('')

# For generating random string
def random_generate():
    return ''.join(random.choice(USED_FOR_MAPPING) for i in range(3))
