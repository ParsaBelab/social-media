from django.db import models
from django.contrib.auth.models import User
from .SizeValidation import file_size


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='profilepic/',validators=[file_size])
    bio = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10, blank=True, null=True)


class Relation(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} follows {self.following}'

