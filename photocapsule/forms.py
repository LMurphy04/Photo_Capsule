from django import forms
from django.contrib.auth.models import User
from photocapsule.models import UserProfile, Photo, Category, CategoryPhoto

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profilePicture']
        
        
class PhotoForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'userID', 'likes']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['likes'].widget = forms.HiddenInput()
        self.fields['userID'].widget = forms.HiddenInput()
        self.fields['description'].required = False
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_categories(instance)
        return instance
    
    def save_categories(self, instance):
        selected_categories = self.cleaned_data['categories']
        for category in selected_categories:
            CategoryPhoto.objects.create(photoID=instance.pk, categoryID=category.pk)
        

