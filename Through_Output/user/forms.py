from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta():
        model = Users
        fields = ('username', 'age', 'email', 'password')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.password = make_password(self.cleaned_data['password'])
        user.save()
        return user
    
class LoginForm(forms.Form):
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'age', 'picture']


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    picture = forms.FileField(label='写真', required=False)
    profile = forms.CharField(label="自己紹介", max_length=200, widget=forms.Textarea(attrs={'cols':'50','rows':'4',}))

    class Meta:
        model = Users
        fields = ('username', 'age', 'email', 'picture', 'profile')