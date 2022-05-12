from django.urls import path

from . import views

# The view argument is a view function or the result of as_view() for class-based views. It can also be an django.urls.include().

""""
path()
path(route, view, kwargs=None, name=None)¶
Returns an element for inclusion in urlpatterns
"""

urlpatterns = [
    path("", views.index, name="index")
]