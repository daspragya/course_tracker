from django.urls import path
from .views import CourseListView, CourseDetailView,SingleLesson,MarkCompleteView

app_name = 'courses'

# Make all the links
urlpatterns=[
    path('', CourseListView.as_view(),name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('lesson/<int:pk>',SingleLesson.as_view(),name='lesson_detail'),
    path('<int:pk>',MarkCompleteView.as_view(),name='mark_complete'),
]