from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.urls import reverse

from loginapp.forms import SignUpForm, profileForm
from loginapp.models import Profile




def signin(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('app_shop:index'))
    return render(request, 'loginapp/signin.html', context={'form': form})


def sing_up(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created Successfully')
            return HttpResponseRedirect(reverse('loginapp:signin'))
    return render(request, 'loginapp/signup.html', context={'form': form})


@login_required
def use_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = profileForm(instance=profile)

    if request.method == "POST":
        form = profileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Change profile Successfully')
            form = profileForm(instance=profile)

    return render(request, 'loginapp/change_profile.html', context={'form': form})


@login_required
def logut_user(request):
    logout(request)
    messages.warning(request,"logout Successfully ")
    return HttpResponseRedirect(reverse('app_shop:index'))
