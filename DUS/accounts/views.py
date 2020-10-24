from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import  UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm


def signup_view(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('accounts:login')
    
    return render(request, "registration/signup.html", {'form':form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logout successful")
    return redirect('Homepage')

def login_view(request):
    if not request.user.is_authenticated: # If you are logged in then it will stop logging in again
        form = AuthenticationForm()
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username= username, password=password)
                if user is not None:
                    login(request, user)
                    redirection_url = request.POST.get('next')
                    if redirection_url:
                        print (redirection_url)
                        return HttpResponseRedirect(redirection_url)
                    else:
                        messages.success(request, f"Logged in successfully as {username}")
                        return redirect('Homepage')
                else:
                    messages.error(request, "User Doesn't Exists.")
                    return render(request, "registration/login.html", {'form':form})
        else:
            form = AuthenticationForm()
        return render(request, "registration/login.html", {'form':form})
    else:
        messages.info(request, "You are already logged in")
        return redirect('Homepage')