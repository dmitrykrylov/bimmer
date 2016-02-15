
import random

from .models import Visit
from .tasks import finish_visit_exploration_task
from .utils import select_arm

from django.contrib.sessions.models import Session
from django.utils import timezone


GOAL_DICT = {
    'demo/goal/': 1
}


class MultiArmedBanditMiddleware(object):

    def process_request(self, request):
        if 'admin' in request.path:   # Implement checking explored urls
            return

        request.session.save()
        s = Session.objects.get(session_key=request.session.session_key)

        if Visit.objects.filter(session__session_key=s.session_key).exists():
            print('Visit exists')
            v = Visit.objects.get(session__session_key=s.session_key)
        else:
            v = Visit(
                date=timezone.now(),
                reward=0,
                arm=select_arm(),
                session=s)

            v.save()

            finish_visit_exploration_task.apply_async(
                args=[v],
                countdown=10)

            print('Visit has created. Rew:%s. Arm:%s' % (0, 1))

        for goal, reward in GOAL_DICT.items():
            if goal in request.path:
                self.set_reward_score(v, reward)

    def process_template_response(self, request, response):
        if 'admin' not in request.path:
            v = Visit.objects.get(
                session__session_key=request.session.session_key)
            response.template_name = self.generate_template_name(
                response, v.arm)

        return response

    def generate_template_name(self, response, n):
        arm_dir = "mab_templates/arm_%s/" % n
        return ('%s%s' % (arm_dir, response.template_name[0]))


    def set_reward_score(self, visit, reward):
        visit.reward = reward
        visit.save()


#  На всякий случай
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
