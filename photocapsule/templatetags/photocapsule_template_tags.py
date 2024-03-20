from django import template
from photocapsule.models import UserLike

register = template.Library()

@register.simple_tag
def hasLikedPhoto(user, photo):
    try:
        like = UserLike.objects.get(photoID=photo, userID=user)
        return "Unlike"
    except:
        return "Like"
