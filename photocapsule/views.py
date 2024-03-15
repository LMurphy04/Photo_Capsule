from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from registration.signals import user_registered
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from photocapsule.models import User, Photo, Category
from django.contrib import messages
from photocapsule.forms import UserForm, ProfileForm

@receiver(user_registered)
def create_user_profile(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()

def index(request):
    return render(request, 'photocapsule/index.html', context={})

@login_required
def upload(request):
    return render(request, 'photocapsule/upload.html', context={})

def browse(request):
    result_list = []
    if request.method == 'POST':
        profile = request.POST['profile'].strip()
        result_list = User.objects.filter(username__contains=profile)
    else:
        result_list = User.objects.filter()
    return render(request, 'photocapsule/browse.html', context={'result_list': result_list, 'categories': Category.objects.all()})

def profileResults(request, userPage):
    context_dict = {}
    try:
        userPage = User.objects.get(username=userPage)
        context_dict['userPage'] = userPage
        context_dict['photos'] = Photo.objects.filter(userID=userPage)
    except User.DoesNotExist:
        context_dict['userPage'] = None
        context_dict['photos'] = None
    return render(request, 'photocapsule/profile.html', context=context_dict)

def categoryResults(request, category):
    context_dict = {}
    try:
        category = Category.objects.get(categoryName=category)
        context_dict['category'] = category
        context_dict['photos'] = Photo.objects.filter(categoryphoto__categoryID=category)
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['photos'] = None
    return render(request, 'photocapsule/category-results.html', context=context_dict)

def profile(request, userPage):
    context_dict = {}
    try:
        userPage = User.objects.get(username=userPage)
        context_dict['userPage'] = userPage
        context_dict['photos'] = Photo.objects.filter(userID=userPage)
    except User.DoesNotExist:
        context_dict['userPage'] = None
        context_dict['photos'] = None
    return render(request, 'photocapsule/profile.html', context=context_dict)

@login_required
def editProfile(request, userPage):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return render(request, 'photocapsule/index.html')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request, 'photocapsule/edit-profile.html', {'user_form': user_form, 'profile_form': profile_form})

def photo(request, userPage, photo):
    return render(request, 'photocapsule/photo.html', context={'photo': Photo.objects.get(id=photo)})


