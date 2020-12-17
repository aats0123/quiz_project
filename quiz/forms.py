from django import forms

from quiz.models import Quiz, Question, Answer, StudentTest
from registrator.models import TeacherProfile, StudentProfile


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ('subject', 'author')

    def save(self, user=None):
        quiz = super().save(commit=False)
        teacher_profile = TeacherProfile.objects.get(user=user)
        quiz.author = user
        quiz.subject = teacher_profile.subject
        quiz.save()
        return quiz


class BulkCreateForm(forms.Form):
    file = forms.FileField()


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('author', 'subject', 'quiz')

    # def __init__(self, user, quiz_id=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not quiz_id:
    #         self.fields['quiz'] = forms.ModelChoiceField(queryset=Quiz.objects.filter(author=user))
    # else:
    #     self.fields['quiz'] = Quiz.objects.get(id=quiz_id)
    #     #self.fields['quiz']
    def save(self, user=None, quiz_id=None):
        question = super().save(commit=False)
        teacher_profile = TeacherProfile.objects.get(user=user)
        question.author = user
        question.subject = teacher_profile.subject
        question.quiz = Quiz.objects.get(id=quiz_id)
        question.save()
        return question


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('question',)

    def save(self, question_id=None):
        answer = super().save(commit=False)
        answer.question = Question.objects.get(id=question_id)
        answer.save()


class QuizAssignForm(forms.ModelForm):
    # quiz = forms.ModelMultipleChoiceField()
    class Meta:
        model = StudentTest
        exclude = ('student', 'is_completed', 'score')

    def __init__(self, user, *args, **kwargs):
        super(QuizAssignForm, self).__init__(*args, **kwargs)
        self.fields['school_class'] = forms.ModelChoiceField(
            queryset=TeacherProfile.objects.get(user=user).school_class
        )
        self.fields['school_class'].label = 'Изберете клас'
        self.fields['quiz'] = forms.ModelChoiceField(
            queryset=Quiz.objects.filter(author=user)
        )
        self.fields['quiz'].label = 'Изберете тест'

    def save(self, user=None):
        school_class = self.cleaned_data['school_class']
        quiz = self.cleaned_data['quiz']
        student_profiles = StudentProfile.objects.filter(school_class=school_class)
        students = [sp.user for sp in student_profiles]
        for student in students:
            student_test_query = StudentTest.objects.filter(student=student).filter(quiz=quiz)
            if not student_test_query:
                student_test = StudentTest(student=student, quiz=quiz)
                student_test.save()
            elif all([st.is_completed for st in student_test_query]):
                student_test = StudentTest(student=student, quiz=quiz)
                student_test.save()

            else:
                continue


class TestQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ('title', 'description', 'subject', 'author')

    def __init__(self, quiz=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(quiz=quiz)
        for question in questions:
            question_answers = Answer.objects.filter(question=question)
            answers_texts = [answer.text for answer in question_answers]
            zipped_answers = zip([answer.id for answer in question_answers], answers_texts)
            self.fields[question.prompt] = forms.CharField(
                widget=forms.RadioSelect(
                    choices=list(zipped_answers),
                    attrs={'id':question.id, 'name': str(question.id)}
                ),
            )


