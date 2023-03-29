from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages

'''
    Our courses have two models 
        one to store each course and 
        another to store lessons related to each course.
'''
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    #When a print(Course) is called it returns the course title 
    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #When a print(Course) is called it returns the lesson title 
    def __str__(self):
        return self.title