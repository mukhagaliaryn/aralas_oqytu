from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django.contrib.auth.forms import AuthenticationForm


# User login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Қолданушының аты',
        widget=forms.TextInput(attrs={
            'placeholder': 'Қолданушының аты',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Құпия сөз',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Құпия сөз'
        })
    )


# User register form
class UserForm(UserCreationForm):
    email = forms.EmailField(
        label='Электронды пошта',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@gmail.com'
        })
    )
    username = forms.CharField(
        label='Қолданушының аты',
        widget=forms.TextInput(attrs={
            'placeholder': 'user.name'
        })
    )
    password1 = forms.CharField(
        label='Құпия сөз',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Қауіпсіз символдар жазыңыз!'
        })
    )
    password2 = forms.CharField(
        label='Құпия сөзді қайталау',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Құпия сөзді қайталау'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )


# User update
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label='Электронды пошта',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@gmail.com'
        })
    )

    class Meta:
        model = User
        fields = ('avatar', 'email', 'first_name', 'last_name', 'profession', )
