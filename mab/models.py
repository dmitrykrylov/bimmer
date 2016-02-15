from django.db import models
from django.contrib.sessions.models import Session

import logging


logger = logging.getLogger(__name__)


class Visit(models.Model):
    date = models.DateTimeField()
    arm = models.IntegerField()
    reward = models.FloatField()
    session = models.ForeignKey(Session, null=True)
    expired = models.BooleanField(default=False)
    deducted = models.BooleanField(default=False)

    #   Uje ne nado (?)
    # def finish_visit_exploration(self):
    #     self.expired = True
    #     self.save()


class Arm(models.Model):
    number = models.IntegerField()
    count = models.IntegerField(default=0)
    av_reward = models.FloatField('Average Reward', default=0)
    prob = models.FloatField('Probability', default=0)


#   Later
# class Experiment(models.Model):
#     arms = models.ManyToManyField(Arm)
#     start_date = models.DateTimeField()