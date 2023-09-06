from django.shortcuts import render, redirect ,get_object_or_404
from . import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import UserActivateTokens, Users
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .forms import UserProfileForm
from django.http import HttpResponse
from tweet.models import Tweets


# Create your views here.
def home(request):
    return render(
        request, 'user/home.html'
    )

def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('user:home')
        except ValidationError as e:
            regist_form.add_error('password', e)
    return render(
        request, 'user/regist.html', context={
            'regist_form': regist_form,
        }
    )



def activate_user(request, token):
    try:
        user_activate_token = UserActivateTokens.objects.get(token=token)
        if user_activate_token.expired_at >= datetime.now():
            user = user_activate_token.user
            user.is_active = True
            user.save()
            messages.success(request, 'ユーザーがアクティブ化されました。ログインしてください。')
            return redirect('user:user_login')
        else:
            messages.warning(request, 'トークンの有効期限が切れています。再度登録を行ってください。')
            return redirect('user:regist')
    except ObjectDoesNotExist:
        messages.warning(request, 'トークンが無効です。再度登録を行ってください。')
        return redirect('user:regist')

    

def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        print(user)  # デバッグメッセージの追加
        # ...
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログイン完了しました。')
                return redirect('user:home')
            else:
                messages.warning(request, 'ユーザがアクティブでありません')
        else:
            messages.warning(request, 'ユーザかパスワードが間違っています')
    return render(
        request, 'user/user_login.html', context={
            'login_form': login_form,
        }
    )

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('user:home')

def mypage(request, user_id):
    user = get_object_or_404(Users, id=user_id)
    tweets = Tweets.objects.filter(user=user).order_by('-created_at')
    return render(request, "user/mypage.html", {"user": user, "tweets": tweets})

@login_required(login_url="user_login") 
def mypage_edit(request):
    user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if user_edit_form.is_valid():
        messages.success(request, '更新完了しました。')
        user_edit_form.save()
    return render(request, 'user/mypage_edit.html', context={
        'user_edit_form': user_edit_form,
    })