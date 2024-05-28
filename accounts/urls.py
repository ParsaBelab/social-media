from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('editprofile/', UserEditProfileView.as_view(), name='eprofile'),
    path('profile/<int:id>', UserProfileView.as_view(), name='profile'),
    path('follow/<int:id>', UserFollowView.as_view(), name='follow'),
    path('unfollow/<int:id>', UserUnfollowView.as_view(), name='unfollow'),
    # password reset
    path('reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('confrim/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('confrim/complete/', UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
