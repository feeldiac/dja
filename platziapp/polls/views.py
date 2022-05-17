# from audioop import reverse
from select import select
from urllib import request
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question


# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "latest_question_list": latest_question_list
#     })


# # def detail(request, question_id):
# #     question = get_object_or_404(Question, pk=question_id)
# #     return render(request, "polls/detail.html", {
# #         "question": question
# #     })

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Poll does not exist")
#     return render(request, "polls/detail.html", {
#         "question": question
#     })

# #Despues de ejecutar vote
# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/result.html", {
#         "question": question
#     })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """"Return the latest five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        # less than or equal to

class DetailView(generic.DetailView):
    model = Question
    template_name= "polls/detail.html"


class ResultView(generic.DetailView):
    model = Question
    template_name= "polls/result.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    selected_choice = question.choice_set.get(pk=request.POST.get("choice"))
    if not selected_choice:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result", args=(question.id,)))
