from django.contrib import admin
from photocapsule.models import *

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(UserLike)
admin.site.register(CategoryPhoto)
admin.site.register(Comment)