from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView, UpdateView

from registrator.forms import StudentRegisterForm, StudentProfileForm, TeacherRegisterForm, TeacherProfileForm, \
    LoginForm, SchoolClassForm, TeacherSchoolClassRegisterForm
from registrator.models import SchoolClass, TeacherProfile, StudentProfile


class RegisterStudentView(TemplateView):
    template_name = 'registrator/student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        forms = (StudentRegisterForm(), StudentProfileForm(), SchoolClassForm())
        # context['student_form'] = StudentRegisterForm()
        # context['student_profile_form'] = StudentProfileForm()
        # context['school_class_form'] = SchoolClassForm()
        context['forms'] = forms
        return context

    @transaction.atomic
    def post(self, request):
        student_form = StudentRegisterForm(request.POST)
        student_profile_form = StudentProfileForm(request.POST)
        school_class_form = SchoolClassForm(request.POST)

        if student_form.is_valid() and student_profile_form.is_valid() and school_class_form.is_valid():
            student = student_form.save()
            student.groups.add(Group.objects.get(name__exact='students'))
            profile = student_profile_form.save(commit=False)
            profile.user = student
            school_class = school_class_form.save(commit=False)
            school_class_query = SchoolClass.objects.filter(
                school__name=school_class.school.name
            ).filter(
                class_level=school_class.class_level
            ).filter(
                class_letter=school_class.class_letter
            )
            if school_class_query:
                school_class = school_class_query[0]
            else:
                school_class.save()

            profile.school_class = school_class
            profile.save()
            login(request, student)
            return redirect('student-detail', pk=student.id)
        forms = (StudentRegisterForm(self.request.POST), StudentProfileForm(self.request.POST),
                 SchoolClassForm(self.request.POST))
        context = {
            'forms': forms,
        }

        return render(request, 'registrator/student.html', context)


# # class StudentEditView(UpdateView, LoginRequiredMixin):
# #     model = User
# #     form_class = StudentRegisterForm
# #     template_name = 'registrator/student.html'
# #
# #     def get_context_data(self, **kwargs):
# #         context = super().get_context_data(**kwargs)
# #         forms = (StudentRegisterForm(), StudentProfileForm())
# #         # context['student_form'] = StudentRegisterForm()
# #         # context['student_profile_form'] = StudentProfileForm()
# #         # context['school_class_form'] = SchoolClassForm()
# #         context['forms'] = forms
# #         return context
#     # def get_queryset(self):
#     #     pass
#
# def student_edit_view(request, pk):
#     student = User.objects.get(id=pk)
#     student_profile = StudentProfile.objects.get(user=student)
#     school_class = student_profile.school_class
#
#
#     if request.method == 'GET':
#         student_form = StudentRegisterForm(instance=student)
#         school_class_form = SchoolClassForm(initial={
#             'school': student_profile.school_class.school,
#             'class_level': student_profile.school_class.class_level,
#             'class_letter': student_profile.school_class.class_letter
#         }
#         )
#         context = {'forms': (student_form, school_class_form)}
#         return render(request, 'registrator/student.html', context)
#     initials = {
#         'first_name': request.POST['first_name'],
#         'last_name': request.POST['last_name'],
#         'username': request.POST['username'],
#         'email': request.POST['email'],
#         'school_id': request.POST['school'],
#     }

    # student_form = StudentRegisterForm(request.POST, instance=student)
    # student_profile_form = StudentRegisterForm(request.POST, instance=student_profile)
    # school_class_form = SchoolClassForm(request.POST, instance=school_class)
    # x=6
    # if student_form.ch
    # if student_form.is_valid() and student_profile_form.is_valid() and school_class_form.is_valid():
    #     student_form.save(commit=False)
    #     student_profile_form.save(commit=False)
    #     school_class_form.save(commit=False)
    #     x=5
    #     return redirect('student-detail', pk)

class RegisterTeacherView(TemplateView):
    # template_name = 'registrator/teacher.html'
    template_name = 'registrator/student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['teacher_form'] = TeacherRegisterForm()
        # context['teacher_profile_form'] = TeacherProfileForm()
        context['forms'] = (TeacherRegisterForm(), TeacherProfileForm())
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
            'forms': (TeacherRegisterForm(request.POST), TeacherProfileForm(request.POST)),
        }

        return render(request, 'registrator/teacher.html', context)


class SchoolClassRegisterView(TemplateView):
    template_name = 'registrator/class-register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['school_class_form'] = TeacherSchoolClassRegisterForm()
        return context

    @transaction.atomic
    def post(self, request, pk):
        school_class_form = TeacherSchoolClassRegisterForm(request.POST)

        if school_class_form.is_valid():
            teacher_profile = TeacherProfile.objects.get(user=request.user)
            school_class = school_class_form.save(commit=False)
            class_level = school_class.class_level
            class_letter = school_class.class_letter
            school_class_query = SchoolClass.objects.filter(
                school=teacher_profile.school
            ).filter(
                class_level=school_class.class_level
            ).filter(
                class_letter=school_class.class_letter
            )
            if school_class_query:
                school_class = school_class_query[0]
            else:
                school_class.school = teacher_profile.school
                school_class.save()
            teacher_profile.school_class.add(school_class)
            teacher_profile.save()

            return redirect('teacher-detail', pk=request.user.id)

        context = {
            'school_class_form': TeacherSchoolClassRegisterForm(),
        }

        return render(request, 'registrator/class-register.html', context)


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
            else:
                messages.warning(request, "The username  or passsword is icorrect ")
                context = {
                    'form': LoginForm(request.POST),
                    'error': 'User name or password incorrect!'
                }
                return render(request, 'registrator/login.html', context)

        context = {
            'form': LoginForm(request.POST),
        }

        return render(request, 'registrator/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('quiz-home')
