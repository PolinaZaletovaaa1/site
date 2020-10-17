from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


from mainapp.models import *


from mainapp.forms import *
from django.contrib.auth import *

from django.urls import reverse

from mainapp.forms import ArticleForm, CustomUserCreationForm
from mainapp.models import Article


@permission_classes((permissions.AllowAny,))
class Login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'registration/login.html'

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('userpage',
                                        kwargs={"username": request.user.username}))
            else:
                return redirect('login')
        else:
            return redirect('login')

    def get(self, request):
        form = AuthenticationForm()
        return Response({'form': form})

    def register(request):
        if request.method == "POST":

            form = CustomUserCreationForm(request.POST)

            if form.is_valid():

                form.save()
            else:
                print(form.errors)
            return redirect('login')
        else:
            form = CustomUserCreationForm()

        return render(request, "registration/register.html", {"form": form})

@permission_classes((permissions.AllowAny,))
class AdminPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_admin_mainpage.html'

    def get(self,request, *args, **kwargs):
        users_list = User.objects.all()
        for i in range(len(users_list)):
            users_list[i].is_active = not users_list[i].is_active
        form = CustomUserCreationForm()
        return Response({'users': users_list, 'form': form})

    def post(self,request, *args, **kwargs):

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('adminpage')

    def delete(request, *args, **kwargs):
        username = kwargs.get('username')
        User.objects.filter(username=username).delete()
        return redirect('adminpage')

    def block(request, *args, **kwargs):
        username = kwargs.get('username')
        User.objects.filter(username=username).update(is_active=False)
        return redirect('adminpage')

    def unblock(request, *args, **kwargs):
        username = kwargs.get('username')
        User.objects.filter(username=username).update(is_active=True)
        return redirect('adminpage')



@permission_classes((permissions.AllowAny,))
class UserPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_mainpage.html'

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            note = form.save(commit=False)

            note.author = request.user

            note.save()
        return redirect(reverse('userpage',
                                kwargs={"username": request.user.username}))

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(author=request.user)
        articleform = ArticleForm()
        return Response({'articleform': articleform, 'articles': articles})


@permission_classes((permissions.AllowAny,))
class FeedPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'feed.html'

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        
        articleform = ArticleForm()
        return Response({'articles': articles})


@permission_classes((permissions.AllowAny,))
class ArticlePage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'article.html'

    def delete(request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)

        article.delete()
        return redirect(reverse('userpage',
                                kwargs={"username": request.user.username}))

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        field_object = Article._meta.get_field('total_views')
        field_value = field_object.value_from_object(article)
        Article.objects.filter(id=article_id).update(total_views=field_value + 1)
        return Response({'article': article})




@permission_classes((permissions.AllowAny,))
class ArticleEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'article_edit.html'

    def post(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            form.save()
        return redirect(reverse('articlepage',
                                kwargs={"article_id": article_id}))

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = Article.objects.get(id=article_id)
        articleform = ArticleForm(instance=article)
        return Response({'articleform': articleform, 'article': article})


