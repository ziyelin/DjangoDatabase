

from django.test import TestCase
from polls.models import Quiz, Question, Answer, Attempt, AnswerAttempt
from polls.views import one_question_score
from django.contrib.auth.models import User

class QuizTestCase(TestCase):
    """ Check if the Quiz model is properly setup. """
    def setUp(self):
        """ Create two quizzes """
        Quiz.objects.create(title = "Animal", description = "test animl quiz")
        Quiz.objects.create(title = "Computer Science", description = "test a CS quiz")
        
        
    def test_quiz_title(self):
        """ Test if the two quizzes have been properly created """
        animal = Quiz.objects.get(title = "Animal")
        cs = Quiz.objects.get(title="Computer Science")
        self.assertEqual(animal.id, 1)
        self.assertEqual(cs.id, 2)


class QuestionAnswerTestCase(QuizTestCase):
    """ Check if the Question and Answer  models are properly setup. """
    def setUp(self):
        """ Create a question and an answer """
        super(QuestionAnswerTestCase,self).setUp()
        animal = Quiz.objects.get(title = "Animal")
        Question.objects.create(orderinquiz = 1, text = "What are mammels", quiz = animal)
        question_1 = Question.objects.get(text = "What are mammels")
        Answer.objects.create(text="Cat", score = 1, question =question_1)

    def test_answer(self):
        answer = Answer.objects.get(text = "Cat")
        self.assertEqual(answer.score, 1)
        

class AnswerTestCase(TestCase):
    def setUp(self):
        """ Create 2 quizes, 5 questions, 19 answers a user and an attempt.
        
        The first quiz called Animal has 4 questions, each with 4 answers
        The second quiz called Comparison has 1 question, with 3 answers
        """
        Quiz.objects.create(title = "Animal", 
                            description = "test animl quiz")
        animal = Quiz.objects.get(title = "Animal")
        Quiz.objects.create(title = "Comparison")
        comparison = Quiz.objects.get(title = "Comparison")
        
        Question.objects.create(orderinquiz = 1, 
                                text = "What are mammels", 
                                quiz = animal)
        question_1 = Question.objects.get(text = "What are mammels")
        Question.objects.create(orderinquiz = 2, 
                                text = "Who is a philosopher", 
                                quiz = animal)
        question_2 = Question.objects.get(text = "Who is a philosopher")
        Question.objects.create(orderinquiz = 3, 
                                text = "Fifty shades of what", 
                                quiz = animal)
        question_3 = Question.objects.get(text = "Fifty shades of what")
        Question.objects.create(orderinquiz = 4, 
                                text = "Which graduate school ziye is attending", 
                                quiz = animal)
        question_4 = Question.objects.get(text="Which graduate school ziye is attending")
        Question.objects.create(orderinquiz = 1, 
                                text = "Quiz black horse?", 
                                quiz = comparison)
        question_5 = Question.objects.get(text = "Quiz black horse?")




        Answer.objects.create(text="Garfield", 
                              score = 1*2, 
                              question =question_1)
        Answer.objects.create(text="Goofy", 
                              score = 1*2, 
                              question =question_1)
        Answer.objects.create(text="Robin", 
                              score = 0*2, 
                              question =question_1)
        Answer.objects.create(text="Pikachu", 
                              score = 0.5*2, 
                              question =question_1)
        

        Answer.objects.create(text="Alex", 
                              score = 0.5*2, 
                              question =question_2)
        Answer.objects.create(text="Jeff", 
                              score = 0*2, 
                              question =question_2)
        Answer.objects.create(text="Kant", 
                              score = 1*2, 
                              question =question_2)
        Answer.objects.create(text="Leibniz", 
                              score = 1*2, 
                              question =question_2)
        
        
        Answer.objects.create(text="Pizza", 
                              score = 0*2, 
                              question =question_3)
        Answer.objects.create(text="Grey", 
                              score = 1*2, 
                              question =question_3)
        Answer.objects.create(text="Scarlet", 
                              score = 0.5*2,
                              question =question_3)
        Answer.objects.create(text="Rainbow", 
                              score = 0*2,
                              question =question_3)
        
	Answer.objects.create(text="Stanford U", 
                              score = 0*2, 
                              question =question_4)
        Answer.objects.create(text="Boston U", 
                              score = 0.5*2, 
                              question =question_4)
        Answer.objects.create(text="Columbia U", 
                              score = 1*2,
                              question =question_4)
        Answer.objects.create(text="Carnegie Mellon", 
                              score = 0.5*2,
                              question =question_4)
        

        Answer.objects.create(text="Maybe", 
                              score = 1*2, 
                              question =question_5)
        Answer.objects.create(text="No", 
                              score = 0.5*2, 
                              question =question_5)
        Answer.objects.create(text="Yes", 
                              score = 0*2, 
                              question =question_5)
        
        user_1 = User.objects.create_user(username="aqua",
                                          password="12345678",
                                          email="aqua@gmail.com")
        user_1.save()
        
        Attempt.objects.create(user=user_1)
        
        
    def test_answerattempt(self):
        """ Test if answerattempt can properly function"""
	self.help_create_new_answerattempt()  

        quest = Question.objects.get(id=1)
        self.assertEqual(quest.text, "What are mammels")
        attempt1 = Attempt.objects.get(id=1)
        self.assertEqual(attempt1.user.username, 'aqua'),"wrong attempt user name"
        answerset = attempt1.answer.filter(question__id=1)
        self.assertEqual(len(answerset),2)

    def help_create_new_answerattempt(self):
	"""Create two answerattempt """
        answer_1 = Answer.objects.get(text = "Garfield")
        answer_2 = Answer.objects.get(text="Goofy")
        answer_3 = Answer.objects.get(text="Robin")
        answer_4 = Answer.objects.get(text="Pikachu")
        attempt_1 = Attempt.objects.get(id=1)

        AnswerAttempt.objects.create(answer=answer_1, 
                                     attempt= attempt_1)
        attempt_1.answer.add(answer_1)
        AnswerAttempt.objects.create(answer=answer_2,
                                     attempt =attempt_1)
        attempt_1.answer.add(answer_2)  
 


