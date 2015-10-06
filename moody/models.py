from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

class Album(models.Model):
    name = models.CharField(max_length=128) #, unique=True)
    artist = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()
    img = models.URLField()
    spotifyid = models.CharField(max_length=128), #unique=True)

    def save(self, *args, **kwargs):
        if self.views < 0:
            self.views = 0
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Genre(models.Model):
    gname = models.CharField(max_length=128, null=True)
    albums = models.ManyToManyField(Album, blank = True)
    gslug = models.SlugField()

    def save(self, *args, **kwargs):
        self.gslug = slugify(self.gname)
        super(Genre, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.gname
