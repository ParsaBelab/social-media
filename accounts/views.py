from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import Relation


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You are already registered', 'danger')
            return redirect('Home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], password=cd['password1'], email=cd['email'])
            login(request, user)
            messages.success(request, 'you registered successfully!', 'success')
            return redirect('Home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    template_name = 'login.html'
    form_class = UserLoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('Home:home')
        messages.error(request, 'username or password incorrect', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out', 'success')
        return redirect('Home:home')


class UserEditProfileView(LoginRequiredMixin, View):
    template_name = 'editprofile.html'
    form_class = UserProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email,
                                                                       'first_name': request.user.first_name,
                                                                       'last_name': request.user.last_name})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            id = request.user.id
            request.user.first_name = cd['first_name']
            request.user.last_name = cd['last_name']
            request.user.save()
            messages.success(request, 'Edited!', 'success')
            return redirect('accounts:profile', id=id)
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request, id):
        is_following = False
        user = get_object_or_404(User, pk=id)
        relation = Relation.objects.filter(follower=request.user, following=user).exists()
        if relation:
            is_following = True
        return render(request, self.template_name, {'user': user, 'is_following': is_following})


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        relation = Relation.objects.filter(follower=request.user, following=user).exists()
        if relation:
            messages.error(request, f'You already followed {user.username}', 'error')
        else:
            Relation.objects.create(follower=request.user, following=user)
            messages.success(request, f'You followed {user.username}', 'success')
        return redirect('accounts:profile', id=id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        relation = Relation.objects.filter(follower=request.user, following=user)
        if relation.exists():
            relation.delete()
            messages.success(request, f'You unfollowed {user.username}', 'success')
        else:
            messages.error(request, f'you are not following {user.username}', 'error')
        return redirect('accounts:profile', id=id)


class UserPasswordResetView(PasswordResetView):
    template_name = 'passReset/password_reset_form.html'
    success_url = reverse_lazy('accounts:password-reset-done')
    email_template_name = 'passReset/password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'passReset/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'passReset/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password-reset-complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'passReset/password_reset_complete.html'
