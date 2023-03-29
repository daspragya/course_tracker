from django.urls import path
from .views import ProfileView, MyCourses, Enroll

app_name = 'profiles'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my_courses/',MyCourses.as_view(), name="my_course_list"),
    path('<int:pk>',Enroll.as_view(),name="enroll_course"),
]
