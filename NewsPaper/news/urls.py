from django.urls import path
from .views import NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete, SearchNewsList


urlpatterns = [
   path('', NewsList.as_view(), name="news"),
   path('<int:pk>', NewsDetail.as_view(), name="post_detail"),
   path('create/', PostCreate.as_view(), name="news_create"),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('search/', SearchNewsList.as_view(), name="search_news"),
]