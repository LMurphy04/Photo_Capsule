from django.shortcuts import render, redirect
from django.urls import reverse
from django.dispatch import receiver
from registration.signals import user_registered
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from photocapsule.models import User, Photo, Category, CategoryPhoto, UserLike, Comment
from django.contrib import messages
from photocapsule.forms import UserForm, ProfileForm, PhotoForm
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import Photo

# Register
@receiver(user_registered)
def create_user_profile(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()

# Homepage
def index(request):
    context_dict = {}
    context_dict['recent'] = Photo.objects.all().order_by('-uploadDate')[:3]
    context_dict['likes'] = Photo.objects.filter(uploadDate__gte = datetime.now() - timedelta(days=1)).order_by('-likes')[:3]
    return render(request, 'photocapsule/index.html', context=context_dict)

# Upload photo
@login_required
def upload(request):
    if request.method == 'POST':
        # Create photo record
        form = PhotoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.userID = request.user
            selected_categories = request.POST.getlist('categories')
            photo.save()
            # Add categories
            if len(selected_categories) == 0: # If no categories selected add to miscellaneous
                category = Category.objects.get(categoryName="Miscellaneous")
                CategoryPhoto.objects.create(photoID=photo, categoryID=category)
            else:
                for category_id in selected_categories:
                    category = Category.objects.get(pk=category_id)
                    CategoryPhoto.objects.create(photoID=photo, categoryID=category)
        return redirect(reverse('photocapsule:profile', kwargs={'userPage':request.user}))
        
    else:
        initial_data = {'userID': request.user.pk}
        form = PhotoForm(initial=initial_data)
        
    return render(request, 'photocapsule/upload.html', context={'form' : form})

# Browse
def browse(request):
    return render(request, 'photocapsule/browse.html', context={'result_list': User.objects.all(), 'categories': Category.objects.all()})

# Category photos page
def categoryResults(request, category):
    context_dict = {}
    try:
        if category == 'All Categories':
            context_dict['category'] = "All"
            context_dict['photos'] = Photo.objects.order_by('-uploadDate')
        else:
            category = Category.objects.get(categoryName=category)
            context_dict['category'] = category
            context_dict['photos'] = Photo.objects.filter(categoryphoto__categoryID=category).order_by('-uploadDate')        
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['photos'] = None
    return render(request, 'photocapsule/category-results.html', context=context_dict)

# Profile page
def profile(request, userPage):
    context_dict = {}
    try:
        userPage = User.objects.get(username=userPage)
        context_dict['userPage'] = userPage
        context_dict['photos'] = Photo.objects.filter(userID=userPage).order_by('-uploadDate')   
    except User.DoesNotExist:
        context_dict['userPage'] = None
        context_dict['photos'] = None
    return render(request, 'photocapsule/profile.html', context=context_dict)

# Edit profile page
@login_required
def editProfile(request, userPage):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect(reverse('photocapsule:profile', kwargs={'userPage':request.POST.get('username')}))

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        return render(request, 'photocapsule/edit-profile.html', {'user_form': user_form, 'profile_form': profile_form})

# Photo details page
def photo(request, userPage, photo):
    context_dict = {}
    try:
        user = User.objects.get(username=userPage)
        photo = Photo.objects.get(userID=user,id=photo)
        context_dict['photo'] = photo
    except:
        context_dict['photo'] = None
    return render(request, 'photocapsule/photo.html', context_dict)

# Like/Dislike photo
def like(request):
    if request.method == "POST" and request.is_ajax():
        like_or_dislike = request.POST.get('type')
        user = User.objects.get(username=request.POST.get('user'))
        photo = Photo.objects.get(id=request.POST.get('photo'))
        
        if (like_or_dislike == "Like"): # If user liked post, create like record and increment count
            UserLike.objects.create(photoID=photo, userID=user)
            setattr(photo, 'likes', photo.likes+1) 
            photo.save()
        else: # If user unliked post, delete like record and decrement count
            UserLike.objects.get(photoID=photo, userID=user).delete()
            setattr(photo, 'likes', photo.likes-1) 
            photo.save()

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})

# Add comment to photo
def addComment(request):
    if request.method == "POST" and request.is_ajax():
        comment = request.POST.get('comment')
        user = User.objects.get(username=request.POST.get('user'))
        photo = Photo.objects.get(id=request.POST.get('photo'))
        newComment = Comment.objects.create(content=comment,photoID=photo,userID=user)
        comment_html = render_to_string('page_sections/comment.html', {'comment': newComment}) # Render new comment
        return JsonResponse({"status": "success", "comment": comment_html})
    return JsonResponse({"status": "error"})
