from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
from django.contrib import messages
from .models import Tweets
from django.http import Http404, HttpResponse ,HttpResponseBadRequest
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.urls import reverse ,reverse_lazy
from django.views.generic import UpdateView
from .forms import EditTweetForm ,CreateTweetForm


# Create your views here.
from django.utils import timezone

@login_required(login_url="user/user_login/")
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


class EditTweetView(UpdateView):
    model = Tweets
    template_name = 'tweet/edit_tweet.html'
    form_class = EditTweetForm  # これを追加
    # fields = ['content']  # この行は削除します

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tweet:list_tweets')





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


@login_required(login_url="user/user_login/")
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweets, id=tweet_id)
    
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
    
    return redirect('tweet:list_tweets')


# def toggle_like(request, tweet_id):
#     return HttpResponse(status=204)

def my_likes(request):
    # ログインユーザーがいいねした投稿の一覧を取得
    liked_tweets = Tweets.objects.filter(likes=request.user).order_by('-created_at')
    selected_category = request.GET.get('category')
    if selected_category:
        tweets = tweets.filter(category=selected_category)
    search_content = request.GET.get('search_content')
    if search_content:
        tweets = tweets.filter(content__icontains=search_content)

    
    return render(request, 'tweet/my_likes.html', {'liked_tweets': liked_tweets,})