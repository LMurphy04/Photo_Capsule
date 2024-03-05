from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

def index(request):
    return render(request, 'photocapsule/index.html', context={})

def register(request):
    return render(request, 'photocapsule/register.html', context={})

def signIn(request):
    return render(request, 'photocapsule/sign-in.html', context={})

def upload(request):
    return render(request, 'photocapsule/upload.html', context={})

def browse(request):
    return render(request, 'photocapsule/browse.html', context={})

def profileResults(request):
    return render(request, 'photocapsule/profile-results.html', context={})

def categoryResults(request):
    return render(request, 'photocapsule/category-results.html', context={})

def profile(request):
    return render(request, 'photocapsule/profile.html', context={})

def editProfile(request):
    return render(request, 'photocapsule/edit-profile.html', context={})

def photo(request):
    return render(request, 'photocapsule/photo.html', context={})

def signOut(request):
    return redirect(reverse('photocapsule:index'))
