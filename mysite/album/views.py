from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm
from .models import Category, Photo


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main_page')

    return render(request, 'album/login_register.html', {'page': page})


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
    images = Photo.objects.all()
    categories = Category.objects.all()
    context = {
        'images': images,
        'categories': categories,
    }
    return render(request, 'album/main.html', context)


@login_required(login_url='login')
def category_photos(request, category_id):
    categories = Category.objects.all()
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
    data = request.POST
    images = request.FILES.getlist('images')
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    if request.method == 'POST':
        if data['category'] != 'none':
            category = Category.objects.get(pk=data['category'])
        elif data['category_new'] != 'none':
            category = Category.objects.create(
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
