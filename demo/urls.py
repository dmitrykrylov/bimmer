from django.conf.urls import url
from .views import IndexView, GoalView

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^goal/$', GoalView.as_view(), name='goal'),
]