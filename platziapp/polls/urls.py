from django.urls import path

from .views import DetailView, IndexView, ResultView, vote

# The view argument is a view function or the result of as_view() for class-based  It can also be an django.urls.include().

""""
path()
path(route, view, kwargs=None, name=None)¶
Returns an element for inclusion in urlpatterns
"""
app_name = "polls"
urlpatterns = [
    path("", IndexView.as_view(), name="index"), #/polls/
    path("<int:pk>/", DetailView.as_view(), name="detail"), #/polls/5/
    path("<int:pk>/result/", ResultView.as_view(), name="result"), #/polls/5/results/
    path("<int:question_id>/vote/", vote, name="vote"), #/polls/5/votes/
    
    
]