from datetime import date
from typing import Any
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, RedirectView
from .models import Blog, Like, Comment

class Home(ListView):
    model : Blog
    template_name = 'blog/home.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.filter(is_archived = False).order_by('-pk')
    
class BlogCreateView(View):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog/blog.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        user = request.user
        today = date.today()
        #print(title, desc, user, today)
        Blog.objects.create(title=title, desc=desc, owner=user, date_posted=today)
        return redirect('home')
    
    

class BlogUpdateView(View):
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        return blog
    
    def get(self, request, **kwargs):
        context = self.get_queryset()
        return render(request, 'blog/blog.html', {'blog' : context})
    
    def post(self, request, **kwargs):
        blog = self.get_queryset()
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        blog.title = title
        blog.desc = desc
        blog.save()
        return redirect('home')

class BlogDeleteView(RedirectView):
    query_string = False
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        blog.delete()
        return reverse(self.pattern_name)


    # def get(self, request, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     blog = get_object_or_404(Blog, pk=pk)
    #     blog.delete()
    #     return redirect('home')

class BlogArchiveView(RedirectView):
    query_string = False
    pattern_name = 'home'

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        blog.is_archived = True
        blog.save()
        return reverse(self.pattern_name)
    
class BlogLike(View):
    def get(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        user = request.user
        today = date.today()
        if(Like.objects.filter(blog=blog, user=user)):
            Like.objects.filter(blog=blog, user=user).delete()
        else:
            Like.objects.create(date_liked = today, user = user, blog = blog)
        return redirect('home')
    
class BlogComment(View):

    def post(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        comment = request.POST.get('inp-comment')
        today = date.today()
        Comment.objects.create(comment=comment, date_commented=today, user=request.user, blog=blog)
        return redirect('home')

    
