from django.urls import path
from photocapsule import views

app_name = 'photocapsule'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('browse', views.browse, name='browse'),
    path('browse/username', views.profileResults, name='profile-results'),
    path('browse/category', views.categoryResults, name='category-results'),
    path('profile/<str:userPage>', views.profile, name='profile'),
    path('profile/<str:userPage>/edit', views.editProfile, name='edit-profile'),
    path('photos/username/image-id', views.photo, name='photo'),
]