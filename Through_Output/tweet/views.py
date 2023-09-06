from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Tweets
from django.http import Http404, HttpResponse
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.
from django.utils import timezone

def create_tweet(request):
    create_tweet_form = forms.CreateTweetForm(request.POST or None)
    if create_tweet_form.is_valid():
        tweet = create_tweet_form.save(commit=False)
        tweet.user = request.user
        tweet.created_at = timezone.now()  # 現在の日時を設定
        tweet.category = create_tweet_form.cleaned_data['category']
        tweet.save()
        messages.success(request, '投稿完了しました')
        return redirect('tweet:list_tweets')
    return render(
        request, 'tweet/create_tweet.html', context={
            'create_tweet_form': create_tweet_form,
        }
    )



def list_tweets(request):
    tweets = Tweets.objects.annotate(likes_count=Count('likes')).order_by('-created_at')
    for tweet in tweets:
        tweet.likes_count = tweet.likes.count()
    selected_category = request.GET.get('category')
    if selected_category:
        tweets = tweets.filter(category=selected_category)
    search_content = request.GET.get('search_content')
    if search_content:
        tweets = tweets.filter(content__icontains=search_content)
    return render(
        request, 'tweet/list_tweets.html', context={
            'tweets': tweets,
            'form': forms.CreateTweetForm()
        }
    )


def edit_tweet(request, id):
    tweet = get_object_or_404(Tweets, id=id)

    # ログインしていない場合はログインページにリダイレクト
    if not request.user.is_authenticated:
        return redirect('user:user_login')

    # ログインユーザーのチェック
    if tweet.user.id != request.user.id:
        raise Http404

    if request.method == 'GET':
        edit_tweet_form = forms.EditTweetForm(request.POST, instance=tweet)
        if edit_tweet_form.is_valid():
            edit_tweet_form.save()
            messages.success(request, '投稿内容を更新しました')
            return redirect('tweet:list_tweets')
    else:
        edit_tweet_form = forms.EditTweetForm(instance=tweet)

    return render(request, 'tweet/edit_tweet.html', context={'edit_tweet_form': edit_tweet_form, 'id': id})



def delete_tweet(request, id):
    tweet = get_object_or_404(Tweets, id=id)
    if tweet.user.id != request.user.id:
        raise Http404
    delete_tweet_form = forms.DeleteTweetForm(request.POST or None, instance=tweet)
    if delete_tweet_form.is_valid(): # csrf check
        tweet.delete()
        messages.success(request, '投稿を削除しました')
        return redirect('tweet:list_tweets')
    return render(
        request, 'tweet/delete_tweet.html', context={
            'tweet': tweet,
            'delete_tweet_form': delete_tweet_form,
        }
    )


@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweets, id=tweet_id)
    
    if request.user in tweet.likes.all():
        # すでにいいねしている場合はいいねを解除
        tweet.likes.remove(request.user)
    else:
        # いいねを追加
        tweet.likes.add(request.user)
    
    return redirect('tweet:list_tweets')


# def toggle_like(request, tweet_id):
#     return HttpResponse(status=204)

def my_likes(request):
    # ログインユーザーがいいねした投稿の一覧を取得
    liked_tweets = Tweets.objects.filter(likes=request.user).order_by('-created_at')
    
    return render(request, 'tweet/my_likes.html', {'liked_tweets': liked_tweets})
