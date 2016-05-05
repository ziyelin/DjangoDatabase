from django.test import TestCase

from models import Quiz, Question, Attempt, AnswerAttempt, Answer
from forms import UserForm
from datetime import timedelta, datetime


from views import validate_id_list, invalid_post, valid_quiz_id, same_question,hacker_detected, hacker_detected1, hacker_detected2, valid_quiz, questiontoquiz,time_too_long,update_last_modified, is_answerset_empty, is_timestamp_updated,TIMETHRESHOLD, one_question_score, question_answer_list, associate_quiz, isInteger, one_question_score_level

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
from django.contrib.auth.hashers import make_password

from django.test import Client
from test_models import AnswerTestCase

from views import TIMETHRESHOLD

class AdminTestCase(TestCase):

    """ Test all the admin functions """

    def setUp(self):
	""" Create a user named aqua. """
        self.pwd = make_password('12345678')
        new_user = User.objects.create_user(
            username='aqua',
            password = '12345678',
            email = "aqua@gmail.com"
        )
        new_user.save()

    def testLogIn(self):
	""" Test function views.quiz_list.
	
	When a user properly logs in, function quiz_list is called.	
	"""
	
        c = Client()

        # case where the user is authenticated and active
        response = c.post(
            '/quizzes/log_in/?user_name="aqua"',
            {'user_name':'aqua','password':'12345678'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'],'Quizes List')

        # case where the user is not authenticated
        
        myuser = User.objects.get(username = 'aqua')
        response = c.post(
            '/quizzes/log_in/?user_name="aqua"',
            {'user_name':'aqua','password':'1234567'}
        )
        self.assertEqual(response.context['user_name'],'aqua')
        myattempt = Attempt.objects.get(id=1)

        # case where the user is not active

        myuser = User.objects.get(username = 'aqua')
        self.assertEqual(myuser.is_active, True)
        myuser.is_active = False
        myuser.save()
        user = User.objects.get(username = 'aqua')
        self.assertEqual(user.is_active, False)
        response = c.post(
            '/quizzes/log_in/?user_name="aqua"',
            {'user_name':'aqua','password':'12345678'}
        )
        self.assertContains(response,"Hacker",status_code=200)
        myuser = User.objects.get(username = 'aqua')
        myuser.is_active = True                   
        myuser.save()

    def testSignUp(self):
        """ Test function views.quiz_list.
	
	When a user properly logs in, function quiz_list is called.	
	"""
	
        
        c = Client()
        mydata={'username':'sargius',
                'password':'12345678',
                'email':'sargius@gmail.com',
                'first_name': 'Sargius',
                'last_name': 'Rwando'}

	# a new user with valid user name and password
	# a new user should be created
        numuser = len(User.objects.all())
        self.assertEqual(numuser,1)
        response = c.post(
            '/StartJourney/',
            data=mydata
        )
        self.assertRedirects(response,'/login/',status_code=302)
        numuser = len(User.objects.all())
        self.assertEqual(numuser,2)

        # a new user with duplicate user name
        # request to sign up should be denied 
        c = Client()
        response = c.post(
            '/StartJourney/',
             data = mydata
            )
        self.assertContains(response,'Incorrect',status_code=200)
    
    def testLogOut(self):
        """ Test funcion end_journey."""
        c = Client()
        c.login(username='aqua',password='12345678')
        response = c.get('/end_journey/')
        self.assertRedirects(response,'/login/',status_code=302)

class AnswerEventsTestCase(AnswerTestCase):
    """Test functions in views.py related to writing answers.
    
    Inherit from AnswerTestCase. 2 Quizzes, 5 questions and 18 answers
    a user named "aqua" an attempt are inherited.
    """
    def setUp(self):

        super(AnswerEventsTestCase,self).setUp()

    def testQuizList(self):
        """ Test the views.quiz_list function triggered by POST. """
        myuser = User.objects.get(username = 'aqua')
        self.assertEqual(myuser.username,'aqua' )
        c = Client()
        c.login(username='aqua',password='12345678')

        #case get with a login user
        response = c.get('/quizzes/log_in/',{'user_name':'aqua'})
        self.assertEqual(len(response.context['quizzes']),2)

        #case post with correct info
        response = c.post('/quizzes/log_in/',
                          {'user_name':'aqua','password':'12345678'})
        self.assertEqual(len(response.context['quizzes']),2)

        # case post but inccorect password
        response = c.post('/quizzes/log_in/',
                          {'user_name':'aqua','password':'123456*'})
        self.assertEqual(response.context['user_name'],'aqua')

        # case get with a user not login
        c.logout()
        response = c.get('/quizzes/log_in/',{'user_name':'aqua'})
        self.assertContains(response,'Hacker')
        
    def testQuizQuestionList(self):
        """ Test the views.quiz_question_list function. 
        
        As quiz_question_list is the function that writes to our database, 
        it is the very function best needed testing against malicious action.
        """
        c = Client()
        c.login(username='aqua',password='12345678')
        myattempt = Attempt.objects.get(id=1)
        self.assertEqual(myattempt.quiz,None)
        
        # case no such attempt
        response = c.get('/quizzes/coolattempt_id/100/coolquiz_id/1/',
                         {'attempt_id':100,'quiz_id':1})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,'My Dear User',status_code=200)

        # case no such quiz
        response = c.get('/quizzes/coolattempt_id/100/coolquiz_id/1/',
                         {'attempt_id':1,'quiz_id':10})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,'My Dear User',status_code=200)

        # case get correct quiz and attempt
        response = c.get('/quizzes/coolattempt_id/1/coolquiz_id/1/',
                         {'attempt_id':1,'quiz_id':1})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['questions']),4)
        
        # case get time too long
        myattempt = Attempt.objects.get(id = 1)
        myattempt.last_modified = timezone.now()-timedelta(hours = 100)
        myattempt.save()
        response = c.get('/quizzes/coolattempt_id/1/coolquiz_id/1/',
                         {'attempt_id':1,'quiz_id':1})
        self.assertContains(response,'Session Expired',status_code=200)

        # case get : finish status = 1                                                
        myattempt = Attempt.objects.get(id = 1)
        myattempt.last_modified = timezone.now()
        myattempt.finish_status = 1
        myattempt.save()
        response = c.get('/quizzes/coolattempt_id/1/coolquiz_id/1/',
                         {'attempt_id':1,'quiz_id':1})
        self.assertContains(response,'My Dear User',status_code=200)

        # case post : a valid post (first restore answer)
        myattempt= Attempt.objects.get(id = 1)
        myattempt.last_modified = timezone.now()
        myattempt.finish_status = 0
        myattempt.save()
    
        response = c.post(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/?attempt_id=1&quiz_id=1',
             {'question_id':1, 'answer':[1,2]}
            )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['quiz_id'],1)
        score = one_question_score_level(1, 1)
        self.assertEquals(score , 2)

        # case post : a valid post with no new answers
        # test if the previous answers are preserved
        
        response = c.post(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/?attempt_id=1&quiz_id=1',
             {'question_id':1, 'answer':[]}
            )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['quiz_id'],1)
        score =one_question_score_level(1, 1)
        self.assertEquals(score , 2)

        # case post : a valid post with new answers
        # test if the previous answers are deleted 
        # before new answers are recorded                     

        response = c.post(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/?attempt_id=1&quiz_id=1',
             {'question_id':1, 'answer':[1]}
            )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['quiz_id'],1)
        score =one_question_score_level(1, 1)
        self.assertEquals(score , 1)

        # case post : an invalid post with answers belong to another quiz
        myanswer1 = Answer.objects.get(text = "Maybe")
        myanswer2 = Answer.objects.get(text = "No")
        self.assertEqual(myanswer1.question.quiz.id, 2)
        self.assertEqual(myanswer2.question.quiz.id, 2)
        self.assertEqual(myanswer1.question.id, 5)
        self.assertEqual(myanswer1.question.id, 5)
        response = c.post(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/?attempt_id=1&quiz_id=1',
             {'question_id':5, 'answer':[myanswer1.id,myanswer2.id]}
            )
        self.assertContains(response,'Invalid Input',status_code=200)


        # case post : an invalid post with answers of different questions
        myanswer1 = Answer.objects.get(id=1)
        myanswer2 = Answer.objects.get(id = 7)
        self.assertEqual(myanswer1.question.text, 'What are mammels')
        self.assertEqual(myanswer2.question.text, 'Who is a philosopher')
        response = c.post(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/?attempt_id=1&quiz_id=1',
             {'question_id':1, 'answer':[1,7]}
            )
        self.assertContains(response,'Invalid Input',status_code=200)
        
        # case post : an invalid post with answer id being a string
        response = c.post(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/?attempt_id=1&quiz_id=1',
             {'question_id':1, 'answer':[1,'joker']}
            )
        self.assertContains(response,'Invalid Input',status_code=200)

        # case post : an invalid post with question id being a string                
        response = c.post(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/?attempt_id=1&quiz_id=1',
             {'question_id':"joker", 'answer':[1]}
            )
        self.assertContains(response,'My Dear User',status_code=200)

    def testQuestionAnswerList(self):
        """ Test the views.question_answer_list function."""
        # test if question_answer_list could be properly rendered
        c = Client()
        c.login(username='aqua',password='12345678')
        myattempt = Attempt.objects.get(id=1)
        boo1 = time_too_long(myattempt.id)
        self.assertEqual(boo1, False)
        myquestion = Question.objects.get(id=1)
        answer_set = myquestion.answer_set.all()
        self.assertEqual(len(answer_set),4)

        response = c.get(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/coolquestion_id/1/',
            {'attempt_id':1, 'quiz_id':1, 'question_id':1}
        )

        self.assertEquals(int(response.context['attempt_id']),1)
        self.assertEquals(len(response.context['answerset']), 4)
        
        # test if time_too long will affect the rendering of the question list
        myattempt = Attempt.objects.get(id=1)
        myattempt.last_modified = timezone.now() - timedelta(hours=10)
        myattempt.save()
        boo1 = time_too_long(myattempt.id)
        self.assertEqual(boo1, True)
        response = c.get(
            '/quizzes/coolattempt_id/1/coolquiz_id/1/',
            {'attempt_id':1, 'quiz_id':1, 'question_id':1}
        )

        # render the page telling the user session expired
        self.assertContains(response,'Session Expired',status_code = 200)      


class ScoreEventsTestCase(AnswerTestCase):
    """ Test related to calculating scores.
    
    Inherit from AnswerTestCase. 2 Quizzes, 5 questions and 18 answers                                                                           
    a user named "aqua" an attempt are inherited.                                                                                                 
    """
    def setUp(self):
        super(ScoreEventsTestCase,self).setUp()
        self.c = Client()    

    def testShowTotalScore(self):
        """ Test views.show_quiz_score"""
        # add more answer_attempt instances
	answer1 = Answer.objects.get(text = "Alex")
	answer2 = Answer.objects.get(text = "Kant")
	myattempt = Attempt.objects.get(id = 1)
	AnswerAttempt.objects.create( answer = answer1, attempt = myattempt)
	myattempt.answer.add(answer1)
	AnswerAttempt.objects.create( answer = answer2, attempt = myattempt)
	myattempt.answer.add(answer2)

	# confirm the total score of the second question is 0.5
	score = one_question_score_level(attempt_id = 1, question_id = 2)
	self.assertEqual(score ,0.5)

	# add more answer_attempt instances
	self.help_create_new_answerattempt()
	# confirm the total score of the first question is 2
        score = one_question_score_level(attempt_id=1, question_id=1)
        self.assertEqual(score, 2)
	
	# confirm the attempt is for user 'aqua'
	self.assertEqual(myattempt.user.username, 'aqua')

        # test when attempt_id does not exists
        c = Client()
        c.login(username = 'aqua', password= '12345678')
        response = c.post('/quizzes/coolattempt_id/100/total_score/?attempt_id=100',
                          {'attempt_id':100})
        self.assertContains(response,'My Dear User', status_code = 200)
    
	# test if the total score for the first attempt is 2.5
	c = Client()
        c.login(username='aqua',password='12345678')
	myattempt.finish_status = 0
        myattempt.save()
        response = c.post('/quizzes/coolattempt_id/1/total_score/?attempt_id=1',
                          {'attempt_id':1})
	self.assertEqual(response.context['score'], 2.5)
        myattempt = Attempt.objects.get(id = 1)
        self.assertEqual(myattempt.finish_status, 1)

        # test if the total score when method is get 
        # is still 2.5, no matter how many other answers are given
        answer3 = Answer.objects.get(text = "Leibniz")
        AnswerAttempt.objects.create( answer = answer3, attempt = myattempt)
        myattempt.answer.add(answer3)
        self.assertEqual(answer3.score,1*2)
        
        myattempt.finish_status = 1
        myattempt.save()
        c = Client()
        c.login(username='aqua',password='12345678')
        response = c.get('/quizzes/coolattempt_id/1/total_score/',
                          {'attempt_id':1})
        self.assertEqual(response.context['score'], 2.5)

        # test the total score when method is post
        # should still be 2.5+1*0.5=3  when the finish_status is adjusted back to 0
        myattempt = Attempt.objects.get(id=1)
        myattempt.finish_status = 0
        myattempt.save()
        c = Client()
        c.login(username='aqua',password='12345678')
        response = c.post('/quizzes/coolattempt_id/1/total_score/?attempt_id=1',
                          {'attempt_id':1})
        self.assertEqual(response.context['score'], 3)
