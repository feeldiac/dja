from ast import arg
import datetime
from urllib import response
from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from .models import Question, Choice

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently should return false for questions whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quién es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """
        was_published_recently should return true0 for questions whose pub_date is now.
        """
        time = timezone.now()
        present_question = Question(question_text="¿Quién es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        """
        was_published_recently should return false for questions whose pub_date is in the past
        """
        time = timezone.now() - datetime.timedelta(days=15)
        past_question = Question(question_text="¿Quién es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

def create_question(question_text, days):
    """
    Create a question given a question text and a number of days from wich question was or will be published,
    e.g. days = 1, the question will be published tomorrow, days = -1, the question was published yesterday.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If there's no any question, an appropiate message is displayed
        """
        # self.client, is the built-in Django test client. This isn't a real browser, and doesn't even make real requests. It just constructs a Django HttpRequest object and passes it through the request/response process - middleware, URL resolver, view, template - and returns whatever Django produces. It won't parse that response at all, or render it, and won't make other requests driven by the HTML for assets etc.
        # Se realiza una petición get a la vista Index de Polls utilizando el Cliente ficticio de Django.
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        response = self.client.get(reverse("polls:index"))
        future_question = create_question("lorem ipsum", days=30)
        # Se comprueba que la pregunta creada en el futuro no haga parte del contexto devuelto, es decir que su fecha sea lte-now.
        self.assertNotIn(future_question, response.context["latest_question_list"])

    def test_future_question2(self):
        """
        Questions with pub_date in the future should not be displayed.
        """
        create_question("Future lorem ipsum", days=30)
        response = self.client.get(reverse("polls:index"))
        # La unica question que estará en la bd de testing es la de la línea anterior por tanto no debería retornar ninguna pregunta
        # teniendo en cuenta que solo se renderiza si existe contexto.
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Question with a pub_date in the past should be displayed in the index.
        """
        question = create_question("Past lorem ipsum", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
    
    def test_future_and_past_question(self):
        """
        Even if both, past and future questions exist, only the past question is displayed.
        """
        past_question = create_question(question_text="past lorem", days=-15)
        future_question = create_question(question_text="future lorem", days=15)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )

    def test_two_past_question(self):
        """
        Every question published in the past should be displayed.
        """
        past_question1 = create_question(question_text="past1 lorem", days=-15)
        past_question2 = create_question(question_text="past2 lorem", days=-25)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )
    
    def test_two_future_question(self):
        """
        All the questions with pub_date in the future should not be displayed.
        """
        future_question1 = create_question(question_text="future1 lorem", days=15)
        future_question2 = create_question(question_text="future1 lorem", days=25)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
    
    def test_multiple_future_question(self):
        """
        All the questions with pub_date in the future should not be displayed.
        """
        for n in range(10):
            question = create_question(question_text=f'Lorem {n}', days= n + 1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[])


    def test_multiple_past_question(self):
        """
        All the questions with pub_date in the past should be displayed.
        """
        for n in range(1,21,3):
            question = create_question(question_text=f'Lorem {n}', days= -1 * n)
        response = self.client.get(reverse("polls:index"))    
        self.assertEqual(len(response.context["latest_question_list"]), 5)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 error not found.
        """
        future_question = create_question(question_text="future lorem", days=15)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with pub_date in the past displays the queston's text
        """
        past_question = create_question(question_text="past lorem", days=-15)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        # En el texto de la response debe existir el texto de la pregunta past_question, es decir debería verse en pantalla
        self.assertContains(response, past_question.question_text)

class QuestionResultViewTests(TestCase):

    def create_question_without_choices(self):
        """
        Users shouldn't be able to create a question without defining at least two choice options
        """
        past_question = create_question(question_text="past lorem", days=-15)
        response = self.client.get(reverse("polls:index"))
        choices = response.context["latest_question_list"].choice_set.count()
        self.assertEqual(len(response.context["latest_question_list"]), 0)
