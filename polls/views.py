from models import Quiz, Question, Attempt, AnswerAttempt, Answer
from forms import UserForm
from datetime import datetime

from django.template import loader, RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


QUESTION_DEFAULT_ID= '2'
QUIZ_DEFAULT_ID = '1'
QUESTION_DEFAULT_ORDER= '1'
ATTEMPT_DEFAULT_ID = '1'
DEFAULT_USERNAME = 'zlin'
TIMETHRESHOLD = 30
TINYTHRESHOLD = 1

def home_page(request):
    """"Load the homepage"""
    return render(request,'homepage.html')

def sign_up(request):
    """Load the sign up page."""
    return render(request,'sign_up.html')

 
def start_journey(request):
    """Post sign up info.
    
    If info is valid, create new user;
    if info incorrect, return error message page;
    if method is not post, return Hacker message.
 
    """
    if request.method == 'POST':
       uf = UserForm(request.POST)
       # Create new user. 
       if uf.is_valid():
           user =User.objects.create_user(
               username=request.POST['username'],
               password=request.POST['password'],
               email=request.POST['email'],
               first_name = request.POST['first_name'],
               last_name = request.POST['last_name'],
           )
           user.save()
           return HttpResponseRedirect(reverse('login'))
       
       else:
           return render(request,'incorrect_registration_info.html') 
    
    else:   
        return hacker_detected1(request)


def quiz_list(request):
    """Show quizzes availabe.

    Create a new attempt for the login user.

    """
    # Case one: user just logged in  
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(username=user_name,
                          password=password)
      
        # Validate the user.
        if user is not None:
            if user.is_active == True:
                login(request, user)
            else: 
                return hacker_detected1(request)
        else:
            # Tell the user log in fails.
            context = {
              'user_name': user_name
              }
            return render(request,'incorrect_password.html',context)
   
    # Case two : an authenticated user has just completed his or her previous attempt
    elif request.user.is_authenticated():
        user = request.user

    # Case three someone who wants to hackin.      
    else:    
        return hacker_detected1(request)

    # Create a new attempt
    new_attempt = Attempt(user = user)
    new_attempt.save()
    quizzes = Quiz.objects.all()
    title='Quizes List'	
    context = {
        'quizzes': quizzes,
        'title' : title,
        'attempt_id': new_attempt.id
        }
    return render(request,'quiz_list.html',context)


def quiz_question_list(
    request, 
    attempt_id=ATTEMPT_DEFAULT_ID, 
    quiz_id=QUIZ_DEFAULT_ID,
    ):
    """ Show available questions; Record answers submited;
    
    The function is called either directly after a user log in 
    or after a user finished answering a question. 
    In the former case, request.method is POST; 
    in the latter case, request.method is GET. 

    """
   
    # Check the validility of user, attempt, quiz 
    # and the current attempt_status. 
    if not request.user.is_authenticated():
        return hacker_detected1(request)

    try:
	current_attempt =  Attempt.objects.get(id = attempt_id)
    except Attempt.DoesNotExist:
	return hacker_detected2(request)
   
    try:
       x = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
       return hacker_detected2(request)

    if Attempt.objects.get(id = attempt_id).finish_status == 1:
	return hacker_detected2(request)
    if time_too_long(attempt_id):
	return hacker_detected(request)
		
    # Case 1: the user has just finished some other quesiton of the quiz, 
    # record the answers.
    if request.method == "POST":
        question_id=request.POST['question_id']
        if isInteger(question_id)==False:
            return hacker_detected2(request)
        # Check the validity of the question
        try :
            this_question = Question.objects.get(id = question_id)
        except Question.DoesNotExist:
            return hacker_detected2(request)

        answe_id_list=request.POST.getlist('answer')
        if len(answe_id_list) == 0:
            pass

        # Check the validity of the answers posted    
        elif (
                validate_id_list(answe_id_list) and 
                same_question(int(question_id),answe_id_list) and 
                valid_quiz(attempt_id, question_id, request)
            ):

            # Change the timestamp for modification
	    update_last_modified(attempt_id)
            assert (True == is_timestamp_updated(attempt_id)) , "timestamp has not been properly modified"

            answer_set = this_question.answer_set.all()
            answer_id_set = [item.id for item in answer_set]   
            
            # Delete all the answers to the question under this specific attempt.
            for i in answer_id_set : 
                this_answer = Answer.objects.get(id=i)
                AnswerAttempt.objects.filter(attempt_id=attempt_id,
                                             answer_id = i).delete()
                current_attempt.answer.remove(this_answer)
            assert (True == is_answerset_empty(attempt_id,question_id)), "Legacy answers have not been completed removed"
        else:
             return invalid_post(request)

        # Store new attempt_answers and write to database. 
        for i in answe_id_list:
            current_answer = Answer.objects.get(id=i)
            answer_attempt=AnswerAttempt(
                answer=current_answer,
                attempt=current_attempt
            )
            answer_attempt.save()    
            # Add many to many relation
            current_attempt.answer.add(current_answer)
   
    # Display the question list
    quiz_id = int(quiz_id)
    this_quiz=Quiz.objects.get(id=quiz_id)
    quiz_question_set = this_quiz.question_set.all()
    template = loader.get_template('question_list.html')
    context = {
        'questions' : quiz_question_set,
        'quiz_id' : quiz_id,
        'attempt_id' : attempt_id,
        'title' : 'Question List of %d' %(quiz_id)
        }
    return HttpResponse(template.render(context,request))


def one_question_score(attempt_id, question_id):
    """ Calculate the score of one question.                                                                                                                     
    Input : attempt id, question id                                                             
    Output : an integer, representing the total score of this question                          
                                                                                                
    """

    attempt_id = int(attempt_id)
    question_id = int(question_id)
    score_other = 1                  # score for partially correct answers
    score_correct = 0                # score for full credit answer
    this_attempt = Attempt.objects.get(id = attempt_id)
    
    # Get the answer set of the current attempt of this specific question
    answerset= this_attempt.answer.filter(question__id=question_id)

    if len(answerset) == 0:
        pass
    else:
        for item in answerset:
            score_other = score_other * item.score
	    if item.score == 1:
		score_correct = score_correct+1

    return score_other*score_correct


def show_quiz_score(request, attempt_id=ATTEMPT_DEFAULT_ID):
    """Display the quiz score and write quiz score to database

    The function calculate the total score for the attempt. If the finish_status
    is marked 1, it means the score has been calculated before, and thus will return
    the total score of the attempt already stored in the database; if the finish_status
    is marked 0, it will calculate the total score, write that score to database, change
    the finish_status to 1 and display the total score.

    """
   	
    attempt_id = int(attempt_id)
    if not request.user.is_authenticated():
        return hacker_detected1(request)
    try:
        this_attempt = Attempt.objects.get(id=attempt_id)
    except Attempt.DoesNotExist:
        return hacker_detected2(request)
    answer_attempt_set = AnswerAttempt.objects.filter(attempt_id=attempt_id)
    template=loader.get_template('show_score.html')    
    question_id_set = []
    this_attempt = Attempt.objects.get(id=attempt_id)

    # Create a set containing the ids of the questions
    # that have been answered in this attempt.
    for i in answer_attempt_set:
        if i.answer.question.id in question_id_set:
            pass
        else:
            question_id_set.append(i.answer.question.id)
    
    score = 0

    if request.method != "POST" or this_attempt.finish_status == 1:
        score = this_attempt.total_score
    else:
        # Calculate score for each question in the question set.
        this_attempt = Attempt.objects.get(id = request.POST['attempt_id'])
        for item in question_id_set:
            score = score + one_question_score_level(attempt_id, item)
            this_attempt.total_score = score
            this_attempt.save()
    
    this_attempt.finish_status=1
    if len(question_id_set) > 0:
    	associate_quiz(attempt_id, question_id_set[0])
    this_attempt.save()        
    context = {
            'score' : score,
            'title' : 'Total Score of %d' % (attempt_id)
          }

    return HttpResponse(template.render(context, request))

def end_journey(request):
    """ Logout the user."""
    if not request.user.is_authenticated():
            return hacker_detected1(request)
	
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def question_answer_list(
        request,
        attempt_id=ATTEMPT_DEFAULT_ID,
        quiz_id=QUIZ_DEFAULT_ID,
        question_id=QUESTION_DEFAULT_ORDER
    ):
    """Desplay the answers of a question"""
    # the user is done with her current session                                                
    if not request.user.is_authenticated():
        return hacker_detected1(request)

    # recognized user but a fake attempt_id                                                                      
    try:
	x =  Attempt.objects.get(id = attempt_id)
    except Attempt.DoesNotExist:
	return hacker_detected2(request)
    if time_too_long(attempt_id):
	return hacker_detected(request)    
    
    try:
        x = Quiz.objects.get(id = quiz_id)
    except Quiz.DoesNotExist:
        return hacker_detected2(request)

    try:
        current_question = Question.objects.get(id = question_id)
    except Question.DoesNotExist:
        return hacker_detected2(request)

    answer_set = current_question.answer_set.all()
    template = loader.get_template('display_question.html')
    
    context = {
        'answerset' : answer_set,
        'attempt_id': attempt_id,
        'quiz_id': quiz_id,
        'question' : current_question
        }
    return HttpResponse(template.render(context,request))

def isInteger(x):
    """Test if the input is an integer or a string of integers"""
    try :
        x += 1
    except TypeError:
        try: 
            int(x)
        except ValueError:
            return False
    return True

def validate_id_list(idlist):
    """ Tell if the id list is valid

    Input : a list of integers ideally
    Output: True if idlist is a list of integers
    False if not

    """
    n = len(idlist)
    for i in range(0,n):
        try:
            int(idlist[i])
            pass
        except ValueError:
            return False
    return True

def invalid_post(request):
    """ Render the Ivalid Post webpage"""
    return render(request,'invalid_post.html')

def valid_quiz_id(thisid):
    """ Test if the quiz exists. """
    try:
        Quiz.objects.get(id=thisid)
    except Quiz.DoesNotExist:
        return False
    return True
    
        
def same_question(benchmark_id, id_list):
    """ Check if the answer list belong to the benchmark question.

    Prerequisite : id_list is of length at least 1
    Input: benchmark_id : the id of the benchmark question
    Input: id_list: a list of answers by id
    Output : True : if the answers all belong to the benchmark question
    Output : False : if otherwise
    
    """
    n = len(id_list)
    try:
        current_id=0
        for i in range (0,n):
            current_id = Answer.objects.get(id=id_list[i]).question.id
            if current_id == benchmark_id:
                pass
            else:
                return False
        return True
    except ObjectDoesNotExist:
        return False



def hacker_detected(request):
    """ Return a warning page.
    
    The session has expired
    
    """
    return render(request,'hacker_detected.html')

def hacker_detected1(request):
    """ Return a waring message.

    An unauthenticated user is trying to hack. 
    """
    return render(request,'hacker_detected1.html')


def hacker_detected2(request):
    """ Return a warning message.
    
    An authenticated user is doing things insane.
    """
    return render(request,'hacker_detected2.html')



def valid_quiz(attempt_id, question_id, request):
    """ Test the relation of the question to the attempt
    
    In one attempt, a user may answer questions from the same quiz.
    The function decides if the question belongs to the quiz the current
    attempt is on. If the current attempt is not associated with any 
    quiz, associate the attempt with the quiz

    Input : attempt_id, question_id
    Output: decide if the question is valid True/False

    """
    attempt_id = int(attempt_id)
    try:
        x =  Attempt.objects.get(id = attempt_id)
    except Attempt.DoesNotExist:
        return False
    # case when the attempt is not associated with any quiz 
    if x.quiz is None:
        myquiz = questiontoquiz(question_id, request)
        x.quiz = myquiz
        x.save()
        return True
    # case when the attempt is associated with some quiz
    this_quiz = questiontoquiz(question_id,request)    
    if x.quiz_id != this_quiz.id:
        return False
    return True

'''
def test_attempt_finish(attempt_id,request):
    x = Attempt.objects.get(id=attempt_id)
    if x.finish_status==1:
        return hacker_detected(request)
    else:
        pass
'''


def questiontoquiz(question_id, request):
    question_id=int(question_id)
    """ Get the quiz pointed to by the question"""
    try:
        x =  Question.objects.get(id=question_id)
    except Attempt.DoesNotExist:
        return hacker_detected2(request)
    return x.quiz    


def time_too_long(attempt_id):
    """ Tell if the the time lapse has been too long

    The quiz taker cannot resume the quiz if the last
    time he/she writes an answer under the attempt was long ago
    which forces the user to start a new attempt.

    """
    attempt_id = int(attempt_id)
    try:
        x =  Attempt.objects.get(id = attempt_id)
    except Attempt.DoesNotExist:
        return True                # return a value that will lead to an error	
    diff = timezone.now() - x.last_modified
    if diff.total_seconds()/60 > TIMETHRESHOLD:
	return 	True	
    else:
        return False

def update_last_modified(attempt_id):
    """ Update the time the attempt is modified

    Should be triggered whenever a new answer is written to the database
    """
    attempt_id = int(attempt_id)
    try:
        x =  Attempt.objects.get(id = attempt_id)
    except Attempt.DoesNotExist:
        return True
    x.last_modified=timezone.now()
    x.save()

def associate_quiz(attempt_id, question_id):
    """ associate the attempt to a quiz """	
    attempt = Attempt.objects.get(id = attempt_id)
    myquiz = Question.objects.get(id = question_id).quiz
    attempt.quiz = myquiz
    attempt.save()
	
def is_answerset_empty(attempt_id,question_id):	
    """ Tell if the answerset of this question under this attmept is empty

    Whenever a user post some answer, before they can be recored
    we need to makesure the answerset of this question under this 
    attempt is empty.
    
    Input : attempt id , question id;
    Output: True / False
    """
    this_question=Question.objects.get(id = question_id)
    answer_set = this_question.answer_set.all()
    answer_id_set = [item.id for item in answer_set]

    for i in answer_id_set :
        this_answer = Answer.objects.get(id=i)
        x= AnswerAttempt.objects.filter(attempt_id=attempt_id,
                                             answer_id = i).all()
        if len(x) > 0: 
            return False
        
    return True


def is_timestamp_updated(attempt_id):
    """ Check if the time_stamp of last_modified has been updated"""
    attempt_id = int(attempt_id)
    x =  Attempt.objects.get(id = attempt_id)
    diff = timezone.now()-x.last_modified
    if diff.total_seconds() < TINYTHRESHOLD:
        return True
    return False

def one_question_score_level(attempt_id, question_id):
    """ Calculate the score of one question.  

    Input : attempt id, question id                                            
    Output : an integer, representing the total score of this question                                  
    """

    attempt_id = int(attempt_id)
    question_id = int(question_id)
    score_other = 1                  # score for partially correct answers      
    score_correct = 0                # score for full credit answer             
    this_attempt = Attempt.objects.get(id = attempt_id)

    # Get the answer set of the current attempt of this specific question       
    answerset= this_attempt.answer.filter(question__id=question_id)

    if len(answerset) == 0:
        pass
    else:
        for item in answerset:
            score_other = score_other * item.score/2
            if item.score == 2:
                score_correct = score_correct+1

    return score_other*score_correct

