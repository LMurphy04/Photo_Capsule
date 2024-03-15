from django.urls import path
from photocapsule import views

app_name = 'photocapsule'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('browse', views.browse, name='browse'),
    path('browse/profile/<str:userPage>', views.profileResults, name='profile-results'),
    path('browse/category/<str:category>', views.categoryResults, name='category-results'),
    path('profile/<str:userPage>', views.profile, name='profile'),
    path('profile/<str:userPage>/edit', views.editProfile, name='edit-profile'),
    path('photos/<str:userPage>/<str:photo>', views.photo, name='photo'),
]