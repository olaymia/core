from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Topic(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(BaseModel):
    MCQ = 'Single Choice Question'
    MULTIPLE_SELECT = 'Multiple Select Question'
    QUESTION_TYPES = [
        (MCQ, 'Single Choice Question'),
        (MULTIPLE_SELECT, 'Multiple Select Question'),
    ]

    text = models.TextField()
    topic = models.ForeignKey(Topic, related_name='topic_questions', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    marks = models.IntegerField(default=1)
    time_limit = models.IntegerField(default=90)
    description = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def get_details(self):
        return {
            "question": self.question,
            "choice_text":self.choice_text,
            "id":self.id,
        }
        
    def __str__(self):
        return self.choice_text

class TopOneUserQuiz(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="top_one_quiz_user")
    topic = models.ForeignKey("topone.Topic", on_delete=models.CASCADE,blank=True, null=True, related_name="top_one_user_quiz_topic")
    question_quantity = models.IntegerField(default=0)
    question = models.ManyToManyField("topone.Question", blank=True, related_name="top_one_userQuiz_quesstion")
    quiz_start_time = models.DateTimeField(null=True, blank=True)
    quiz_end_time = models.DateTimeField(null=True, blank=True)
    is_completed=models.BooleanField(default=False)

class TopOneUserResponse(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_quiz = models.ForeignKey("topone.TopOneUserQuiz", on_delete=models.CASCADE, related_name="top_one_user_quiz_response", blank=True, null=True)
    question = models.ForeignKey("topone.Question", on_delete=models.CASCADE, related_name="top_one_user_reponse_quesion")
    single_selected_choice = models.ForeignKey("topone.Choice", on_delete=models.CASCADE,blank=True, null=True, related_name="top_one_user_response_selected_single_choice")
    multi_selected_choices = models.ManyToManyField("topone.Choice", blank=True, related_name="top_one_user_response_selected_multi_choices")
    question_type = models.CharField(choices=Question.QUESTION_TYPES, max_length=50, blank=True, null=True)
    marks = models.FloatField(default=0.0)
    is_correct = models.BooleanField(default=False)