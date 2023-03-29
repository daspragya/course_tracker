from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import Course, Lesson
from profiles.views import LessonProgress,Profile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'

@method_decorator(login_required, name='dispatch')
class SingleLesson(DetailView):
    model = LessonProgress
    template_name = 'single_lesson.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_progress = kwargs['object']
        completed = lesson_progress.completed
        context['completed']=completed
        context['lesson']=lesson_progress.lesson
        return context

@method_decorator(login_required, name='dispatch')
class MarkCompleteView(View):
    model = Lesson
    def post(self, request, **kwargs):
        pk=kwargs['pk']
        user = Profile.objects.get(user = self.request.user)
        lesson = get_object_or_404(Lesson, pk=pk)
        lp = LessonProgress.objects.filter(user=user, lesson=lesson).first()
        lp.completed= True
        lp.save()
        return redirect('courses:course_detail',lesson.course.pk)
        
@method_decorator(login_required, name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course=kwargs['object']
        user = Profile.objects.get(user = self.request.user)
        x=Profile.objects.filter(user=self.request.user)
        for i in x:
            if course in i.courses.all():
                enrolled=1
            else:
                enrolled=0

        user_lessons_completed=[]
        user_lessons_notCompleted=[]
        lessons=[]
        for i in Lesson.objects.filter(course=course):
            lessons.append(i)
        for i in LessonProgress.objects.filter(user=user):
            if(Lesson.objects.filter(title=i.lesson, course=course)):
                if(i.completed==1):
                    user_lessons_completed.append(i)
                else:
                    user_lessons_notCompleted.append(i)
        context['completed_lessons']=user_lessons_completed
        context['notCompleted_lessons']=user_lessons_notCompleted
        context['enrolled']=enrolled
        context['lessons']=lessons
        print(lessons)
        return context

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    def post(self, request):
        users = User.objects.all()
        for user in users:
            try:
                profile = Profile.objects.get(user=user)
            except ObjectDoesNotExist:
                # If a profile doesn't exist, create a new one with courses=None
                profile = Profile.objects.create(user=user)
                profile.courses.set([])
        return redirect('login')