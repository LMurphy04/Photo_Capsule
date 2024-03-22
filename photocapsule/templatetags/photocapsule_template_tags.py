from django import template
from photocapsule.models import UserLike

register = template.Library()

@register.simple_tag
def hasLikedPhoto(user, photo): # Used on Photo Details page load, checks if user has liked photo before
    try:
        like = UserLike.objects.get(photoID=photo, userID=user)
        return "Unlike" # If has liked, set button to Unlike
    except:
        return "Like" # If hasn't, set button to Like