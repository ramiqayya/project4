from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, User, Follow
from django.contrib.auth.decorators import login_required

from .forms import PostForm


def index(request):

    if request.method == "POST":
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            print("tsee tsee")
            post = post_form.cleaned_data['post']
            Post.objects.create(publisher=request.user, tweet=post)
            return redirect("index")

    else:
        post_form = PostForm()
    all_posts = Post.objects.order_by("-date_time")

    return render(request, "network/index.html", {
        "new_post": post_form,
        "posts": all_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='/login')
def profile(request):
    following = Follow.objects.filter(followee=request.user)
    followers = Follow.objects.filter(follower=request.user)
    following_count = len(following)
    followers_count = len(followers)
    posts = Post.objects.filter(publisher=request.user).order_by("-date_time")

    return render(request, "network/profile.html",
                  {
                      "following": following_count,
                      "follwers": followers_count,
                      "username": request.user,
                      "posts": posts

                  }
                  )


@login_required(login_url='/login')
def following(request):
    followings = Follow.objects.filter(follower=request.user)
    allposts = []

    for following in followings:
        print(following.followee.id)
        posts = Post.objects.filter(publisher=following.followee)
        for post in posts:
            print(post)
            allposts.append(post)

    return render(request, "network/following.html", {
        "posts": allposts
    })

    # def all_posts(request):
    #     all_posts = Post.objects.order_by("-date_time")
    #     return render(request, "network/allposts.html",

    #                   {"posts": all_posts})
