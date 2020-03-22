#===========================
#blog/views.py
#===========================
#--------------------------------------------------
#IMPORTS
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                DetailView, CreateView,
                                UpdateView, DeleteView)
                                
#####################################################
#Classes
#####################################################
#--------------------------------------------------
#Class: AboutView
#View for about
class AboutView(TemplateView):
    template_name = 'about.html'

#--------------------------------------------------
#Class: PostListView
#View a list of the posts
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

#--------------------------------------------------
#Class: PostDetailView
#View the details of the chosen post
class PostDetailView(DetailView):
    model = Post

#--------------------------------------------------
#Class: CreatePostView
#Create a new post as a logged in user
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

#--------------------------------------------------
#Class: PostUpdateView
#Update an existing post as a logged in user
class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

#--------------------------------------------------
#Class: PostDeleteView
#Delete an existing post as a logged in user
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

#--------------------------------------------------
#Class: DraftListView
#View a list of the unpublished drafts
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

#####################################################
#Functions
#####################################################
#--------------------------------------------------
#Function: post_publish
#Publish a post from drafts to live
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish
    return redirect('post_detail', pk=post.pk)

#--------------------------------------------------
#Function: add_comment_to_post
#Add a comment to an existing post
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.isvalid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

#--------------------------------------------------
#Function: comment_approve
#Approve a submitted comment on a post
@login_required
def comment_approve(request, pk):
    post = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

#--------------------------------------------------
#Function: comment_remove
#Remove a submitted comment on a post
@login_required
def comment_remove(request, pk):
    post = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
