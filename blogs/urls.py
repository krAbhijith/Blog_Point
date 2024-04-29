from django.urls import include, path

from blogs.views import *

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('create/', BlogCreateView.as_view(), name='create-blog'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog-update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog-delete'),
    path('archive/<int:pk>/', BlogArchiveView.as_view(), name='blog-archive'),
    path('Like/<int:pk>/', BlogLike.as_view(), name='blog-Like'),
    path('comment/<int:pk>/', BlogComment.as_view(), name='blog-comment'),
]