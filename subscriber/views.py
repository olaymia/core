from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,
                                         username=email,
                                         password=password)

        if user != None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email Password Are Not Matched ')
        return redirect('/')

    return render(request, 'subscriber/login.html')


def user_dashboard(request):
    return render(request, 'subscriber/dashboard.html')


def user_registration(request):
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fullname = request.POST.get('fullname')

        # check email
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email are already Exists !')
            return redirect('register')

        # check email
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already exist in the system, please chose another username  !')
            return redirect('register')

        user = User(

            username=username,
            email=email,

        )

        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'subscriber/registration.html')

@login_required
def user_dashboard(request):
    return render(request, 'subscriber/dashboard.html')


def users_profile(request):
    return render(request, 'subscriber/profile.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_options_pre(request):
    return render(request, 'subscriber/pre_options.html')

@login_required
def user_options_para(request):
    return render(request, 'subscriber/para_options.html')

@login_required
def user_options_clicnical(request):
    return render(request, 'subscriber/clinical_options.html')


@login_required
def data_repo(request):
    return render(request, 'subscriber/repo.html')
