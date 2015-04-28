from django.db import models
from django.contrib.auth.models import User


class Zipcode(models.Model):
    code = models.CharField(max_length=6, default='00000')

    def __unicode__(self):
        return self.code


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=2, default='WI')
    preference = models.CharField(max_length=20, default='Restaurants')
    desired_1 = models.CharField(max_length=22, default='')
    desired_2 = models.CharField(max_length=22, default='')
    desired_3 = models.CharField(max_length=22, default='')
    num_businesses_so_far = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username
