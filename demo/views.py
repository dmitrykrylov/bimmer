from django.views.generic import TemplateView
import random


class IndexView(TemplateView):

    template_name = 'demo/index.html'


class GoalView(TemplateView):
    
    template_name = 'demo/goal.html'
