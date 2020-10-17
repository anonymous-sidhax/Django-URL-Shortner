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

