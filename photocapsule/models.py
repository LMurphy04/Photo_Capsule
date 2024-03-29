from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePicture = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.png') 
    
    def __str__(self):
        return self.user.username

class Category(models.Model):
    categoryName=models.CharField(max_length=25, unique=True)
    
    def __str__(self):
        return self.categoryName

class Photo(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='uploads', blank=False)
    likes = models.IntegerField(default=0)
    uploadDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class UserLike(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    photoID = models.ForeignKey(Photo, on_delete=models.CASCADE)
    
class CategoryPhoto(models.Model):
    photoID = models.ForeignKey(Photo, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    
class Comment(models.Model):
    photoID = models.ForeignKey(Photo, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    uploadDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.userID) + ' ' + str(self.photoID) + ' ' + str(self.uploadDate)