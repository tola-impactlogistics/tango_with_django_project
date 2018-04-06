# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
    	# Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
            #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        self.views = self.views >= 0
        super(Category, self).save(*args, **kwargs)
        

    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    first_visit = models.DateField(null=True)
    last_visit = models.DateField(null=True)

    def __str__(self):      #For Python 2, use __str__ on Python 3
        return self.title
    
    #def first_visited(self):      #For Python 2, use __str__ on Python 3
    #    return self.first_visit == datetime.timedelta(days=0)

    #def last_visited(self):      #For Python 2, use __str__ on Python 3
    #    return self.last_visit == timezone.now()

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, unique=True)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to ='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
    @property
    def image_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url

