from django.test import TestCase

from models import Quiz, Question, Attempt, AnswerAttempt, Answer
from forms import UserForm
from datetime import timedelta, datetime


from views import validate_id_list, invalid_post, valid_quiz_id, same_question,hacker_detected, hacker_detected1, hacker_detected2, valid_quiz,questiontoquiz,time_too_long,update_last_modified, is_answerset_empty, is_timestamp_updated,TIMETHRESHOLD, associate_quiz

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

from polls.views import same_question,valid_quiz,questiontoquiz

from test_models import QuizTestCase,AnswerTestCase
from django.test.client import RequestFactory


class ValidateTestCase(AnswerTestCase):
    """ Test helper functions in views.py. 
    
    helper functions are the functions in views.py not
    directly triggered by a url. They are for the purpose
    of validating, or other helps.

    """
    def setUp(self):
        super(ValidateTestCase,self).setUp()
        self.factory = RequestFactory()

    def testSameQuestion(self):
        """Test views.same_question function."""
        bench_id = Answer.objects.get(text="Garfield").id
        
        id_list_1 =[1,2,3,4]           #answer 1,2,3,4 belong to question 1
        id_list_2 = [1,2,3,5]          # answer 5 belong to question 2
        
        boo1 = same_question(bench_id, id_list_1)
        boo2 = same_question(bench_id, id_list_2)
        self.assertEquals(boo1,True),"should come from the same question"
        self.assertEquals(boo2,False),"not come from the same question"

    def testValidQuiz(self):
        """Test views.validate_quiz"""
        
        request = self.factory.get('/login/')
        myattempt=Attempt.objects.get(id=1)
        myattempt.quiz = Quiz.objects.get(id=1)
        myattempt.save()
        boo1 = valid_quiz(1,1,request)     #question 1 belongs to quiz 1
        boo2 = valid_quiz(1,5,request)     # question 5 belongs to quiz 2
        self.assertEquals(boo1,True),"attempt is coherent with the question"
        self.assertEquals(boo2,False),"the quiz of the attempt does not contain the question"

    def testTimeTooLong(self):
        """ Test views.time_too_long and views.update_last_modified.

        This one can test two functions. 
        """
        myattempt = Attempt.objects.get(id=1)
        myattempt.last_modified = timezone.now()-timedelta(hours=1)
        myattempt.save()
        boo1 = time_too_long(1)
        self.assertEquals(boo1, True)
        update_last_modified(attempt_id = 1)
        boo1 = time_too_long(1)
        self.assertEquals(boo1, False)

    def testAssociateQuiz(self):
        """ Test views.associate_quiz. """
        myattempt = Attempt.objects.get(id = 1)
        self.assertEqual(myattempt.quiz, None)
        myquestion = Question.objects.get(id = 4)
        self.assertEqual(myquestion.quiz.id, 1)
        associate_quiz(attempt_id = 1, question_id = 4)
        myattempt = Attempt.objects.get(id = 1)
        self.assertEqual(myattempt.quiz.id, 1)

        myattempt = Attempt.objects.get(id = 1)
        myattempt.quiz = None
        myattempt.save()
        
    def testEmptyAnswerSet(self):
        """ Test views.is_answerset_empty. """
        boo1 = is_answerset_empty(1, 1)
        self.assertEquals(boo1,True)
        myanswer = Answer.objects.get(id=1)
        myattempt = Attempt.objects.get(id=1)
        self.assertEqual(myanswer.question.id, 1)
        AnswerAttempt.objects.create(answer=myanswer, attempt=myattempt)
        boo2 = is_answerset_empty(attempt_id=1, question_id=1)
        self.assertEquals(boo2, False)
        
    
