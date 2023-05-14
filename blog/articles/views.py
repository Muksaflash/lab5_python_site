# -*- coding: utf-8 -*-

from .models import Article
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect




def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        print(f"post: {post}")
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        print("Article.DoesNotExist")
        raise Http404
        
@login_required
def create_post(request):
    if request.method == "POST":
        # обработать данные формы, если метод POST
        form = {
            'text': request.POST["text"], 'title': request.POST["title"]
        }
        # в словаре form будет храниться информация, введенная пользователем
        if form["text"] and form["title"]:
            # если поля заполнены без ошибок
            if Article.objects.filter(title=form["title"]).exists():
                # если статья с таким названием уже существует
                form['errors'] = "Статья с таким названием уже существует"
                return render(request, 'create_post.html', {'form': form})
            else:
                article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=article.id)
                # перейти на страницу поста
        else:
            # если введенные данные некорректны
            form['errors'] = "Не все поля заполнены"
            return render(request, 'create_post.html', {'form': form})
    else:
        # просто вернуть страницу с формой, если метод GET
        return render(request, 'create_post.html', {})


