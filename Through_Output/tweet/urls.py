from django.urls import path 
from . import views

app_name = 'tweet'

urlpatterns = [
    path('create_tweet/', views.create_tweet, name='create_tweet'),
    path('list_tweet/', views.list_tweets, name='list_tweets'),
    path('delete_tweet/<int:id>', views.delete_tweet, name='delete_tweet'),
    # path('edit_tweet/<int:id>/', views.edit_tweet, name='edit_tweet'),
    path('tweet/<int:pk>/edit/', views.EditTweetView.as_view(), name='edit_tweet'),
    # path('tweet/<int:pk>/update/', views.UpdateTweetView.as_view(), name='update_tweet'),
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),
    # path('toggle_like/<int:tweet_id>/', views.toggle_like, name='toggle_like'),
    path('my_likes/', views.my_likes, name='my_likes'),
]