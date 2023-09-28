from django.urls import path
from . import views


urlpatterns = [
    path('select_topic/', views.select_topic, name='select_topic'),
    path('select_topic_quantity/<int:topic_id>/', views.select_topic_quantity, name='select_topic_quantity'),
    path('start_topic_quiz/<int:topic_id>/', views.start_topic_quiz, name='start_topic_quiz'),
    path('top_one_quiz_complete/<int:q_id>', views.top_one_complete_quiz, name='top_one_quiz_complete'),

]