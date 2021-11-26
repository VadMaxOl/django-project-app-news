from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from app_news.models import News, Comments, Profile
from django.views.generic import ListView, CreateView, DetailView
from app_news.forms import NewsForm, CommentsForm, RegistrationUserForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied


class NewsViews(ListView):
    model = News
    template_name = "news/news_list.html"
    queryset = News.objects.filter(flag_active='a')


def addnews(request):
    if not request.user.has_perm('app_news.can_verification_user'):
        raise PermissionDenied
    form = NewsForm(request.POST)
    user_count = Profile.objects.get(user=request.user)
    if form.is_valid():
        user_count.count_news += 1
        user_count.save()
        form.save()
        return redirect("/")
    return render(request, 'news/add_news.html', {'form': form})


class UnpublishedNewsViews(ListView):
    model = News
    template_name = "news/unpublished_news_list.html"
    queryset = News.objects.filter(flag_active='n')


class FilterTagNewsViews(ListView):
    model = News
    template_name = "news/filter_news_list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = News.objects.filter(
            Q(content__icontains=query) | Q(created_at__icontains=query)
        )
        return queryset

'''
class DetailsNewsViews(DetailView):
    model = News
    template_name = "news/comment_news.html"
    pk_url_kwarg = 'news_id'
    context_object_name = 'news_detail'



class AddNews(CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"



@permission_required('app_news.can_add_news')
def addnews(request):
    form = News.objects.all()
    return render(request, 'news/add_news.html', {'add_news': form})
'''


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
        news = get_object_or_404(News, pk=news_id)
        comment_form = CommentsForm(request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                form.news = news
                form.user = request.user
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


def register_user(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            user = form.save()
            Profile.objects.create(
                user=user,
                phone=phone,
                city=city,
            )
            return redirect('/')
    else:
        form = RegistrationUserForm
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponse('Вы успешно вышли из под своей учетной записи!')


class UsersViews(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = 'users'


class DetailsUserViews(DetailView):
    model = User
    template_name = "users/user_detail.html"
    pk_url_kwarg = 'user_id'
    context_object_name = 'user_detail'
