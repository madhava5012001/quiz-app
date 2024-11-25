from django.db import models
from django.contrib.auth.models import User
import random


class Question(models.Model):
    ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1
    question = models.TextField(help_text='Question text.')
    is_published = models.BooleanField(default=False, null=True, help_text='Is the question published')
    maximum_marks = models.DecimalField(help_text='Maximum marks for a question', default=4, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.question
class Choice(models.Model):
    MAX_CHOICES_COUNT = 4

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    is_correct =  models.BooleanField(default=False, null=True, help_text='Is the choice published')
    choice = models.TextField(help_text='The choice')

    def __str__(self):
        return self.choice

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.DecimalField(help_text='Total score', default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f'Profile: user={self.user}'

    def get_new_question(self):
        used_questions_pk = AttemptedQuestion.objects.filter(profile=self).values_list('question__pk', flat=True)
        remaining_questions = Question.objects.exclude(pk__in=used_questions_pk)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)

    def create_attempt(self, question):
        attempted_question = AttemptedQuestion(question=question, profile=self)
        attempted_question.save()

    def evaluate_attempt(self, attempted_question, selected_choice):
        if attempted_question.question_id != selected_choice.question_id:
            return

        attempted_question.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question.is_correct = True
            attempted_question.marks_obtained = attempted_question.question.maximum_marks

        attempted_question.save()
        self.update_score()

    def update_score(self):
        marks_sum = self.attempts.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        self.total_score = marks_sum or 0
        self.save()


class AttemptedQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='attempts')
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(help_text='Was this attempt correct?', default=False, null=False)
    marks_obtained = models.DecimalField(help_text='Total marks obtained', default=0, decimal_places=2, max_digits=6)

    def get_absolute_url(self):
        return f'/submission-result/{self.pk}/'



