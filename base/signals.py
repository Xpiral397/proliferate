
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.models import  User
from base.models import Profile

def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != "":
        user.username = user.email
pre_save.connect(updateUser, sender=User)


"""
def profile(sender,instance,created,**kwargs):

    if created:
        profile =Profile.objects.create(
            user = instance,
            email = instance.email,
            full_name = instance.first_name,
            first_name = instance.first_name

        )

post_save.connect(profile, sender=User)
"""
