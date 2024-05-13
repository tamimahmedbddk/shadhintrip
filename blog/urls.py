from django.urls import path
from blog import views

urlpatterns = [
    # Other URL patterns for your project
    path('', views.blog_home, name='blog_home'),
    path('fetch_posts/', views.fetch_blog_posts, name='fetch_blog_posts'),
    path("<slug:slug>/", views.blog_details, name="blog_details"),
]
