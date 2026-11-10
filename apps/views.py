import os

from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout

from .models import Post, PostMedia, User


IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.webm'}


def get_media_type(file):
    extension = os.path.splitext(file.name)[1].lower()
    if extension in IMAGE_EXTENSIONS:
        return PostMedia.MediaType.IMAGE
    if extension in VIDEO_EXTENSIONS:
        return PostMedia.MediaType.VIDEO
    return None


def get_post_media_error(post_type, media_types):
    if post_type not in Post.PostType.values:
        return "Post turini tanlang!"
    if None in media_types:
        return "Faqat rasm (jpg, jpeg, png, gif, webp) yoki video (mp4, mov, webm) yuklash mumkin!"

    images = media_types.count(PostMedia.MediaType.IMAGE)
    videos = media_types.count(PostMedia.MediaType.VIDEO)

    if post_type == Post.PostType.PHOTO and (images == 0 or videos > 0):
        return "Photo post uchun kamida bitta rasm tanlang, video qo'shmang!"
    if post_type == Post.PostType.VIDEO and (videos == 0 or images > 0):
        return "Video post uchun kamida bitta video tanlang, rasm qo'shmang!"
    if post_type == Post.PostType.PHOTO_VIDEO and (images == 0 or videos == 0):
        return "Photo + video post uchun kamida bitta rasm va bitta video tanlang!"
    if post_type == Post.PostType.REELS and (videos != 1 or images > 0):
        return "Reels uchun faqat bitta video tanlang!"
    return None



def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        db_user = User.objects.filter(username=username).first()
        if db_user and db_user.check_password(password):
            # print("Siz bazada borsiz va parol ham to'g'ri!")
            login(request, db_user)
            return redirect('post_list')
        else:
            print("Username yokida parol xato!")
            # task2 Username yokida parol xatoliga sayt dachiqsishi kerak task1 kabi bajariladi
        
    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        username = data.get('username')
        password = data.get('password')
        date = data.get('date')

        db_user = User.objects.filter(username=username).exists()
        # print(f"<<>>><<>><><{db_user}<><><><><><><>>")
        if not db_user:
            new_user = User.objects.create(
                first_name=name,
                username=username,
                password=make_password(password),
                birthday=date
            )
            new_user.save()
            return redirect('post_list')
        else:
            pass
            # task1 Bunday username band ekanligi haqida foydalanuvchiga habar berish kerak
            # buning uchun django.message ishatiladi

    return render(request, 'register.html')


@login_required(login_url='login')
def posts_view(request):
    post_list = Post.objects.prefetch_related('media')
    return render(request, 'posts.html', context={'post_list': post_list})


@login_required(login_url='login')
def post_create_view(request):
    context = {'post_types': Post.PostType.choices}

    if request.method == "POST":
        about = request.POST.get("about")
        location = request.POST.get("location")
        post_type = request.POST.get("post_type")
        files = request.FILES.getlist("media")
        media_types = [get_media_type(file) for file in files]

        error = get_post_media_error(post_type, media_types)
        if error:
            context.update(error=error, about=about, location=location, post_type=post_type)
            return render(request, 'post-create.html', context=context)

        with transaction.atomic():
            new_post = Post.objects.create(
                author=request.user,
                post_type=post_type,
                about=about,
                location=location
            )
            for file, media_type in zip(files, media_types):
                PostMedia.objects.create(post=new_post, media_type=media_type, file=file)
        return redirect('post_list')

    return render(request, 'post-create.html', context=context)



def profile_view(request):
    return render(request, 'profile.html')

