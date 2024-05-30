from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify

from .SizeValidation import file_size


class Post(models.Model):
    title = models.CharField(max_length=75, unique=True)
    image = models.ImageField(upload_to='posts/image/', validators=[file_size])
    body = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Post, self).save()

    def get_absolute_url(self):
        return reverse_lazy('posts:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.author} -- {self.body[:50]}'

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments',
                              null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_reply:
            return f'{self.reply.author} replied to {self.reply}'
        else:
            return f'{self.author} commented to {self.post}'

    class Meta:
        ordering = ['-created']


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='plikes')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulikes')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.liked_by} liked {self.post.slug}'
