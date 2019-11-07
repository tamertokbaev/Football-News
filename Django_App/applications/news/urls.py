from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/<int:news_id>/', views.one_by_one, name='one_by_one'),
    path('news/<int:news_id>/leave_comment', views.leave_comment, name='leave_comment'),
    path('accounts/register/', views.register_user, name='register'),
    path('archive/', views.archive, name='archive'),
    # path('search/<slug:search_str>/', views.search, name='search')
    path('search/', views.search, name='search'),
]
