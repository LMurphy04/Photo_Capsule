from django.test import TestCase
from django.urls import reverse
from .models import Photo, Category, Comment, UserProfile, UserLike, CategoryPhoto
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
from datetime import datetime

# Set Up
class BaseTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create(username='User1', email='user1@gmail.com')
        self.user2 = User.objects.create(username='User2', email='user2@gmail.com')

        # Create categories
        self.category1 = Category.objects.create(categoryName='Nature')
        self.category2 = Category.objects.create(categoryName='Sport')

# Testing Photos and Photo Interaction
class PhotoModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()  

        # Create photos
        self.photo1 = Photo.objects.create(
            title='Test Photo 1',
            description='This is a test photo 1',
            image='uploads/test1.jpg',
            userID=self.user1
        )

        self.photo2 = Photo.objects.create(
            title='Test Photo 2',
            description='', #Check for extreme case (empty description)
            image='uploads/test2.jpg',
            userID=self.user2
        )

        # Associate categories with photos
        CategoryPhoto.objects.create(photoID=self.photo1, categoryID=self.category1)
        CategoryPhoto.objects.create(photoID=self.photo2, categoryID=self.category2)
        CategoryPhoto.objects.create(photoID=self.photo2, categoryID=self.category1) #Test Photos can have multiple categories

        # Create comments
        self.comment1 = Comment.objects.create(
            photoID=self.photo1,
            userID=self.user2,
            content='Nice photo!'
        )
        self.comment2 = Comment.objects.create(
            photoID=self.photo2,
            userID=self.user1,
            content='Great shot!'
        )

        # Create likes
        self.userlike1 = UserLike.objects.create(photoID=self.photo1, userID=self.user2)
        self.userlike2 = UserLike.objects.create(photoID=self.photo2, userID=self.user1)
        self.userlike3 = UserLike.objects.create(photoID=self.photo2, userID=self.user2) #Test Users can like their own photos

    def test_photo_creation(self):
        """Test that a photo is created correctly"""
        self.assertEqual(self.photo1.title, 'Test Photo 1')
        self.assertEqual(self.photo2.title, 'Test Photo 2')
        self.assertEqual(self.photo1.description, 'This is a test photo 1')
        self.assertEqual(self.photo2.description, '')
        self.assertEqual(self.photo1.image, 'uploads/test1.jpg')
        self.assertEqual(self.photo2.image, 'uploads/test2.jpg')
        self.assertEqual(self.photo1.userID, self.user1)
        self.assertEqual(self.photo2.userID, self.user2)

        #Test association with categories
        photo_1_categories = Category.objects.filter(categoryphoto__photoID=self.photo1)
        photo_2_categories = Category.objects.filter(categoryphoto__photoID=self.photo2)
        self.assertEqual(len(photo_1_categories), 1)
        self.assertEqual(len(photo_2_categories), 2)

        #Test that uploadDate is populated automatically
        self.assertTrue(self.photo1.uploadDate <= timezone.now())
        self.assertTrue(self.photo2.uploadDate <= timezone.now())

    def test_comment_creation(self):
        """Test that a comment is created correctly"""
        self.assertEqual(self.comment1.photoID, self.photo1)
        self.assertEqual(self.comment1.userID, self.user2)
        self.assertEqual(self.comment1.content, 'Nice photo!')
        self.assertEqual(self.comment2.photoID, self.photo2)
        self.assertEqual(self.comment2.userID, self.user1)
        self.assertEqual(self.comment2.content, 'Great shot!')

        #Test that uploadDate is populated automatically
        self.assertTrue(self.comment1.uploadDate <= timezone.now())
        self.assertTrue(self.comment2.uploadDate <= timezone.now())

    def test_userlike_creation(self):
        """Test that a like is created correctly"""
        self.assertEqual(self.userlike1.photoID, self.photo1)
        self.assertEqual(self.userlike1.userID, self.user2)
        self.assertEqual(self.userlike2.photoID, self.photo2)
        self.assertEqual(self.userlike2.userID, self.user1)
        self.assertEqual(self.userlike3.photoID, self.photo2)
        self.assertEqual(self.userlike3.userID, self.user2)

# Testing Categories
class CategoryModelTestCase(BaseTestCase):
    def test_category_creation(self):
        """Test that a category is created correctly"""
        self.assertEqual(self.category1.categoryName, 'Nature')

# Testing Profiles
class UserProfileModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()  

        # Create user profile pictures
        self.user_1_profile_picture = UserProfile.objects.create(user=self.user1, profilePicture='profile_pictures/picture.png')
        self.user_2_profile_picture = UserProfile.objects.create(user=self.user2) #tests default profile picture

    def test_userprofile_creation(self):
        """Test that a user profile picture is created correctly"""
        self.assertEqual(self.user_1_profile_picture.user, self.user1)
        self.assertEqual(self.user_1_profile_picture.profilePicture, 'profile_pictures/picture.png')
        self.assertEqual(self.user_2_profile_picture.user, self.user2)
        self.assertEqual(self.user_2_profile_picture.profilePicture, 'profile_pictures/default.png')

# Helper Functions
def createUser(username, email):
    user = User.objects.get_or_create(username=username, email=email)[0]
    return user

def createCategory(name):
    category = Category.objects.get_or_create(categoryName=name)[0]
    return category

def createPhoto(title,description,image,user,dateOverride=None):
    photo = Photo.objects.get_or_create(
            title=title,
            description=description,
            image=image,
            userID=user
        )[0]
    
    if (dateOverride):
        setattr(photo, 'uploadDate', dateOverride)
        photo.save()

    return photo

def createLike(user,photo):
    userLike = UserLike.objects.get_or_create(userID=user,photoID=photo)[0]
    setattr(photo, 'likes', photo.likes+1) 
    photo.save()
    return userLike

def createComment(comment,user,photo):
    comment = Comment.objects.get_or_create(content=comment,userID=user,photoID=photo)[0]
    return comment

def assignPhotoToCategory(photo,category):
    categoryLink = CategoryPhoto.objects.get_or_create(photoID=photo, categoryID=category)[0]
    return categoryLink

''' Testing Views '''

# Testing Index / Homepage
class IndexViewTests(TestCase):

    def test_index_view_with_no_photos(self):
        response = self.client.get(reverse('photocapsule:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['recent'], []) # Should contain most recent three photos
        self.assertQuerysetEqual(response.context['likes'], []) # Should contain most liked three photos of the last 24hrs
    
    def test_index_view_with_no_photos_in_last_day(self):
        
        user = createUser("User1","user1@gmail.com")
        createPhoto("Test Photo","This photo is outwith the last 24hrs","uploads/test.jpg",user,datetime(2022,3,16,tzinfo=pytz.UTC))
        createPhoto("Test Photo 2","This photo is also outwith the last 24hrs","uploads/test2.png",user,datetime(2023,7,26,tzinfo=pytz.UTC))

        response = self.client.get(reverse('photocapsule:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recent']), 2)
        self.assertQuerysetEqual(response.context['likes'], [])

    def test_index_view_with_photos_in_last_day(self):
        
        user = createUser("User1","user1@gmail.com")
        createPhoto("Test Photo","This photo is not outwith the last 24hrs","uploads/test.jpg",user)
        createPhoto("Test Photo 2","This photo is outwith the last 24hrs","uploads/test2.png",user,datetime(2023,7,26,tzinfo=pytz.UTC))

        response = self.client.get(reverse('photocapsule:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recent']), 2)
        self.assertEqual(len(response.context['likes']), 1)

    def test_index_view_with_over_4_photos_in_last_day(self):
        
        user = createUser("User1","user1@gmail.com")
        createPhoto("Test Photo","This photo is not outwith the last 24hrs","uploads/test.jpg",user)
        createPhoto("Test Photo 2","This photo is not also outwith the last 24hrs","uploads/test2.jpg",user)
        createPhoto("Test Photo 3","This photo is not also outwith the last 24hrs","uploads/test3.png",user)
        createPhoto("Test Photo 4","This photo is not also outwith the last 24hrs","uploads/test4.jpg",user)

        response = self.client.get(reverse('photocapsule:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recent']), 3)
        self.assertEqual(len(response.context['likes']), 3)

# Testing Browse
class BrowseViewTests(TestCase):

    def test_browse_view_with_no_profiles_and_no_categories(self):
        response = self.client.get(reverse('photocapsule:browse'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['result_list'], []) # Should contain all profiles
        self.assertQuerysetEqual(response.context['categories'], []) # Should contain all categories

    def test_browse_view_with_profiles_and_categories(self):

        createUser("User1","user1@gmail.com")
        createUser("User2","user2@gmail.com")
        createUser("User3","user3@gmail.com")
        createUser("User4","user4@gmail.com")
        createUser("User5","user5@gmail.com")

        createCategory("Category1")
        createCategory("Category2")
        createCategory("Category3")
        createCategory("Category4")

        response = self.client.get(reverse('photocapsule:browse'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['result_list']), 5)
        self.assertEqual(len(response.context['categories']), 4)

# Testing Category Results
class CategoryResultsViewTests(TestCase):

    def test_category_results_view_with_nonexistant_category(self):
        response = self.client.get(reverse('photocapsule:category-results', kwargs={'category':'FakeCategory'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photos'], None) # Should contain all photos in matching category

    def test_category_results_view_with_category_with_no_photos(self):
        createCategory("Category1")

        response = self.client.get(reverse('photocapsule:category-results', kwargs={'category':'Category1'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['photos'], [])

    def test_category_results_view_with_category_with_photos(self):
        user = createUser("User1","user1@gmail.com")
        category = createCategory("Category1")
        photo1 = createPhoto("TestPhoto 1","Description","uploads/test.png",user)
        assignPhotoToCategory(photo1,category)
        photo2 = createPhoto("TestPhoto 2","Description","uploads/test2.png",user)
        assignPhotoToCategory(photo2,category)
        
        response = self.client.get(reverse('photocapsule:category-results', kwargs={'category':'Category1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['photos']), 2)

    def test_category_results_view_with_all_category_with_distinct_photos(self):
        user = createUser("User1","user1@gmail.com")
        category1 = createCategory("Category1")
        category2 = createCategory("Category2")
        photo1 = createPhoto("TestPhoto 1","Description","uploads/test.png",user)
        assignPhotoToCategory(photo1,category1)
        photo2 = createPhoto("TestPhoto 2","Description","uploads/test2.png",user)
        assignPhotoToCategory(photo2,category1)
        photo3 = createPhoto("TestPhoto 3","Description","uploads/test3.png",user)
        assignPhotoToCategory(photo3,category2)

        response = self.client.get(reverse('photocapsule:category-results', kwargs={'category':'All Categories'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['photos']), 3)

    def test_category_results_view_with_all_category_with_shared_photo(self):
        user = createUser("User1","user1@gmail.com")
        category1 = createCategory("Category1")
        category2 = createCategory("Category2")
        photo1 = createPhoto("TestPhoto 1","Description","uploads/test.png",user)
        assignPhotoToCategory(photo1,category1)
        assignPhotoToCategory(photo1,category2)

        response = self.client.get(reverse('photocapsule:category-results', kwargs={'category':'All Categories'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['photos']), 1)

# Testing Profile View
class ProfileViewTests(TestCase):

    def test_profile_view_with_nonexistant_profile(self):
        response = self.client.get(reverse('photocapsule:profile', kwargs={'userPage':'FakeUser'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photos'], None) # Should contain all photos uploaded by user

    def test_profile_view_with_profile_with_no_photos(self):
        createUser("User1","user1@gmail.com")
        
        response = self.client.get(reverse('photocapsule:profile', kwargs={'userPage':'User1'}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['photos'], [])

    def test_profile_view_with_profile_with_photos(self):
        user = createUser("User1","user1@gmail.com")
        createPhoto("TestPhoto 1","Description","uploads/test1.png",user)
        createPhoto("TestPhoto 2","Description","uploads/test2.png",user)
        
        response = self.client.get(reverse('photocapsule:profile', kwargs={'userPage':'User1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['photos']), 2)

# Testing Photo Details View
class PhotoViewTests(TestCase):

    def test_photo_view_with_nonexistant_photo(self):
        response = self.client.get(reverse('photocapsule:photo', kwargs={'userPage':'FakeUser','photo':1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photo'], None) # Should be photo with matching user and photoID

    def test_photo_view_with_wrong_user(self):
        user = createUser("User1","user1@gmail.com")
        createUser("User2","user2@gmail.com")
        photo = createPhoto("TestPhoto 1","Description","uploads/test1.png",user)

        response = self.client.get(reverse('photocapsule:photo', kwargs={'userPage':'User2','photo':photo.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photo'], None)

    def test_photo_view_with_right_user(self):
        user = createUser("User1","user1@gmail.com")
        photo = createPhoto("TestPhoto 1","Description","uploads/test1.png",user)

        response = self.client.get(reverse('photocapsule:photo', kwargs={'userPage':'User1','photo':photo.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['photo'], photo)