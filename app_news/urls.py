from django.urls import path
from .views import NewsViews, AddNews, EditNews, CommentNews, UnpublishedNewsViews, \
    NewsLoginView, RegisterUser, logout_view


urlpatterns = [
    path('', NewsViews.as_view(), name='news'),
    path('unpublished_news_list/', UnpublishedNewsViews.as_view(), name='unpublished_news'),
    path('add_news/', AddNews.as_view(), name='add_news'),
    path('<int:news_id>/edit_news/', EditNews.as_view(), name='edit_news'),
    path('<int:news_id>/comment_news/', CommentNews.as_view(), name='comment_news'),
    #path('<int:news_id>/news_detail/', DetailsNewsViews.as_view(), name='news_detail'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', NewsLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
