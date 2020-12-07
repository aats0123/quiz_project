from django.contrib.auth.models import User
from django.db import models
from quiz.models import SUBJECT, Quiz


class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=11, choices=SUBJECT)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class StudentProfile(models.Model):
    GRADE = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8))
    SCHOOL_CLASS = ((1, 'А'), (2, 'Б'), (3, 'В'), (4, 'Г'), (5, 'Д'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADE)
    school_class = models.IntegerField(choices=SCHOOL_CLASS)

    def __str__(self):
        return f'{self.user.first_name[0].upper()}. {self.user.last_name}, {self.school}, {self.grade} - {self.school_class}'


class StudentTest(models.Model):
    student = models.ManyToManyField(User)
    test = models.ManyToManyField(Quiz, related_name='tests')
    is_completed = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
