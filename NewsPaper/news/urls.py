from django.urls import path
from .views import (NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete, SearchNewsList, make_me_author,
                    CategoryList, NewsCategoryList)


urlpatterns = [
   path('', NewsList.as_view(), name="news"),
   path('<int:pk>', NewsDetail.as_view(), name="post_detail"),
   path('create/', PostCreate.as_view(), name="news_create"),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('search/', SearchNewsList.as_view(), name="search_news"),
   path('makeauthor/', make_me_author, name = 'makeauthor'),
   path('category/', CategoryList.as_view(), name="category"),
   path('category/content/', NewsCategoryList.as_view(), name="news_category"),
]