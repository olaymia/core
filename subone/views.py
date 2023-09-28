from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from subone import models as subone_models
from django.utils import timezone
from datetime import datetime, timedelta
from core import utils as core_utils
import string
from django.http import JsonResponse

@login_required
def select_subject(request):
    subjects = subone_models.Subject.objects.all()
    return render(request, 'subone/select_subject.html', {'subjects': subjects})



@login_required
def select_quantity(request, subject_id):
    subject = subone_models.Subject.objects.get(id=subject_id)

    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions'))
        if num_questions < 1:
            # Handle invalid input, e.g., show an error message
            return render(request, 'subone/select_quantity.html', {'subject': subject})

        # Store num_questions in the session
        request.session['num_questions'] = num_questions

        # Redirect to the start_quiz view
        return redirect('start_quiz', subject_id=subject_id)

    return render(request, 'subone/select_quantity.html', {'subject': subject})


@login_required
def start_quiz(request, subject_id):
    if request.method == 'GET':
        subject = subone_models.Subject.objects.get(id=subject_id)
        number_of_questions = int(request.GET.get('num_questions'))
        
        print("number_of_questions===========>", number_of_questions)
        quiz_id = request.GET.get('q_id', None)
        
        # Check if the user has already started the quiz
        # request.session['question_index'] = 1
        question_index = int(request.GET.get('question_index', 0))
        if 'question_index' not in request.session:
            request.session['question_index'] = question_index  # Initialize question index

            request.session['subject_id'] = subject_id  # Store subject ID in session
            expired_time = core_utils.get_datetime(timezone.now()+timedelta(seconds=(number_of_questions*90)))
            formatted_expiry_time = expired_time.strftime('%Y-%m-%d %H:%M:%S')
            request.session['expiry_time']=formatted_expiry_time
        else:
            request.session['question_index'] =question_index    

        # Retrieve the questions related to the subject
        question_instances = subone_models.Question.objects.filter(subject=subject).order_by('?')[:number_of_questions] # Filter
        
        if not quiz_id:
            sub_one_user_quiz_instance = subone_models.SubOneUserQuiz.objects.filter(
                user=request.user,
                subject=subject,
                question_quantity=number_of_questions,
                is_completed=False
            ).last()
        else:
            sub_one_user_quiz_instance = subone_models.SubOneUserQuiz.objects.filter(
                user=request.user,
                id=quiz_id,
                is_completed=False
            ).last()
            
        total_attempts = subone_models.UserResponse.objects.filter(
                user=request.user,
                user_quiz=sub_one_user_quiz_instance,
            ).count()

            
        sub_one_user_quiz_instance_list = []
        if not sub_one_user_quiz_instance:
            sub_one_user_quiz_instance = subone_models.SubOneUserQuiz.objects.create(
                user=request.user,
                question_quantity=number_of_questions,
                quiz_start_time=core_utils.get_datetime(timezone.now()),
                quiz_end_time=core_utils.get_datetime(timezone.now()+timedelta(seconds=(number_of_questions*90))),
                subject=subject
            )
            
            if sub_one_user_quiz_instance:
                for question in question_instances:
                    sub_one_user_quiz_instance.question.add(question)
        
        sub_one_user_quiz_instance_list = sub_one_user_quiz_instance.question.all()
        
        count = 1
        question_id_with_index_list = []
        
        for obj in sub_one_user_quiz_instance_list:
            
            user_submitted_quesion = subone_models.UserResponse.objects.filter(
                user=request.user,
                user_quiz=sub_one_user_quiz_instance,
                question=obj
            ).last()
            
            is_question_submmited=False
            if user_submitted_quesion:
                is_question_submmited=True
                
                
            question_id_with_index_list.append(
                {
                    "question_id":obj.id,
                    "question_index":count,
                    "is_question_submmited":is_question_submmited
                }
            )
            count +=1 
        
        
        
        # Check if there are questions left to display
        
        if request.session['question_index'] <= (len(sub_one_user_quiz_instance_list) - 1):
            current_question = sub_one_user_quiz_instance_list[request.session['question_index']]
            question_option_instances = subone_models.Choice.objects.filter(question=current_question)
            current_question_is_submited = False
            current_question_submitted = subone_models.UserResponse.objects.filter(
                user=request.user,
                user_quiz=sub_one_user_quiz_instance,
                question=current_question
            ).last()
            if current_question_submitted:
                current_question_is_submited=True
    
            a_to_z_list = list(string.ascii_uppercase)
            question_option_instances_list =[]
            question_count = 0
            
            for question_option_instances in question_option_instances:
                question_details = question_option_instances.get_details()
                if current_question_submitted:
                    if current_question_submitted.question_type == subone_models.Question.MCQ:
                        user_submitted_answers = current_question_submitted.single_selected_choice.id
                        question_details["user_submitted_answers"] = user_submitted_answers
                    else:
                        user_submitted_answers = [obj.id for obj in current_question_submitted.multi_selected_choices.all()]
                        question_details["user_submitted_answers"] = user_submitted_answers
                        
                question_option_instances_list.append(
                    {
                        "option":question_details,
                        "index_by_alpha":a_to_z_list[question_count],
                        "index_by_number":question_count
                    }
                )
                question_count +=1
            
            
            
            return render(request, 'subone/start_quiz.html', {
                'subject': subject,
                'current_question': current_question,
                "quesion_options":question_option_instances_list,
                "question_ids":question_id_with_index_list,
                "user_quiz_question_instace_id":sub_one_user_quiz_instance.id,
                "current_index":request.session['question_index'],
                "current_index_for_dipslay":request.session['question_index']+1,
                "current_question_id":current_question.id,
                "number_of_questions":sub_one_user_quiz_instance.question_quantity,
                "current_question_is_submitted":current_question_is_submited,
                "total_attempts":total_attempts
                
            })
        else:
            return redirect('quiz_complete', q_id=sub_one_user_quiz_instance.id)  # Replace 'quiz_complete' with the URL for the completion page

    if request.method == 'POST':
        subject = subone_models.Subject.objects.get(id=subject_id)
        
        number_of_questions = int(request.POST.get("num_questions"))
        current_quiz_id=request.POST.get("current_quiz_id")
        current_question_id=request.POST.get("current_question_id")
        current_question_ans=request.POST.get("current_question_ans")
        question_type=request.POST.get("question_type")
        
     
        question_instances = subone_models.Question.objects.filter(
            subject=subject,
            id=current_question_id,
            question_type=question_type
        ).last()
        
        sub_one_user_quiz_instance = subone_models.SubOneUserQuiz.objects.filter(
                id=current_quiz_id,
                user=request.user,
                subject=subject,
                question_quantity=number_of_questions,
                is_completed=False
        ).last()
        question_mark = 0
        
        user_question_response_instance = subone_models.UserResponse.objects.filter(
                    user=request.user,
                    user_quiz=sub_one_user_quiz_instance,
                    question=question_instances,
                    question_type=question_instances.question_type,
                ).last()
        
        if user_question_response_instance:
            return JsonResponse({'error': "YOu have already summmited answer for this question", "status_code": 500})  
        
        if question_instances and sub_one_user_quiz_instance:
            if question_type == subone_models.Question.MCQ:
                
                quesion_option = subone_models.Choice.objects.filter(
                    question=question_instances,
                    id=current_question_ans
                ).last()
                
                if quesion_option.is_correct:
                    question_mark = question_instances.marks
            
                user_response_instance = subone_models.UserResponse.objects.create(
                    user=request.user,
                    user_quiz=sub_one_user_quiz_instance,
                    question=question_instances,
                    single_selected_choice=quesion_option,
                    question_type=question_instances.question_type,
                    marks=question_mark,
                    is_correct=quesion_option.is_correct,
                )
            else:
                current_question_ans_list = current_question_ans.split(',')
                
                question_correct_options_instance_count = subone_models.Choice.objects.filter(
                        question=question_instances,
                        is_correct=True
                    ).count()
                user_correct_ans = 0
                
                user_response_instance = subone_models.UserResponse.objects.create(
                    user=request.user,
                    user_quiz=sub_one_user_quiz_instance,
                    question=question_instances,
                    question_type=question_instances.question_type,
                )
                
                for ans in current_question_ans_list:
                    
                    quesion_option = subone_models.Choice.objects.filter(
                        question=question_instances,
                        id=ans
                    ).last()
                    user_response_instance.multi_selected_choices.add(quesion_option)
                    
                    if quesion_option.is_correct:
                        user_correct_ans += 1
                
                if user_correct_ans>0:
                    user_question_marsk = user_correct_ans / question_correct_options_instance_count
                    user_response_instance.marks = user_question_marsk
                    user_response_instance.is_correct = True
                    user_response_instance.save()
                            
            

        else:
            return JsonResponse({'error': "Question is not found", "status_code": 500})    
        
                
        return JsonResponse({'success': True, "status_code": 200})

        
@login_required
def submit_quiz(request):
    if request.method == 'GET':
        # Get the submitted question ID and selected answer
        quiz_id = request.GET.get('q_id')
        user_quiz_object = subone_models.SubOneUserQuiz.objects.filter(
            id=quiz_id,
            is_completed=False
        ).last()
        
        if user_quiz_object:
            return JsonResponse({'success': True, "status_code": 200})  # Redirect to the completion page or take appropriate action

        
        
        

@login_required
def complete_quiz(request, q_id=None):
    
    if request.method == 'GET':
        
        if 'question_index' in request.session:
            # request.session.clear()
            request.session.pop("question_index")
            request.session.pop("expiry_time")
        
        if q_id:
            quiz_id=q_id
        else:
            quiz_id = request.GET.get('q_id')
            
        user_quiz_object = subone_models.SubOneUserQuiz.objects.filter(
            id=quiz_id,
        ).last()
        
        total_question = user_quiz_object.question_quantity

        # Retrieve user responses for the quiz
        user_responses = subone_models.UserResponse.objects.filter(
            user=request.user,
            user_quiz=user_quiz_object
        )
        
        user_quiz_object.is_completed = True
        user_quiz_object.save(update_fields=["is_completed"])
        
        total_attempts_question = user_responses.count()
        total_marks = 0
        correct_answers = 0
        incorrect_answers = 0
        for obj in user_responses:
            total_marks +=obj.marks
            correct_answers = user_responses.filter(is_correct=True).count()
            incorrect_answers = user_responses.filter(is_correct=False).count()
        
        # Calculate the result percentage
        if total_question > 0:
            result_percentage = (correct_answers / total_question) * 100
        else:
            result_percentage = 0
        
        return render(request, 'subone/quiz_complete.html', {
            'total_questions': total_question,
            'correct_answers': correct_answers,
            'score': correct_answers,  # You can use a different scoring system if needed
            'result_percentage': result_percentage,
            'incorrect_answers':incorrect_answers
        })