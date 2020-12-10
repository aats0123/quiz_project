from django.contrib.auth.models import User
from django.db import models
from quiz.models import SUBJECT, Quiz


class School(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    LEVEL = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8))
    SCHOOL_CLASS = (('А', 'А'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Д', 'Д'), ('Е', 'Е'))
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING)
    class_level = models.IntegerField(choices=LEVEL)
    class_letter = models.CharField(max_length=1, choices=SCHOOL_CLASS)

    def __str__(self):
        return f'{self.school.name} {self.class_level}-{self.class_letter}'


class TeacherProfile(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=11, choices=SUBJECT)
    school_class = models.ManyToManyField(SchoolClass, default=None)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # school = models.ForeignKey(School, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user.first_name[0].upper()}. {self.user.last_name}, {self.school_class.school}, {self.school_class}'
