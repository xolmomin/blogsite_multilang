from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json, datetime
from django.contrib.auth.models import User
from django.contrib import messages
from blogApp.models import UserProfile, Category, Post

from blogApp.forms import UserRegistration, UpdateProfile, UpdateProfileMeta, UpdateProfileAvatar, \
    SavePost, AddAvatar

category_list = Category.objects.all()
context = {
    'page_title': 'Simple Blog Site',
    'category_list': category_list,
    'category_list_limited': category_list
}


# login
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


# Logout
def logoutuser(request):
    logout(request)
    return redirect('/')


def home(request):
    context['page_title'] = 'Home'
    posts = Post.objects.filter(status=1).all()
    context['posts'] = posts
    print(request.user)
    return render(request, 'home.html', context)


def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            newUser = User.objects.all().last()
            try:
                profile = UserProfile.objects.get(user=newUser)
            except:
                profile = None
            if profile is None:
                UserProfile(user=newUser, dob=data['dob'], contact=data['contact'], address=data['address'],
                            avatar=request.FILES['avatar']).save()
            else:
                UserProfile.objects.filter(id=profile.id).update(user=newUser, dob=data['dob'], contact=data['contact'],
                                                                 address=data['address'])
                avatar = AddAvatar(request.POST, request.FILES, instance=profile)
                if avatar.is_valid():
                    avatar.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username=username, password=pwd)
            login(request, loginUser)
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request, 'register.html', context)


@login_required
def profile(request):
    context = {
        'page_title': "My Profile"
    }

    return render(request, 'profile.html', context)


@login_required
def update_profile(request):
    context['page_title'] = "Update Profile"
    user = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=user)
    context['userData'] = user
    context['userProfile'] = profile
    if request.method == 'POST':
        data = request.POST
        # if data['password1'] == '':
        # data['password1'] = '123'
        form = UpdateProfile(data, instance=user)
        if form.is_valid():
            form.save()
            form2 = UpdateProfileMeta(data, instance=profile)
            if form2.is_valid():
                form2.save()
                messages.success(request, "Your Profile has been updated successfully")
                return redirect("profile")
            else:
                # form = UpdateProfile(instance=user)
                context['form2'] = form2
        else:
            context['form1'] = form
            form = UpdateProfile(instance=request.user)
    return render(request, 'update_profile.html', context)


@login_required
def update_avatar(request):
    context['page_title'] = "Update Avatar"
    user = User.objects.get(id=request.user.id)
    context['userData'] = user
    context['userProfile'] = user.profile
    img = user.profile.avatar.url

    context['img'] = img
    if request.method == 'POST':
        form = UpdateProfileAvatar(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Profile has been updated successfully")
            return redirect("profile")
        else:
            context['form'] = form
            form = UpdateProfileAvatar(instance=user)
    return render(request, 'update_avatar.html', context)


# Category
@login_required
def category_mgt(request):
    categories = Category.objects.all()
    context['page_title'] = "Category Management"
    context['categories'] = categories
    return render(request, 'category_mgt.html', context)


@login_required
def manage_category(request, pk=None):
    # category = Category.objects.all()
    if pk == None:
        category = {}
    elif pk > 0:
        category = Category.objects.filter(id=pk).first()
    else:
        category = {}
    context['page_title'] = "Manage Category"
    context['category'] = category

    return render(request, 'manage_category.html', context)


@login_required
def save_category(request):
    resp = {'status': 'failed', 'msg': ''}
    # if request.method == 'POST':
    #     category = None
    #     if not request.POST['id'] == '':
    #         category = Category.objects.filter(id=request.POST['id']).first()
    #     if not category == None:
    #         form = SaveCategory(request.POST, instance=category)
    #     else:
    #         form = SaveCategory(request.POST)
    # if form.is_valid():
    #     form.save()
    #     resp['status'] = 'success'
    #     messages.success(request, 'Category has been saved successfully')
    # else:
    #     for field in form:
    #         for error in field.errors:
    #             resp['msg'] += str(error + '<br>')
    #     if not category == None:
    #         form = SaveCategory(instance=category)

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_category(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            category = Category.objects.filter(id=id).first()
            category.delete()
            resp['status'] = 'success'
            messages.success(request, 'Category has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Post
@login_required
def post_mgt(request):
    if request.user.profile.user_type == 1:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(author=request.user).all()

    context['page_title'] = "post Management"
    context['posts'] = posts
    return render(request, 'post_mgt.html', context)


@login_required
def manage_post(request, pk=None):
    # post = post.objects.all()
    if pk == None:
        post = {}
    elif pk > 0:
        post = Post.objects.filter(id=pk).first()
    else:
        post = {}
    context['page_title'] = "Manage post"
    context['post'] = post

    return render(request, 'manage_post.html', context)


@login_required
def save_post(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        post = None
        if not request.POST['id'] == '':
            post = Post.objects.filter(id=request.POST['id']).first()
        if not post == None:
            form = SavePost(request.POST, request.FILES, instance=post)
        else:
            form = SavePost(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        resp['status'] = 'success'
        messages.success(request, 'Post has been saved successfully')
    else:
        for field in form:
            for error in field.errors:
                resp['msg'] += str(error + '<br>')
        if not post == None:
            form = SavePost(instance=post)

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_post(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        id = request.POST['id']
        try:
            post = Post.objects.filter(id=id).first()
            post.delete()
            resp['status'] = 'success'
            messages.success(request, 'Post has been deleted successfully.')
        except Exception as e:
            raise print(e)
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_post(request, pk=None):
    context['page_title'] = ""
    if pk is None:
        messages.error(request, "Unabale to view Post")
        return redirect('home-page')
    else:
        post = Post.objects.filter(id=pk).first()
        context['page_title'] = post.title
        context['post'] = post
    return render(request, 'view_post.html', context)


def post_by_category(request, pk=None):
    if pk is None:
        messages.error(request, "Unabale to view Post")
        return redirect('home-page')
    else:
        category = Category.objects.filter(id=pk).first()
        context['page_title'] = category.name
        context['category'] = category
        posts = Post.objects.filter(category=category).all()
        context['posts'] = posts
    return render(request, 'by_categories.html', context)


def categories(request):
    categories = Category.objects.all()
    context['page_title'] = "Category Management"
    context['categories'] = categories
    return render(request, 'categories.html', context)
