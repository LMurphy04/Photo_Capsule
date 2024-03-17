import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Photo_Capsule.settings')
django.setup()

import pytz
import random
from django.contrib.auth.models import User
from photocapsule.models import *
from datetime import datetime
random.seed(1)

def populate():
    
    users_data = [
        {'username': 'PhotographyFan01', 'email': 'steven01@gmail.com', 'password': 'genericPassword', 'profile_picture': 'profile_pictures/vintageCamera.jpeg'},
        {'username': 'FakePerson43', 'email': 'temporaryemail@yahoo.com', 'password': 'mothersMaidenName9', 'profile_picture': 'profile_pictures/scribbleHead.png'},
        {'username': 'Snap_King', 'email': 'paul7gerrard@gmail.com', 'password': 'y8uLkn90', 'profile_picture': 'profile_pictures/sunset.jpg'},
        {'username': '1950BlackAndWhite', 'email': 'oldschool@gmail.com', 'password': 'back1nMyDay', 'profile_picture': 'profile_pictures/default.png'},  
        {'username': 'ScotlandScenery', 'email': 'visitscotland@gmail.com', 'password': 'scot1andfor3v3r', 'profile_picture': 'profile_pictures/scotlandFlag.png'},
        {'username': 'BritannyMcGill', 'email': 'runningFanatic@yahoo.com', 'password': 'sp33d0fs0und', 'profile_picture': 'profile_pictures/flowerDog.png'},
    ]
    
    categories_data = [
        {'categoryName': 'Nature'},
        {'categoryName': 'Sport'},
        {'categoryName': 'City'},
        {'categoryName': 'Animal'},
        {'categoryName': 'Events'},
        {'categoryName': 'People'},
        {'categoryName': 'Night'},
        {'categoryName': 'Space'},
        {'categoryName': 'Landscape'},
        {'categoryName': 'Miscellaneous'},
    ]
    
    photos_data = [
        {'title': 'Blue Lake Mountains', 'description': 'Scenic blue lake, paired with a beautiful mountain backdrop.', 'image': 'uploads/mountainScape.jpeg', 'username': 'PhotographyFan01', 'categories': ['Nature','Landscape'], 'uploadDate': None},
        {'title': 'Light Blur', 'description': 'Travelling at the speed of light.', 'image': 'uploads/lightBlur.jpeg', 'username': 'FakePerson43', 'categories': ['Night', 'Miscellaneous'], 'uploadDate': None},
        {'title': '1956 Sports Photo of the Year', 'description': 'What an incredible feat of human talent.', 'image': 'uploads/1956sportsPhotoOfTheYear.jpg', 'username': 'PhotographyFan01', 'categories': ['Sport','People','Events'], 'uploadDate': datetime(2022,3,16,tzinfo=pytz.UTC)},
        {'title': 'Space Station', 'description': 'ISS to Mission Control...', 'image': 'uploads/spaceStation.png', 'username': 'FakePerson43', 'categories': ['Space', 'Events'], 'uploadDate': datetime(2022,1,7,tzinfo=pytz.UTC)},
        {'title': 'Central Park Fog', 'description': 'The skyscrapers loom ominously over Central Park.', 'image': 'uploads/newYorkFog.jpg', 'username': 'PhotographyFan01', 'categories': ['Nature','City','Night'], 'uploadDate': datetime(2024,2,24,tzinfo=pytz.UTC)},
        {'title': 'Cow Farm', 'description': 'Me and my two favourite cows!', 'image': 'uploads/farm.jpg', 'username': 'FakePerson43', 'categories': ['People','Animal'], 'uploadDate': None},
        {'title': 'Dining Out', 'description': 'No better way to spend a Sunday than nachos and beer!', 'image': 'uploads/diningOut.jpeg', 'username': 'PhotographyFan01', 'categories': ['People','Miscellaneous'], 'uploadDate': datetime(2023,8,17,tzinfo=pytz.UTC)},    
        {'title': 'Cross Country Race 2', 'description': 'Congratulations to all my competitors, unfortunately for them there can be only one winner!', 'image': 'uploads/crossCountry.jpg', 'username': 'BritannyMcGill', 'categories': ['Sport','People','Events'], 'uploadDate': None},
        {'title': 'Hard Rock Livery', 'description': 'I would sell my soul for this car. Like this image if you feel the same!', 'image': 'uploads/blackCar.jpg', 'username': 'PhotographyFan01', 'categories': ['Miscellaneous'], 'uploadDate': datetime(2023,11,10,tzinfo=pytz.UTC)},
        {'title': 'Ocean Horizon', 'description': 'To think the world drops off over there.', 'image': 'uploads/horizon.jpg', 'username': 'ScotlandScenery', 'categories': ['Nature'], 'uploadDate': datetime(2024,2,4,tzinfo=pytz.UTC)},
        {'title': 'Powerlines Pretty Sky', 'description': '', 'image': 'uploads/powerlines.jpg', 'username': 'Snap_King', 'categories': ['Miscellaneous'], 'uploadDate': datetime(2022,9,9,tzinfo=pytz.UTC)},
        {'title': 'Skyscraper', 'description': 'Makes me feel so small.', 'image': 'uploads/skyscraper.jpg', 'username': 'BritannyMcGill', 'categories': ['City'], 'uploadDate': datetime(2023,5,21,tzinfo=pytz.UTC)},
    ]

    comments_data = [
        {'photoID': 1, 'username': 'PhotographyFan01', 'content': 'Nice photo!'},
        {'photoID': 2, 'username': 'FakePerson43', 'content': 'Great view!'},
    ]

    # Populate users
    for data in users_data:
        newUser, created = User.objects.get_or_create(username=data['username'], email=data['email'])
        if created:
            newUser.set_password(data['password'])
            newUser.save()
            UserProfile.objects.get_or_create(user=newUser, profilePicture=data['profile_picture'])
    
    # Populate categories
    for data in categories_data:
        Category.objects.get_or_create(categoryName=data['categoryName'])

    # Populate photos
    for data in photos_data:
        user = User.objects.get(username=data['username'])
        categories = []
        for category in data['categories']:
            categories.append(Category.objects.get(categoryName=category))
        photo, created = Photo.objects.get_or_create(title=data['title'], description=data['description'], image=data['image'], userID=user)
        if created:
            # If the photo is created, assign it to the categories
            for category in categories:
                CategoryPhoto.objects.create(photoID=photo, categoryID=category)
            #If custom upload date is specified, set it (allows testing of trending which only counts photos from the last day)
            if data['uploadDate'] != None:
                setattr(photo, 'uploadDate', data['uploadDate'])
                photo.save()

    # Populate comments
    for data in comments_data:
        photo = Photo.objects.get(id=data['photoID'])
        user = User.objects.get(username=data['username'])
        Comment.objects.create(photoID=photo, userID=user, content=data['content'])

    # Populate likes
    for photo in Photo.objects.all():
        for user in User.objects.all():
            #to avoid having to create a bunch of arbitrary likes, use a random with a set seed to generate the same like structure everytime
            if (random.randrange(0,2) == 0):
                UserLike.objects.create(photoID=photo, userID=user)
                setattr(photo, 'likes', photo.likes+1) 
                photo.save()

if __name__ == '__main__':
    print('Populating database...')
    populate()
    print('Population complete.')
