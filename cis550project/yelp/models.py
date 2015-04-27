from django.db import models
from django.contrib.auth.models import User


class Zipcode(models.Model):
    code = models.CharField(max_length=6, default='00000')

    def __unicode__(self):
        return self.code


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=2, default='WI')
    picture = models.URLField(blank=True)

    def __unicode__(self):
        return self.user.username