from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from registrator.models import StudentProfile, TeacherProfile


class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            # 'email': forms.EmailInput(),

        }


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ('user',)


class TeacherRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first)name', 'last_name', 'username', 'password1', 'password2', 'email')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }


class TeacherRegisterForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        exclude = ('user',)
