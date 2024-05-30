from django.shortcuts import render
from django.views.generic import View

from posts.models import Post


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(plikes__gt=0)[:3]
        return render(request, self.template_name, {'posts': posts})


