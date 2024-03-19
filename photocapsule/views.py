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
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Photo

@receiver(user_registered)
def create_user_profile(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()

def index(request):
    context_dict = {}
    context_dict['recent'] = Photo.objects.all().order_by('-uploadDate')[:4]
    context_dict['likes'] = Photo.objects.filter(uploadDate__gte = datetime.now() - timedelta(days=1)).order_by('-likes')[:4]
    return render(request, 'photocapsule/index.html', context=context_dict)

@login_required
def upload(request):
    return render(request, 'photocapsule/upload.html', context={})

def browse(request):
    result_list = []
    if request.is_ajax():
        profile = request.POST['profile'].strip()
        result_list = User.objects.filter(username__contains=profile)

        #create list of profiles to display
        profile_http = ""
        if len(result_list) == 0:
            profile_http += '<li>No Profiles Found!</li>'
        else:
            for user in result_list:
                profile_http += '<li><a href="/photocapsule/browse/profile/'+user.username+'">'+user.username+'</a></li>'

        return HttpResponse(profile_http)
    else:
        result_list = User.objects.filter()
        return render(request, 'photocapsule/browse.html', context={'result_list': result_list, 'categories': Category.objects.all()})

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

def add_comment(request, photo_id):
    if request.method == 'POST' and request.is_ajax():
        text = request.POST.get('comment')
        photo = get_object_or_404(Photo, id=photo_id)
        comment = Comment.objects.create(photo=photo, text=text, user=request.user)
        
        # 将新评论渲染为 HTML
        comment_html = render_to_string('includes/comment.html', {'comment': comment}, request=request)
        
        return JsonResponse({'comment_html': comment_html})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# def search_profiles(request):
#     search_term = request.GET.get('search_term', '')
#     profiles = UserProfile.objects.filter(user__username__icontains=search_term)
#     profiles_html = render_to_string('includes/profiles_list.html', {'profiles': profiles}, request=request)
#     return JsonResponse({'profiles_html': profiles_html})

# def sort_results(request):
#     sort_by = request.GET.get('sort_by', 'default_sort_field')
#     results = MyModel.objects.all().order_by(sort_by)
#     results_html = render_to_string('includes/results_list.html', {'results': results}, request=request)
#     return JsonResponse({'results_html': results_html})

@require_POST
@login_required
def like_photo(request):
    photo_id = request.POST.get('photo_id')
    action = request.POST.get('action')
    if photo_id and action:
        try:
            photo = Photo.objects.get(id=photo_id)
            if action == 'like':
                photo.likes += 1
            elif action == 'unlike':
                photo.likes -= 1
            photo.save()
            return JsonResponse({'status':'ok'})
        except Photo.DoesNotExist:
            pass
    return JsonResponse({'status':'error'})