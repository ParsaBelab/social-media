from django.urls import path
from .views import *

app_name = 'posts'
urlpatterns = [
    path('all/', PostListView.as_view(), name='all'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('reply/<slug:slug>/<int:comment_id>/', PostAddReplyView.as_view(), name='reply'),
    path('like/<slug:slug>', PostLikeView.as_view(), name='like'),
    path('update/<slug:slug>', PostUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>', PostDeleteView.as_view(), name='delete'),
]
