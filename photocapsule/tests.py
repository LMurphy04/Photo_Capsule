from django.test import TestCase
from django.urls import reverse
from .models import Photo, Category, Comment, UserProfile, UserLike, CategoryPhoto
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

class BaseTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create(username='tester1', email='test1@example.com')
        self.user2 = User.objects.create(username='tester2', email='test2@example.com')

        # Create categories
        self.category1 = Category.objects.create(categoryName='Nature')
        self.category2 = Category.objects.create(categoryName='Sport')

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
        self.photo1.uploadDate = timezone.now()

        self.photo2 = Photo.objects.create(
            title='Test Photo 2',
            description='This is a test photo 2',
            image='uploads/test2.jpg',
            userID=self.user2
        )
        self.photo2.uploadDate = timezone.now()

        # Associate categories with photos
        CategoryPhoto.objects.create(photoID=self.photo1, categoryID=self.category1)
        CategoryPhoto.objects.create(photoID=self.photo2, categoryID=self.category2)

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

    def test_photo_creation(self):
        """Test that a photo is created correctly"""
        self.assertEqual(self.photo1.title, 'Test Photo 1')
        self.assertEqual(self.photo2.title, 'Test Photo 2')
        self.assertEqual(self.photo1.description, 'This is a test photo 1')
        self.assertEqual(self.photo2.description, 'This is a test photo 2')
        self.assertEqual(self.photo1.image, 'uploads/test1.jpg')
        self.assertEqual(self.photo2.image, 'uploads/test2.jpg')
        self.assertEqual(self.photo1.userID, self.user1)
        self.assertEqual(self.photo2.userID, self.user2)
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

    def test_userlike_creation(self):
        """Test that a like is created correctly"""
        self.assertEqual(self.userlike1.photoID, self.photo1)
        self.assertEqual(self.userlike1.userID, self.user2)
        self.assertEqual(self.userlike2.photoID, self.photo2)
        self.assertEqual(self.userlike2.userID, self.user1)

class CategoryModelTestCase(BaseTestCase):
    def test_category_creation(self):
        """Test that a category is created correctly"""
        self.assertEqual(self.category1.categoryName, 'Nature')

class UserProfileModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()  

        # Create user profile
        self.user = User.objects.create(username='tester', email='test@example.com')
        self.profile = UserProfile.objects.create(user=self.user, profilePicture='profile_pictures/test.jpg')

    def test_userprofile_creation(self):
        """Test that a user profile is created correctly"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.profilePicture, 'profile_pictures/test.jpg')
