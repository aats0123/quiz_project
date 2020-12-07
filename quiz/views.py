from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, DetailView, DeleteView
from django.views.generic.base import View

from quiz.forms import QuizCreateForm, QuestionCreateForm, AnswerCreateForm
from quiz.models import Quiz, Question, Answer
from registrator.models import TeacherProfile, StudentProfile


def render_home(request):
    return render(request, 'quiz/home.html')


class StudentDetailView(DetailView):
    model = User
    template_name = 'quiz/student-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_profile = StudentProfile.objects.get(user=self.request.user)
        context['profile'] = student_profile
        return context


class TeacherDetailView(DetailView):
    model = User
    template_name = 'quiz/teacher-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_profile = TeacherProfile.objects.get(user=self.request.user)
        quizzes = Quiz.objects.filter(author=self.request.user)
        context['profile'] = teacher_profile
        context['quizzes'] = quizzes
        return context


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz-detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = context['quiz']
        questions = Question.objects.filter(quiz=quiz)
        context['questions'] = questions
        return context


class QuizCreateView(FormView):
    form_class = QuizCreateForm
    template_name = 'quiz/quiz-create.html'
    success_url = reverse_lazy('quiz-home')
    teacher_id = None

    def form_valid(self, form):
        self.teacher_id = self.request.user.id
        form.save(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacher-detail', kwargs={'pk': self.teacher_id})


class QuizDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Quiz
    template_name = 'quiz/quiz-delete.html'
    quiz_id = None

    def test_func(self):
        return self.get_object().owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


def question_create_view(request, pk):
    if request.method == 'GET':
        form = QuestionCreateForm()
        context = {'form': form, 'pk': pk}
        return render(request, 'quiz/question-create.html', context)

    form = QuestionCreateForm(request.POST)
    if form.is_valid():
        form.save(request.user, pk)
        return redirect('quiz-detail', pk)
    return render(request, 'quiz/question-create.html', {'form': form, 'pk': pk})


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'quiz/question-detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context['question']
        context['answers'] = Answer.objects.filter(question=question)
        return context


def answer_create_view(request, quiz_id, question_id):
    if request.method == 'GET':
        return render(request, 'quiz/answer-create.html', {'form': AnswerCreateForm()})

    form = AnswerCreateForm(request.POST)
    if form.is_valid():
        form.save(question_id=question_id)
        return redirect('question-detail', quiz_id, question_id)

    return render('quiz/answer-create.html', quiz_id, question_id)
