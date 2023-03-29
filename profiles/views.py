from django.shortcuts import redirect
from django.views.generic import TemplateView
from courses.models import Course, Lesson
from .models import Profile, LessonProgress
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages


class ProfileView(TemplateView):
    template_name = 'profiles/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

class MyCourses(TemplateView):
    template_name= 'user_course_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = Profile.objects.get(user=self.request.user)
        user_courses = user.courses.all()
        user_courses_completed=[]
        user_courses_progress=[]
        for i in user_courses:
            for j in LessonProgress.objects.filter(user=user):
                if(j.lesson.course==i):
                    if(j.completed==0):
                        user_courses_progress.append(i)
                        break
            else:
                user_courses_completed.append(i)
        context['user_courses_completed']=user_courses_completed
        context['user_courses_progress']=user_courses_progress
        return context

@method_decorator(login_required, name='dispatch')
class Enroll(View):
    model = Course
    def post(self, request, **kwargs):
        print("Here!")
        course = Course.objects.get(pk=kwargs['pk'])
        user = Profile.objects.get(user=self.request.user)
        print(user.courses.all())
        user.courses.add(course)
        user.save()
        lessons = Lesson.objects.filter(course=course)
        for i in lessons:
            lp = LessonProgress()
            lp.lesson=i
            lp.user=user
            lp.completed=0
            lp.save()
        print(lessons)
        messages.success(request, f"You have enrolled in {course.title}.")
        return redirect('profiles:my_course_list')