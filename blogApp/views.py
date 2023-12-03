from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User

from blogApp.models import Post, Comment
# Create your views here.


@login_required()
def dashboardView(request):
    return render(request,'home.html')

def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render(request,'register.html',{'form':form})

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_at']

   
class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    
class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    #fields = '__all__'
    # fields = ('title','body')

 
class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    #fields = '__all__'
    
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = reverse_lazy('home')
    
    
    
   
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title', 'body']

 
class DeletePostView(DeleteView):
    model= Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

 
class UserDetailView(DetailView):
    model = User
    template_name = 'profile.html'

@login_required()    
def SearchBlog(request):
    if request.method == "POST":
        blog = request.POST['blog']
        blogs = Post.objects.filter(title__contains=blog)
        blogbody = Post.objects.filter(body__contains=blog)
        
        return render(request,'search_blog.html', {'blog':blog, 'blogs':blogs, 'blogbody':blogbody})
    else:
        return render(request,'search_blog.html')