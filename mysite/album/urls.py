

from django.urls import path
from .views import main_page, category_photos, view_image, add_image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', main_page, name='main_page'),
    path('category/<int:category_id>', category_photos, name='category_photos'),
    path('photo/<int:image_id>', view_image, name='view_image'),
    path('add_photo', add_image, name='add_image')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
