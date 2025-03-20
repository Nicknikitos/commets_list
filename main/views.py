from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Comment
from .forms import CommentForm


def comment_list(request):
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            parent_id = request.POST.get('parent')  # Получаем ID родительского комментария
            comment = form.save(commit=False)  # Создаем объект комментария, но не сохраняем

            if parent_id:
                comment.parent_id = int(parent_id)  # Устанавливаем родительский комментарий

            # Если в форме было загружено изображение, сохраняем его
            if 'image' in request.FILES:
                comment.image = request.FILES['image']

            comment.save()  # Сохраняем комментарий с изображением, если оно есть
            return redirect('comments_list')  # Перезагружаем страницу

    else:
        form = CommentForm()

    comments = Comment.objects.filter(parent=None).prefetch_related('replies')  # Загружаем родительские и дочерние комментарии
    paginator = Paginator(comments, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/comments_list.html', {'page_obj': page_obj, 'form': form})
