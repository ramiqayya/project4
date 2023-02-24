from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, User, Follow
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from math import ceil

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
    # print(len(all_posts))
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "new_post": post_form,
        "posts": all_posts,
        'page_obj': page_obj
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
def profile(request, user_id):

    following = Follow.objects.filter(followee_id=user_id)
    followers = Follow.objects.filter(follower_id=user_id)
    # print(followers)
    # followees_list = []
    followings_list = Follow.objects.filter(
        follower=request.user, followee_id=user_id)
    ff_list = []
    for ff in followings_list:
        print(ff.follower)
        ff_list.append(str(ff.follower))
    print(ff_list)
    # print(followings_list)
    # for follower in followers:
    # print(follower.followee)
    # followees_list.append(follower.followee)
    # print(followees_list)
    following_count = len(following)
    followers_count = len(followers)
    posts = Post.objects.filter(publisher_id=user_id).order_by("-date_time")
    me = request.user
    username = User.objects.get(pk=user_id)
    if request.method == "POST":
        if "follow" in request.POST:
            Follow.objects.create(follower=me, followee=username)
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))

        elif "unfollow" in request.POST:
            unfollow = Follow.objects.get(follower=me, followee=username)
            unfollow.delete()
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))

    return render(request, "network/profile.html",
                  {
                      "following": following_count,
                      "followers": followers_count,
                      "username": str(username.username),
                      "posts": posts,
                      "me": str(me),
                      "f_list": ff_list,
                      "user_id": user_id


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

    paginator = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": allposts,
        "page_obj": page_obj

    })

    # def all_posts(request):
    #     all_posts = Post.objects.order_by("-date_time")
    #     return render(request, "network/allposts.html",

    #                   {"posts": all_posts})
