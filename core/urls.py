from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedules_list, name='schedules_list'),
    path('schedule', views.schedule, name='schedule'),
    path('check_unavailable_classrooms', views.check_unavailable_classrooms, name='check_unavailable_classrooms'),
    path('check_unavailable_classrooms_form', views.check_unavailable_classrooms_form, name='check_unavailable_classrooms_form'),
    path('update_schedules', views.update_schedules, name='update_schedules'),
]
