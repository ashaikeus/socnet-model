from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from random import randrange


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(default="Some text post you haven't saved yet.")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_long = models.BooleanField(default=False)

    def publish(self):
        if len(self.text) > 280:
            self.is_long = True
        else:
            self.is_long = False
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.text[:30]


class Field(models.Model):
    name = models.CharField(max_length=25)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    handle = models.CharField(max_length=16, default='handle')
    nickname = models.CharField(max_length=50, default='Nickname')
    tags = models.ManyToManyField(Field, blank=True)
    pfp = models.FileField(default="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAAA1BMVEWw3+W05AztAAAASElEQVR4nO3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIC3AcUIAAFkqh/QAAAAAElFTkSuQmCC",
                           blank=True)
    bio = models.TextField(blank=True, max_length=400)
    following = models.ManyToManyField(User, symmetrical=False, blank=True, related_name='followers')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        '''if self.user.username in User.objects.all():
            self.user.username = self.user.username + randrange(1000, 9999)'''
        self.handle = self.user.username
        self.nickname = self.user.username

    def __str__(self):
        return self.nickname


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

