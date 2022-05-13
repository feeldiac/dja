from django.urls import path

from . import views

# The view argument is a view function or the result of as_view() for class-based views. It can also be an django.urls.include().

""""
path()
path(route, view, kwargs=None, name=None)¶
Returns an element for inclusion in urlpatterns
"""
app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"), #/polls/
    path("<int:question_id>/", views.detail, name="detail"), #/polls/5/
    path("<int:question_id>/result/", views.result, name="result"), #/polls/5/results/
    path("<int:question_id>/vote/", views.vote, name="vote"), #/polls/5/votes/
    
    
]