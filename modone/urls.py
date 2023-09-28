from django.urls import path
from . import views


urlpatterns = [

    path('select_semester/', views.select_semester, name='select_semester'),
    path('select_semester_quantity/<int:semester_id>/', views.select_semester_quantity, name='select_semester_quantity'),
    path('start_semester_quiz/<int:semester_id>/', views.start_semester_quiz, name='start_semester_quiz'),
    path('semester_quiz_complete/<int:q_id>/', views.semester_quiz_complete, name='semester_quiz_complete'),

]