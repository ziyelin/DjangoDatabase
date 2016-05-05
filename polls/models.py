from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

QUIZ_DEFAULT_ID = 1
QUESTION_DEFAULT_ORDER= 1
ATTEMPT_DEFAULT_ID = 1
PERSON_DEFAULT_USERNAME = 'zlin1993'


class Quiz(models.Model):     
    title=models.CharField(
			   max_length=60,
			   default="title of the quiz,must be filled",
			   blank=True
			   )
						  
    description=models.TextField(
				 default="a description of the quiz,can be blank",
				 blank=True
				 )
							
    question_total_number=models.IntegerField(default=0)
      
    def get_default_id(self):
        return QUIZ_DEFAULT_ID      

    def __str__(self):
        return self.title
		
		
class Question(models.Model):     
    orderinquiz=models.IntegerField(default=0)
	
    text=models.TextField(
			  blank=True,
			  default="a description of the question, must be filled",
			  )
							 
    quiz=models.ForeignKey(
			   Quiz,
			   default=QUIZ_DEFAULT_ID,
			   on_delete=models.CASCADE,
			   )		       
			     	 
    def get_default_order(self):
        return QUESTION_DEFAULT_ORDER      
        
    def __str__(self):
        return self.text
		                

class Answer(models.Model):    
    text=models.TextField(
			  blank=True,
			  default="a description of the answer, must be filled"
			  )
							 
    score=models.DecimalField(
			      max_digits=2, 
			      decimal_places=1,
			      default=1.0
			      )

    question=models.ForeignKey(
			       Question,
			       default=QUESTION_DEFAULT_ORDER,   
			       on_delete=models.CASCADE,
			       blank=True
			       )
	
    def __str__(self):
        return self.text
							 
                                 
		
class Attempt(models.Model):     
    answer=models.ManyToManyField(Answer)

   
    user = models.ForeignKey(
                             User,
                             on_delete=models.SET_NULL,
                             null = True,
                             blank = True
                            )
    quiz = models.ForeignKey(
                            Quiz,
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True
                             )
    total_score=models.DecimalField(
				    default=0.0,
				    max_digits=5,
				    decimal_places=2
				    )	
    finish_status = models.BooleanField(
				default = False
				)
    last_modified = models.DateTimeField(
		                        default=datetime.now,
					blank=True
					)				   

    def get_default_id(self):
    	return ATTEMPT_DEFAULT_ID       
    
    def __str__(self):
        funnystring = self.user.username+ "_attept_"+str(self.id)
        return  funnystring
			
    	
    	                    
class AnswerAttempt(models.Model):
    answer=models.ForeignKey(
			     Answer,
			     on_delete=models.CASCADE
			     )
  
    attempt=models.ForeignKey( 
			      Attempt,
			      on_delete=models.CASCADE
			      ) 
     
    def __str__(self):
        funnystring = self.attempt.user.username+ ' ' + self.answer.text
        return funnystring

class QuizAttempt(models.Model):
    quiz=models.ForeignKey(
                          Quiz,
                          on_delete=models.CASCADE
                          )
    attempt=models.ForeignKey(
                             Attempt,
                             on_delete=models.CASCADE
                             )
    score=models.DecimalField(
                            default=0.0,
                            max_digits=5,
                            decimal_places=2
                            )
    def __str__(self):
        funnystring = self.attempt.user.username+' ' +self.quiz.title
        return funnystring
 
class QuizQuestionAnswer(models.Model):
    """ This table is reserved for loading data through load_data.py
        
        
    If data is loaded using load_data.py (rather than through
    the admin page manually), this table is  where the loaded
     data is first stored. Then, quiz data, question data and
    answer will be written to the corresponding table in order.
    Then this table will be emptied.
    """

    quiz = models.CharField(
                           max_length=60,
                           default="title of the quiz",
                           blank=True
                           )
    question = models.TextField(
                          blank=True,
                          default="a description of the question",
                          )
    answer = models.TextField(
                          blank=True,
                          default="a description of the answer"
                          )

    score = models.DecimalField(
                            default=0.0,
                            max_digits=5,
                            decimal_places=2
                            )

                                            
