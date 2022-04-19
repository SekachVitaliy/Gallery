from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from .models import Category, Photo


def loginUser(request):
    page = 'login'
    error_auth, user_auth = '', ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main_page')
        elif User.objects.filter(username=username):
            error_auth = 'Неверный пароль'
            user_auth = username
        else:
            error_auth = 'Неверное имя пользователя или пароль'
    return render(request, 'album/login_register.html',
                  {'page': page, 'error_auth': error_auth, 'user_auth': user_auth})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('main_page')
    context = {'form': form, 'page': page}
    return render(request, 'album/login_register.html', context)


@login_required(login_url='login')
def main_page(request):
    user = request.user
    category = request.GET.get('category')
    if category is None:
        images = Photo.objects.filter(category__user=user)
    else:
        images = Photo.objects.filter(
            category__name=category, category__user=user)
    categories = Category.objects.filter(user=user)
    context = {
        'images': images,
        'categories': categories,
    }
    return render(request, 'album/main.html', context)


@login_required(login_url='login')
def category_photos(request, category_id):
    user = request.user
    categories = user.category_set.all()
    category = Category.objects.get(pk=category_id)
    images_by_category = Photo.objects.filter(category=category)
    context = {
        'images': images_by_category,
        'categories': categories,
        'category': category,
    }
    return render(request, 'album/category_photos.html', context)


@login_required(login_url='login')
def view_image(request, image_id):
    image = Photo.objects.get(pk=image_id)
    context = {
        'image': image,
    }
    return render(request, 'album/view_image.html', context)


@login_required(login_url='login')
def add_image(request):
    user = request.user
    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(pk=data['category'])
        elif data['category_new'] != '':
            category = Category.objects.create(
                user=user,
                name=data['category_new']
            )
        else:
            category = None
        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('main_page')
    context = {
        'categories': categories
    }
    return render(request, 'album/add_photo.html', context)
