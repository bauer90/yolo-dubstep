from django.db import models


class Zipcode(models.Model):
    code = models.CharField(max_length=6, default='00000')

    def __unicode__(self):
        return self.code