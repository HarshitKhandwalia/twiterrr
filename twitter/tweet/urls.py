from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("", views.tweet_list,name='tweet_list'),
    path('test/', views.test_view, name='test_view'),
    path('create/', views.tweet_create,name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit,name='tweet_edit'),
    path('<int:tweet_id>/del/', views.tweet_del,name='tweet_del'),
    path('register/',views.register,name='register'),
    # Removed custom media handler - using Django's built-in static file serving instead
]