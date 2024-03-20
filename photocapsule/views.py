from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models.signals import post_save
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
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Photo

@receiver(user_registered)
def create_user_profile(sender, user, request, **kwargs):
    profile = UserProfile(user=user)
    profile.save()

def index(request):
    context_dict = {}
    context_dict['recent'] = Photo.objects.all().order_by('-uploadDate')[:3]
    context_dict['likes'] = Photo.objects.filter(uploadDate__gte = datetime.now() - timedelta(days=1)).order_by('-likes')[:3]
    return render(request, 'photocapsule/index.html', context=context_dict)

@login_required
def upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.userID = request.user
            selected_categories = request.POST.getlist('categories')
            photo.save()
            if len(selected_categories) == 0:
                category = Category.objects.get(categoryName="Miscellaneous")
                CategoryPhoto.objects.create(photoID=photo, categoryID=category)
            else:
                for category_id in selected_categories:
                    category = Category.objects.get(pk=category_id)
                    CategoryPhoto.objects.create(photoID=photo, categoryID=category)
            return redirect(reverse('photocapsule:index'))
    else:
        initial_data = {'userID': request.user.pk}
        form = PhotoForm(initial=initial_data)
        
    return render(request, 'photocapsule/upload.html', context={'form' : form})

def browse(request):
    return render(request, 'photocapsule/browse.html', context={'result_list': User.objects.all(), 'categories': Category.objects.all()})

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
            return render(request, 'photocapsule/index.html')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request, 'photocapsule/edit-profile.html', {'user_form': user_form, 'profile_form': profile_form})

def photo(request, userPage, photo):
    context_dict = {}
    try:
        user = User.objects.get(username=userPage)
        photo = Photo.objects.get(userID=user,id=photo)
        context_dict['photo'] = photo
    except:
        context_dict['photo'] = None
        context_dict['userLiked'] = None
    return render(request, 'photocapsule/photo.html', context_dict)

def add_comment(request, photo_id):
    if request.method == 'POST' and request.is_ajax():
        text = request.POST.get('comment')
        photo = get_object_or_404(Photo, id=photo_id)
        comment = Comment.objects.create(photo=photo, text=text, user=request.user)
        
        # 将新评论渲染为 HTML
        comment_html = render_to_string('includes/comment.html', {'comment': comment}, request=request)
        
        return JsonResponse({'comment_html': comment_html})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def like(request):
    if request.method == "POST" and request.is_ajax():
        like_or_dislike = request.POST.get('type')
        user = User.objects.get(username=request.POST.get('user'))
        photo = Photo.objects.get(id=request.POST.get('photo'))
        if (like_or_dislike == "Like"):
            UserLike.objects.create(photoID=photo, userID=user)
            setattr(photo, 'likes', photo.likes+1) 
            photo.save()
        else:
            UserLike.objects.get(photoID=photo, userID=user).delete()
            setattr(photo, 'likes', photo.likes-1) 
            photo.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})

def addComment(request):
    if request.method == "POST" and request.is_ajax():
        comment = request.POST.get('comment')
        user = User.objects.get(username=request.POST.get('user'))
        photo = Photo.objects.get(id=request.POST.get('photo'))
        newComment = Comment.objects.create(content=comment,photoID=photo,userID=user)
        comment_html = render_to_string('page_sections\comment.html', {'comment': newComment})
        return JsonResponse({"status": "success", "comment": comment_html})
    return JsonResponse({"status": "error"})

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