from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from posts.forms import *
from posts.models import Post, Comment, Like


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    form_class = CreateCommentForm
    form_class_reply = ReplyCommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(post=self.post_instance, is_reply=False)
        return render(request, self.template_name, {'post': self.post_instance, 'comments': comments,
                                                    'form': self.form_class, 'reply_form': self.form_class_reply})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.post_instance
            comment.author = request.user
            comment.save()
            messages.success(request, 'your comment sended', 'success')
        return redirect('posts:detail', self.post_instance.slug)


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = ReplyCommentForm

    def post(self, request, slug, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        cpost = get_object_or_404(Post, slug=slug)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = cpost
            reply.author = request.user
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply sended', 'success')
        return redirect('posts:detail', cpost.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like = Like.objects.filter(post=post, liked_by=request.user)
        if like.exists():
            like.delete()
            messages.success(request, 'disliked', 'success')
        else:
            Like.objects.create(post=post, liked_by=request.user)
            messages.success(request, 'Liked', 'success')
        return redirect('posts:detail', post.slug)


class PostCreateView(LoginRequiredMixin, View):
    template_name = 'posts/post_create.html'
    form_class = PostCreateForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created', 'success')
            return redirect('posts:detail', post.slug)
        return render(request, self.template_name, {'form': form})


