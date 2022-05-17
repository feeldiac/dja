import datetime

from django.db import models
from django.utils import timezone
# Clases en Mayus en singular
class Question(models.Model): 
    # id # PK autoincremental, set by django
    # Si termina en field se puede utilizar para un atributo
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    # Dunder string method: This method returns the string representation of the object. This method is called when print() or str() function is invoked on an object.
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    # Cuando borramos una pregunta, se borran en cascada las choices que tenga
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
