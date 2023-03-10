import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Post, User, Follow
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from math import ceil
from django.views.decorators.csrf import csrf_exempt


from .forms import PostForm


@csrf_exempt
def index(request):

    if request.method == "POST":
        if "tweet" in request.POST:
            post_form = PostForm(request.POST)

            if post_form.is_valid():
                tweet = post_form.cleaned_data['tweet1']
                Post.objects.create(publisher=request.user, tweet=tweet)
                return redirect("index")
        else:

            print("takeha takeha takeha")
            data = json.loads(request.body)
            liked_id = data.get("liked_id", "")
            user = request.user
            print(liked_id)
            tweet = Post.objects.get(pk=liked_id)
            liked_by = list(tweet.liked_by.all())
            print(liked_by)

            if user in liked_by:

                tweet.liked_by.remove(user)

            else:
                tweet.liked_by.add(user)

            liked_by = list(tweet.liked_by.all())

            print(liked_by)

            tweet.likes = len(liked_by)
            tweet.save()

            print(len(liked_by))
            # tweet.save()
            # tweet.likes = len(tweet.liked_by)
            return JsonResponse({"likes_count": len(liked_by)}, status=201)
            # print(len(tweet.liked_by))

    post_form = PostForm()
    all_posts = Post.objects.order_by("-date_time")
    me = request.user
    # print(len(all_posts))
    for ss in all_posts:
        print(list(ss.liked_by.all()))
        ss.likes = len(list(ss.liked_by.all()))

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # print(me)

    return render(request, "network/index.html", {
        "new_post": post_form,
        "page_obj": page_obj,
        "me": str(me),

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

    followings_list = Follow.objects.filter(
        follower=request.user, followee_id=user_id)
    ff_list = []
    for ff in followings_list:
        print(ff.follower)
        ff_list.append(str(ff.follower))

    following_count = len(following)
    followers_count = len(followers)
    posts = Post.objects.filter(publisher_id=user_id).order_by("-date_time")
    me = request.user
    username = User.objects.get(pk=user_id)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
                      "page_obj": page_obj,
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
        "page_obj": page_obj

    })


@login_required(login_url='/login')
def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    print(post.serialize())

    return JsonResponse(post.serialize())


@csrf_exempt
@login_required(login_url='/login')
def save_changes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        edited_post = data.get("edited_post", "")
        post_id = data.get("post_id", "")
        print(edited_post)
        print(post_id)
        post = Post.objects.get(pk=post_id)
        post.tweet = edited_post
        post.save()
        return JsonResponse({"edit": edited_post}, status=201)
