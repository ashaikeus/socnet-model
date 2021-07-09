from django.shortcuts import render
from .models import *


def profile(request):
    pf = Profile.objects.get(pk=1)
    return render(request, 'profile_page.html', {'pf': pf})


def feed(request):
    pf = Profile.objects.get(nickname='rlyeh')
    posts = [post for post in Post.objects.order_by('-created_date') if post.author in pf.following.all()]
    return render(request, 'feed.html', {'feed': posts})
