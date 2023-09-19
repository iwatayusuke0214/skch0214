from django import forms
from .models import Tweets
from django.utils import timezone

class CreateTweetForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ("FREE","FREE"),
        ("政治","政治"),
        ("IT","IT"),
        ("経済","経済"),
        ("哲学","哲学"),
        ("人間関係","人間関係"),
        ("恋愛","恋愛"),
    )
    content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'cols':'50','rows':'4',}))
    category = forms.ChoiceField(label='カテゴリ', choices=CATEGORY_CHOICES)  # カテゴリの選択肢をプルダウンとして表示

    class Meta:
        model = Tweets
        fields = ('content',)


class DeleteTweetForm(forms.ModelForm):

    class Meta:
        model = Tweets
        fields = []


class EditTweetForm(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': '50', 'rows': '4'})
        }