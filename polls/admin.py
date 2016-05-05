from django.contrib import admin
from models import Answer, Question,Quiz,Attempt, User
'''
class AnswerInline(admin.TabularInline):
    name = Answer
    


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=('orderinquiz','text','quiz_id')
    inlines=[
        AnswerInline,
    ]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=('text','score','question_id')

'''
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz)
admin.site.register(Attempt)    
# Register your models here.
