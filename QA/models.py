from django.conf import settings
from django.db import models
from django.urls.base import reverse
from user.models import User



class Question(models.Model):
    title = models.CharField(max_length=100)
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('QA:question_detail', kwargs={'pk': self.id})

    def can_accept_answers(self, user):
        return user == self.user

    def get_comment_count(self):
        return Question.answer_set.count()

class Answer(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE,related_name='answers')
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.answer