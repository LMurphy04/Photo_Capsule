from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from registration.signals import user_registered
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(user_registered)
def create_user_profile(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()


def index(request):
    return render(request, 'photocapsule/index.html', context={})



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
