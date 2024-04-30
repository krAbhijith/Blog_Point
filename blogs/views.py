from datetime import date
from typing import Any
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, RedirectView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog, Like, Comment



class Home(LoginRequiredMixin, ListView):
    model : Blog
    template_name = 'blog/home.html'
    context_object_name = 'blogs'

    login_url = 'register-account'
    redirect_field_name = 'redirected_to'

    def get_queryset(self):
        return Blog.objects.filter(is_archived = False).order_by('-pk')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all()
        context['comments_dict'] = comments  # Pass comments dictionary to the template
        return context
    
# class BlogCreateView(View):
#     model = Blog
#     context_object_name = 'blog'
#     template_name = 'blog/blog.html'

#     def get(self, request):
#         return render(request, self.template_name)
    
#     def post(self, request):
#         title = request.POST.get('title')
#         desc = request.POST.get('desc')
#         user = request.user
#         today = date.today()
#         #print(title, desc, user, today)
#         Blog.objects.create(title=title, desc=desc, owner=user, date_posted=today)
#         return redirect('home')


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'desc']
    template_name = 'blog/blog.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.date_posted = date.today()
        return super().form_valid(form)    
    

# class BlogUpdateView(View):
    
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         blog = get_object_or_404(Blog, pk=pk)
#         return blog
    
#     def get(self, request, **kwargs):
#         context = self.get_queryset()
#         return render(request, 'blog/blog.html', {'blog' : context})
    
#     def post(self, request, **kwargs):
#         blog = self.get_queryset()
#         title = request.POST.get('title')
#         desc = request.POST.get('desc')
#         blog.title = title
#         blog.desc = desc
#         blog.save()
#         return redirect('home')


class BlogUpdateView(UpdateView):
    model = Blog
    template_name = "blog/blog.html"
    fields = ['title', 'desc']
    success_url = reverse_lazy('home')
    #context_object_name = 'blog' default model name in lower case aayirikum



class BlogDeleteView(RedirectView):
    query_string = False
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        blog.delete()
        return reverse(self.pattern_name)



class BlogArchiveView(RedirectView):
    query_string = False
    pattern_name = 'home'

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        pk = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=pk)
        blog.is_archived = True
        blog.save()
        return reverse(self.pattern_name)
    


class BlogLikeView(View):
    def get(self, request, **kwargs):
        pk = self.request.GET.get('blog_id')
        blog = get_object_or_404(Blog, pk=pk)
        user = request.user
        today = date.today()
        if(Like.objects.filter(blog=blog, user=user)):
            Like.objects.filter(blog=blog, user=user).delete()
        else:
            Like.objects.create(date_liked = today, user = user, blog = blog)
        return redirect('home')



# class BlogCommentView(CreateView):
#     model = Comment
#     fields = ['comment']
#     success_url = reverse_lazy('home')
#     template_name = 'blog/home.html'

#     def form_valid(self, form):
#         print('hello')
#         form.instance.date_commented = date.today()
#         form.instance.user = self.request.user
#         form.instance.blog = get_object_or_404(Blog, pk=1)
#         return super().form_valid(form)
        



class BlogCommentView(View):

    def post(self, request, **kwargs):
        pk = self.request.POST.get('blog_id')
        blog = get_object_or_404(Blog, pk=pk)
        comment = request.POST.get('comment_text')
        today = date.today()
        Comment.objects.create(comment=comment, date_commented=today, user=request.user, blog=blog)
        return redirect('home')

    
