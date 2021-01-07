from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def user_login(request):
    template_name = "user-login.html"
    ctx = {}

    if request.method == 'POST':
        username = request.POST.get('username',"")
        password = request.POST.get('password',"")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
        ctx['error'] = 'Valid username and password required.'

    return render(request, template_name, ctx)
