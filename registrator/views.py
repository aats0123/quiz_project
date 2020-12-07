from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from registrator.forms import StudentRegisterForm, StudentProfileForm, TeacherRegisterForm, TeacherProfileForm, \
    LoginForm


class RegisterStudentView(TemplateView):
    template_name = 'registrator/student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_form'] = StudentRegisterForm()
        context['student_profile_form'] = StudentProfileForm()
        return context

    @transaction.atomic
    def post(self, request):
        student_form = StudentRegisterForm(request.POST)
        student_profile_form = StudentProfileForm(request.POST)

        if student_form.is_valid() and student_profile_form.is_valid():
            student = student_form.save()
            student.groups.add(Group.objects.get(name__exact='students'))
            profile = student_profile_form.save(commit=False)
            profile.user = student
            profile.save()
            login(request, student)
            return redirect('student-detail', pk=student.id)

        context = {
            'student_form': StudentRegisterForm(),
            'student_profile_form': StudentProfileForm(),
        }

        return render(request, 'registrator/student.html', context)


class RegisterTeacherView(TemplateView):
    template_name = 'registrator/teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_form'] = TeacherRegisterForm()
        context['teacher_profile_form'] = TeacherProfileForm()
        return context

    @transaction.atomic
    def post(self, request):
        teacher_form = TeacherRegisterForm(request.POST)
        teacher_profile_form = TeacherProfileForm(request.POST)

        if teacher_form.is_valid() and teacher_profile_form.is_valid():
            teacher = teacher_form.save()
            teacher.groups.add(Group.objects.get(name__exact='teachers'))
            profile = teacher_profile_form.save(commit=False)
            profile.user = teacher
            profile.save()
            login(request, teacher)
            return redirect('teacher-detail', pk=teacher.id)

        context = {
            'teacher_form': TeacherRegisterForm(),
            'teacher_profile_form': StudentProfileForm(),
        }

        return render(request, 'registrator/teacher.html', context)


# class UserLoginView(LoginView):
#     template_name = 'registrator/login.html'
#     #redirect_authenticated_user = True
#
#     def get_success_url(self):
#         user = self.request.user
#         user_group_names = [g.name for g in user.groups.all()]
#         if 'students' in user_group_names:
#             return redirect('student-detail', pk=user.id)
#         else:
#             return redirect('quiz-home')
def login_user(request):
    RETURN_URLS = {
        'students': 'student-detail',
        'teachers': 'teacher-detail',
    }
    if request.method == 'GET':
        return render(request, 'registrator/login.html', context={'form': LoginForm()})
    else:
        login_form = LoginForm(request.POST)

        return_url = request.POST.get('return_url')

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                user_group_name = [group.name for group in user.groups.all()][0]
                if not return_url:
                    return_url = RETURN_URLS[user_group_name]
                login(request, user)
                return redirect(return_url, pk=user.id)

        context = {
            'login_form': login_form,
        }

        return render(request, 'registrator/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('quiz-home')
