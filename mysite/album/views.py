from django.shortcuts import redirect, render

from .models import Category, Photo


def main_page(request):
    images = Photo.objects.all()
    categories = Category.objects.all()
    context = {
        'images': images,
        'categories': categories,
    }
    return render(request, 'album/main.html', context)


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


def view_image(request, image_id):
    image = Photo.objects.get(pk=image_id)
    context = {
        'image': image,
    }
    return render(request, 'album/view_image.html', context)


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
