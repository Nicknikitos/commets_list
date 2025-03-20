import os
from PIL import Image
import bleach
from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import Comment


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'text', 'image', 'file']
        widgets = {
            'homepage': forms.URLInput(attrs={'placeholder': 'example.com'})
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('Поле не может быть пустым')

        allowed_tags = ['a', 'code', 'i', 'strong']
        allowed_attrs = {'a': ['href', 'title']}

        cleaned_text = bleach.clean(text, tags=allowed_tags, attributes=allowed_attrs, strip=True)

        return cleaned_text

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endwith('.txt'):
                raise forms.ValidationError('Файл должен быть формата TXT.')
            if file.size > 100 * 1024:
                raise forms.ValidationError('Размер файла не должен быть больше 100 КБ.')

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            try:
                img = Image.open(image)
                max_width, max_height = 320, 240
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height))  # Уменьшаем изображение
                    if hasattr(image, 'path') and os.path.exists(image.path):
                        img.save(image.path)  # Сохраняем уменьшенную версию
            except Exception as e:
                raise ValidationError(f"Ошибка обработки изображения: {e}")
        return image

