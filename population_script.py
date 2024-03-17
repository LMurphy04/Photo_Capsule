import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Photo_Capsule.settings')

import django
django.setup()

from django.contrib.auth.models import User
from photocapsule.models import Category, Photo, CategoryPhoto, Comment, UserLike

def populate():
    users_data = [
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'password1', 'profile_picture': 'profile_pictures/pen.jpg'},
        {'username': 'user2', 'email': 'user2@example.com', 'password': 'password2', 'profile_picture': 'profile_pictures/default.png'},  
    ]
    
    categories_data = [
        {'categoryName': 'Scenery'},
        {'categoryName': 'Example'},
    ]
    
    photos_data = [
        {'title': 'Donut', 'description': 'Example', 'image': 'uploads/download.png', 'userID': 'user1', 'category': 'Example'},
        {'title': 'Window', 'description': 'Majestic morning', 'image': 'uploads/WIN_20230421_17_54_33_Pro.jpg', 'userID': 'user2', 'category': 'Scenery'},
    ]

    comments_data = [
        {'content': 'Nice photo!', 'photo_title': 'Donut', 'user_username': 'user2'},
        {'content': 'Great view!', 'photo_title': 'Window', 'user_username': 'user1'},
    ]

    # Populate users
    for data in users_data:
        user, created = User.objects.get_or_create(username=data['username'], email=data['email'])
        if created:
            user.set_password(data['password'])
            user.save()
    
    # Populate categories
    for data in categories_data:
        Category.objects.get_or_create(categoryName=data['categoryName'])

    # Populate photos
    for data in photos_data:
        user = User.objects.get(username=data['userID'])
        category = Category.objects.get(categoryName=data['category'])
        photo, created = Photo.objects.get_or_create(title=data['title'], description=data['description'], image=data['image'], userID=user)
        if created:
            # If the photo is created, assign it to the category
            CategoryPhoto.objects.create(photoID=photo, categoryID=category)

    # Populate comments
    for data in comments_data:
        photo = Photo.objects.get(title=data['photo_title'])
        user = User.objects.get(username=data['user_username'])
        Comment.objects.create(photoID=photo, userID=user, content=data['content'])

    # Populate likes
    for photo in Photo.objects.all():
        for user in User.objects.all():
            UserLike.objects.create(userID=user, photoID=photo)

if __name__ == '__main__':
    print('Populating database...')
    populate()
    print('Population complete.')
