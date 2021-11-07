from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from app_news.models import News, Comments
from django.views.generic import ListView, CreateView
from app_news.forms import NewsForm, CommentsForm
from django.contrib.auth.views import LoginView


class NewsViews(ListView):
    model = News
    template_name = "news/news_list.html"
    queryset = News.objects.filter(flag_active='a')


class UnpublishedNewsViews(ListView):
    model = News
    template_name = "news/unpublished_news_list.html"
    queryset = News.objects.filter(flag_active='n')


'''
class DetailsNewsViews(DetailView):
    model = News
    template_name = "news/comment_news.html"
    pk_url_kwarg = 'news_id'
    context_object_name = 'news_detail'
'''


class AddNews(CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"


class EditNews(View):
    def get(self, request, news_id):
        edit_news = News.objects.get(id=news_id)
        edit_form = NewsForm(instance=edit_news)
        return render(request, "news/edit_news.html", context={"edit_form": edit_form, "id": news_id})

    def post(self, request, news_id):
        edit_news = News.objects.get(id=news_id)
        edit_form = NewsForm(request.POST, instance=edit_news)

        if edit_form.is_valid():
            edit_news.save()
            return redirect("/")
        return render(request, "news/edit_news.html", context={"edit_form": edit_form, "id": news_id})


class CommentNews(View):
    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        comments = Comments.objects.filter(news=news)
        comment_form = CommentsForm()
        return render(request, "news/comment_news.html", context={"comment_news": news,
                                                                  "comment_list": comments,
                                                                  "comment_form": comment_form})

    def post(self, request, news_id):
        news = News.objects.get(id=news_id)
        comment_form = CommentsForm(request.POST)
        if request.user.is_authenticated:
            comments = Comments.objects.filter(news=news)
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                form.name = request.user
                form.text = comments
                form.save()
                return redirect("/")
        else:
            if comment_form.is_valid():
                Comments.objects.create(news=news, **comment_form.cleaned_data)
                return redirect("/")
        comments = Comments.objects.filter(news=news)
        comment_form = CommentsForm()
        return render(request, "news/comment_news.html", context={"comment_news": news,
                                                                  "comment_list": comments,
                                                                  "comment_form": comment_form})


class NewsLoginView(LoginView):
    template_name = 'users/login.html'


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


def logout_view(request):
    logout(request)
    return HttpResponse('Вы успешно вышли из под своей учетной записи!')
