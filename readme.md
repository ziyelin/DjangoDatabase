"""

--Files Layout
--Ontology
--Usage

#####

--Files Layout

lab4site
   |-manage.py
   |-readme.md
   |-polls
   |	|-forms.py
   |	|-admin.py
   |	|-models.py
   |	|-views.py
   |	|-test_models.py
   |	|-test_help_validate_views.py
   |	|-test_views.py
   |	|-templates-
   |	|-migrations-	
   |
   |-labrsite
	|-settings.py
	|-urls.py
	|-wsgi.py

######

--Ontology of the Database: 

The database basically stores two things: 1) data about the quiz , 2)data about quiz taker

For the first part, quizzes information are stored in three tables: answer, question and quiz. The quiz table includes info about the title of the quiz, total number of questions in the quiz, etc. The question table includes info about the body of the question, which quiz it belongs to, etc. The answer table includes the body of the answer, the score and which question it belongs to.

For the second part, we have a table from Django called User to record the basic info like username, password, email of the quiz taker. When a quiz taker takes a quiz, we use an instance from the table called attempt to mark that a quiz taker is sitting for some quiz.The attempt table records who is taking the quiz, which quiz he is taking,  his total score, has he finished the quiz, and the last time he modified the quiz. Of course those info are generated and written to the database on the fly. We also have table called AnswerAttempt. Each time an ansewr is posted by a quiz taker, we create an instance to store the answers that quiz taker submits. The answerattempt table as the name suggests includes info about answer and attempt.

#####

--Usage

-How to load data to database?

Go to the admin page "zlin.master.cs.haverford.edu/admin" with username 'zlin' and password see email, add data of quizzes, questions and answers in order. For information about each model and requirements for each field, please refer to the following table: 
   Model  	      Field    	     	    ForeignKey?	Must/Optional
   Quiz		      title		    N  		Must
   Quiz		      description	    N  		Optional
   Quiz		      question_total_number N  		Optional
   Question	      orderinquiz	    N  		Optional
   Question	      text		    N  		Must
   Question	      quiz		    Y  		Must
   Answer	      text		    N  		Must
   Answer	      score		    N  		Must
   Answer	      question		    Y  		Must

-How to check the total score of a quiz taker ?

Go to the admin  page "zlin.master.cs.haverford.edu/admin". Find the 'attempt' entry in polls. Each attempt is named by the convention username + '_attempt_'+attempt_id.  For example a user 'zlin' with attempt id '001' will be shown as 'zlin_attempt_001'. Click the button of the attempt that you want to check its score. The score as well as other info related to the attempt is displayed. What need to notice here is that if the finish status is 0, the total score will be the default score, which is 0 in our case.


-How to run unit test?
Go to the level where manage.py is located, in the command line, type './manage.py test --keepdb'. 

-How to play the quiz:
Go to 'zlin.master.cs.haverford.edu/'. 
