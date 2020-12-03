from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from registrator.forms import StudentRegisterForm, StudentProfileForm, TeacherRegisterForm, TeacherProfileForm


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
            return redirect('quiz-home')

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
            return redirect('quiz-home')

        context = {
            'teacher_form': TeacherRegisterForm(),
            'teacher_profile_form': StudentProfileForm(),
        }

        return render(request, 'registrator/student.html', context)

