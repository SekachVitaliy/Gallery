from django.db import models


class Photo(models.Model):
    description = models.CharField(max_length=100, null=False, verbose_name='Описание')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=False, blank=False, verbose_name='Категория')
    image = models.ImageField(null=False, upload_to='', blank=False, verbose_name='Фотография')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Фотографии'
        verbose_name = 'Фотография'
        ordering = ['-published']


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False,  db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ['name']
