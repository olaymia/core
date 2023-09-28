from django.urls import path
from . import views



urlpatterns = [

    path('select_subject/', views.select_subject, name='select_subject'),
    path('select_quantity/<int:subject_id>/', views.select_quantity, name='select_quantity'),
    path('start_quiz/<int:subject_id>/', views.start_quiz, name='start_quiz'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
    path('quiz_complete/<int:q_id>', views.complete_quiz, name='quiz_complete'),
    
]