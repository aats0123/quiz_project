from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from registrator.models import StudentProfile, TeacherProfile, SchoolClass


class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            # 'email': forms.EmailInput(),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Име'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['username'].label = 'Потребителско име'
        self.fields['username'].help_text = 'Задължително поле, позволени са букви, цифри и @ /./ + / - / _ . Макс. дължина 150 символа'
        # Required. 150 characters or fewer.Letters, digits and @ /./ + / - / _ only.
        self.fields['password1'].label = 'Парола'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Потвърдете паролата'
        self.fields['password2'].help_text = ''
        self.fields['email'].label = 'Email'


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ('user', 'school_class')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# class StudentUpdateForm(forms.ModelForm):
#     class Meta:
#         model = StudentProfile
#         fields = ('first_name', 'last_name', 'username', 'email')
#
#     def __init__(self, user=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         student_profile = StudentProfile.objects.get(user=self.user)
#         self.fields['']


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].label = 'Училище'
        self.fields['class_level'].label = 'Клас'
        self.fields['class_letter'].label = 'Паралелка'


class TeacherRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(TeacherRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Име'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['username'].label = 'Потребителско име'
        self.fields['username'].help_text = ''
        self.fields['password1'].label = 'Парола'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Потвърдете паролата'
        self.fields['password2'].help_text = ''
        self.fields['email'].label = 'Email'


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        exclude = ('user', 'school_class')

    def __init__(self, *args, **kwargs):
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        self.fields['school'].label = 'Училище'
        self.fields['subject'].label = 'Предмет'


class TeacherSchoolClassRegisterForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        exclude = ('school',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_level'].label = 'Клас'
        self.fields['class_letter'].label = 'Паралелка'


class TeacherLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(label='Потребителско име')
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Парола'
    )
