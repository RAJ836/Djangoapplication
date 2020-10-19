from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import (ListView, DetailView,
                               CreateView, UpdateView,
                                  DeleteView)
from django.contrib import messages
from django.contrib.auth.mixins import  LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
from .models import Post
from django.contrib.auth.models import User



def home(request):
    posts=Post.objects.all()
    context={
        'posts':posts
    }
    return render(request,'blog/home.html',context=context)

class PostListView(ListView):
    model = Post
    #<app>/<model>_<viewtype>.html
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    #<app>/<model>_<viewtype>.html
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user= get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    # overwriting the method to assign the author before saving the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # overwriting the method to assign the author before saving the post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # to check that the author of the post is the current_user
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'blog/about.html')

