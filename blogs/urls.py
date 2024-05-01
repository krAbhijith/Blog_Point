from django.urls import include, path

from blogs.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog-update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog-delete'),
    path('archive/<int:pk>/', BlogArchiveView.as_view(), name='blog-archive'),
    path('save/<int:pk>/', BlogSaveView.as_view(), name='blog-save'),
    path('Like/', BlogLikeView.as_view(), name='blog-Like'),
    path('comment/', BlogCommentView.as_view(), name='blog-comment'),
]