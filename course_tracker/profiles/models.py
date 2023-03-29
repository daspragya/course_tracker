from django.contrib.auth.models import User
from django.db import models
from courses.models import Course, Lesson

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='profiles', blank=True)

    def __str__(self):
        return self.user.username

class LessonProgress(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_profiles')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.lesson}"
