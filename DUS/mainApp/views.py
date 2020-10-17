from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Keys, Shorten_Urls
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm, LoginForm
import random
import string

USED_FOR_MAPPING = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"




def home(request):
    return render(request, "index.html")


# def shortenn(request):
#     url = "http://127.0.0.1:8000/"
#     original_url = request.GET.get('original_url')
#     key = Keys.objects.last()
#     url += key.key
#     key.delete()
#     shorten_url = Shorten_Urls(original_url=original_url, short_url=url)
#     shorten_url.save()
#     return redirect('/')

# def redirection(request, url):
#     short_url = "http://127.0.0.1:8000" + request.path
#     original_url = Shorten_Urls.objects.get(short_url=short_url)
#     return HttpResponseRedirect(' ')

# def shorten(request):
#     if request.method == "POST":
#         print('POST')
#         if request.POST['original_url'] and request.POST['custom_url']:
#             print ('custom')
#             original = request.POST['original_url']
#             short = 'http://127.0.0.1:8000/' + str(request.POST['custom_url'])
#             check = Shorten_Urls.objects.filter(short_url=short)
#             print ('check')
#             if not check:
#                 newurl = Shorten_Urls(
#                     original_url=original,
#                     short_url=short,
#                 )
#                 newurl.save()
#                 return redirect('/')
#             else:
#                 messages.error(request, "Already Exists")
#                 return render(request, 'index.html', { 'error' : 'Custom URL already exists'})
#         elif request.POST['original_url']:
#             original = request.POST['original_url']
#             short = 'http://127.0.0.1:8000/'
#             '''present = False

#             while not present:
#                 short = random_generate()
#                 check = Shorten_Urls.objects.filter(short_url=short)
#                 if not check:
#                     newurl = Shorten_Urls(
#                         original_url=original,
#                         short_url=short,
#                     )
#                     newurl.save()
#                     return redirect('/')
#                 else:
#                     continue
#                     '''
#             key = Keys.objects.last()
#             short += key.key
#             key.delete()
#             newurl = Shorten_Urls (
#                         original_url=original,
#                         short_url=short,
#                     )
#             newurl.save()
#             return redirect('/')
#         else:
#             messages.error(request, "Empty Field")
#             return redirect('')
#     else:
#         return redirect('')

# # For generating random string
# def random_generate():
#     return ''.join(random.choice(USED_FOR_MAPPING) for i in range(3))
