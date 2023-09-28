from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from modone import models as mode_models
from django.utils import timezone
from datetime import datetime, timedelta
from core import utils as core_utils
from django.http import JsonResponse

@login_required
def select_semester(request):
    semesters = mode_models.Semester.objects.all()
    return render(request, 'modone/select_semester.html', {'semesters': semesters})


@login_required
def select_semester_quantity(request, semester_id):
    semesters = get_object_or_404(mode_models.Semester, id=semester_id)
    return render(request, 'modone/select_semester_quantity.html', {'semesters': semesters})


@login_required
def start_semester_quiz(request, semester_id):
    if request.method == 'GET':
        question_index = int(request.GET.get('question_index', 0))
        num_questions = int(request.GET.get('num_questions', 20))
        quiz_id = request.GET.get('q_id', None)
        semester = mode_models.Semester.objects.get(id=semester_id)
        if 'question_index' not in request.session:
            request.session['question_index'] = question_index  # Initialize question index
            request.session['semester_id'] = semester_id  # Store subject ID in session
            expired_time = core_utils.get_datetime(timezone.now()+timedelta(seconds=(num_questions*90)))
            formatted_expiry_time = expired_time.strftime('%Y-%m-%d %H:%M:%S')
            request.session['expiry_time']=formatted_expiry_time
        else:
            request.session['question_index'] =question_index    
            
        question_instances = mode_models.Question.objects.filter(Semesters__id=semester_id).order_by('?')[:num_questions]
        
        
        mod_one_user_quiz_instance_list = []
        
        if not quiz_id:
            
            modone_user_quiz_instance = mode_models.ModOneUserQuiz.objects.filter(
                    user=request.user,
                    question_quantity=num_questions,
                    semester=semester,
                    is_completed=False
            ).last()
        else:
            
            modone_user_quiz_instance = mode_models.ModOneUserQuiz.objects.filter(
                    user=request.user,
                    id=quiz_id,
                    is_completed=False
            ).last()
            
        total_attempts = mode_models.ModUserResponse.objects.filter(
                user=request.user,
                user_quiz=modone_user_quiz_instance,
            ).count()

        if not modone_user_quiz_instance:
            modone_user_quiz_instance = mode_models.ModOneUserQuiz.objects.create(
                user=request.user,
                question_quantity=num_questions,
                quiz_start_time=core_utils.get_datetime(timezone.now()),
                quiz_end_time=core_utils.get_datetime(timezone.now()+timedelta(seconds=(num_questions*90))),
                semester=semester
            )
            
            if modone_user_quiz_instance:
                for question in question_instances:
                    modone_user_quiz_instance.question.add(question)
        
        total_question = modone_user_quiz_instance.question.all().count()
        
        mod_one_user_quiz_instance_list = modone_user_quiz_instance.question.all().order_by('pk')
        
        count = 1
        question_id_with_index_list = []
        
        for obj in mod_one_user_quiz_instance_list:
            
            user_submitted_quesion = mode_models.ModUserResponse.objects.filter(
                user=request.user,
                user_quiz=modone_user_quiz_instance,
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
                
        total_question=question_instances.count()
        
              
        if request.session['question_index'] <= (len(mod_one_user_quiz_instance_list) - 1):
                
            current_question = mod_one_user_quiz_instance_list[request.session['question_index']]
            
            question_option_instances = mode_models.Choice.objects.filter(question=current_question)
            
            
            current_question_is_submited = False
            current_question_submitted = mode_models.ModUserResponse.objects.filter(
                user=request.user,
                user_quiz=modone_user_quiz_instance,
                question=current_question
            ).last()
            if current_question_submitted:
                current_question_is_submited=True
                
            question_option_instances_list =[]
            question_count = 0
            
            for question_option_instances in question_option_instances:
                question_details = question_option_instances.get_details()
                if current_question_submitted:
                    if current_question_submitted.question_type == mode_models.Question.MCQ:
                        user_submitted_answers = current_question_submitted.single_selected_choice.id
                        question_details["user_submitted_answers"] = user_submitted_answers
                    else:
                        user_submitted_answers = [obj.id for obj in current_question_submitted.multi_selected_choices.all()]
                        question_details["user_submitted_answers"] = user_submitted_answers
                        
                question_option_instances_list.append(
                    {
                        "option":question_details,
                        "index_by_number":question_count
                    }
                )
                question_count +=1
            
            return render(
                request, 
                    'modone/start_semester_quiz.html',{
                    'semesters': semester, 
                    "current_question": current_question,
                    "question_option_instances":question_option_instances_list,
                    "current_index":request.session['question_index'],
                    "user_quiz_question_instace_id":modone_user_quiz_instance.id,
                    "current_index_for_dipslay":request.session['question_index']+1,
                    "total_question":total_question,
                    "question_id_with_index_list":question_id_with_index_list,
                    "current_question_id":current_question.id,
                    "number_of_questions":modone_user_quiz_instance.question_quantity,
                    "current_question_is_submitted":current_question_is_submited,
                    "total_attemps":total_attempts
                }
            )
        else:
            return redirect('semester_quiz_complete', q_id=modone_user_quiz_instance.id)
        
    if request.method == 'POST':
        semester = mode_models.Semester.objects.get(id=semester_id)
        
        number_of_questions = int(request.POST.get("num_questions"))
        current_quiz_id=request.POST.get("current_quiz_id")
        current_question_id=request.POST.get("current_question_id")
        current_question_ans=request.POST.get("current_question_ans")
        question_type=request.POST.get("question_type")

        question_instances = mode_models.Question.objects.filter(
            Semesters=semester,
            id=current_question_id,
            question_type=question_type
        ).last()
        
        sub_one_user_quiz_instance = mode_models.ModOneUserQuiz.objects.filter(
                id=current_quiz_id,
                user=request.user,
                semester=semester,
                question_quantity=number_of_questions,
                is_completed=False
        ).last()
        question_mark = 0
        
        user_question_response_instance = mode_models.ModUserResponse.objects.filter(
                    user=request.user,
                    user_quiz=sub_one_user_quiz_instance,
                    question=question_instances,
                    question_type=question_instances.question_type,
                ).last()
        
        if user_question_response_instance:
            return JsonResponse({'error': "YOu have already summmited answer for this question", "status_code": 500})  
        
        if question_instances and sub_one_user_quiz_instance:
            if question_type == mode_models.Question.MCQ:
                
                quesion_option = mode_models.Choice.objects.filter(
                    question=question_instances,
                    id=current_question_ans
                ).last()
                
                if quesion_option.is_correct:
                    question_mark = question_instances.marks
            
                user_response_instance = mode_models.ModUserResponse.objects.create(
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
                
                question_correct_options_instance_count = mode_models.Choice.objects.filter(
                        question=question_instances,
                        is_correct=True
                    ).count()
                user_correct_ans = 0
                
                user_response_instance = mode_models.UserResponse.objects.create(
                    user=request.user,
                    user_quiz=sub_one_user_quiz_instance,
                    question=question_instances,
                    question_type=question_instances.question_type,
                )
                
                for ans in current_question_ans_list:
                    
                    quesion_option = mode_models.Choice.objects.filter(
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
def semester_quiz_complete(request, q_id=None):
    
    if request.method == 'GET':
        
        if 'question_index' in request.session:
            request.session.pop("question_index")
            request.session.pop("expiry_time")
        
        if not q_id:
            quiz_id = request.GET.get('q_id')
        else:
            quiz_id = q_id 
            
        user_quiz_object = mode_models.ModOneUserQuiz.objects.filter(
            id=quiz_id,
        ).last()
        
        total_question = user_quiz_object.question_quantity

        # Retrieve user responses for the quiz
        user_responses = mode_models.ModUserResponse.objects.filter(
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
        return render(request, 'modone/quiz_complete.html', {
            'total_questions': total_question,
            'correct_answers': correct_answers,
            'score': correct_answers,  # You can use a different scoring system if needed
            'result_percentage': f"{result_percentage:.2f}",
            'incorrect_answers':incorrect_answers,
            "total_attempts_question":total_attempts_question
        })

'''
def quiz(request, topic_id, num_quuestions):
    topic = get_object_or_404(Topic, id=topic_id)
    questions = Question.objects.filter(topic=topic).order_by('?')[:num_questions]

    if request.method == 'POST':
        user_answers = request.POST.getlist('answer')
        user_score = calculate_score(questions, user_answers)

        # Save the user's quiz result
        user_quiz = UserQuiz(user=request.user, topic=topic, total_questions=num_questions, score=user_score)
        user_quiz.save()

        # Create a QuizResult entry
        result = QuizResult(user=request.user, quiz=user_quiz, score=user_score)
        result.save()

        return render(request, 'quiz_completed.html', {'score': user_score})

    return render(request, 'quiz.html', {'topic': topic, 'questions': questions})

'''