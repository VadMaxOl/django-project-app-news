from django.urls import path
from .views import NewsViews, AddNews, EditNews, CommentNews, UnpublishedNewsViews, \
    NewsLoginView, logout_view, UsersViews, register_user, DetailsUserViews, FilterTagNewsViews

urlpatterns = [
    path('', NewsViews.as_view(), name='news'),
    path('unpublished_news_list/', UnpublishedNewsViews.as_view(), name='unpublished_news'),
    path('filter_news_list/', FilterTagNewsViews.as_view(), name='filter_news'),
    path('add_news/', AddNews.as_view(), name='add_news'),
    path('<int:news_id>/edit_news/', EditNews.as_view(), name='edit_news'),
    path('<int:news_id>/comment_news/', CommentNews.as_view(), name='comment_news'),
    path('<int:user_id>/user_detail/', DetailsUserViews.as_view(), name='user_detail'),
    path('register/', register_user, name='register'),
    path('accounts/login/', NewsLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/account/', UsersViews.as_view(), name='users'),
]
