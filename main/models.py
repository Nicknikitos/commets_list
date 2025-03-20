import os
from PIL import Image
from django.db import models
from django.core.exceptions import ValidationError


def validate_image(image):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Недопустимый формат файла. Возможны только JPG, PNG, GIF')


class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='comments_images/', null=True, blank=True)
    file = models.FileField(upload_to='comments_file/', null=True, blank=True)

    def __str__(self):
        return f'Comment by {self.username} at {self.created_at}'

    class Meta:
        ordering = ['-created_at']  # Сортировка по убыванию LIFO

    def save(self, *args, **kwargs):
        """Переопределяем сохранение, чтобы обрабатывать изображения"""
        super().save(*args, **kwargs)  # Сначала сохраняем объект

        if self.image:
            image_path = self.image.path
            img = Image.open(image_path)

            if img.width > 320 or img.height > 240:
                img.thumbnail((320, 240))  # Пропорционально уменьшаем
                img.save(image_path)  # Перезаписываем файл
