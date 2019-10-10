from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:product_id>', views.details, name='details'),
    path('signup', views.signup, name='signup'),
    path('create', views.create, name='create'),
    path('<int:product_id>/upvote', views.upvote, name='upvote'),
]