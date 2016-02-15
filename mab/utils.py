from .models import Visit, Arm
import random
import math

def update_algorithm_data():
    arms = []

    #  Getting arms. It needs to be rewrited
    arms.append(Arm.objects.get(number=1))
    arms.append(Arm.objects.get(number=2))
    arms.append(Arm.objects.get(number=3))

    counts = [0]*len(arms)
    av_rewards = [0]*len(arms)

    new_data = Visit.objects.filter(
        expired=True,
        deducted=False)

    for visit in new_data:
        counts[visit.arm-1] += 1
        rewards[visit.arm-1] += visit.av_reward

        visit.deducted = True
        visit.save()

    set_updated_data(arms, counts, av_rewards)
    set_probs(arms, counts, av_rewards)


def set_updated_data(arms, counts, av_rewards):
    print(arms)
    print(counts)
    print(rewards)
    for i in range(len(arms)):
        k = counts[i]
        n = arms[i].count + k
        arms[i].count = n

        value = arms[i].av_reward
        new_value = ((n-k))/float(n)*value+(k/float(n))*av_rewards[i]
        arms[i].av_reward = new_value
        arms[i].save()


def categorical_draw(probs):
    z = random.random()
    cum_prob = 0.0
    for i in range(len(probs)):
        prob = probs[i]
        cum_prob += prob
        if cum_prob > z:
            return i
    return len(probs) - 1


def set_probs(arms, counts, av_rewards):
    t = sum(counts) + 1
    temperature = 1 / math.log(t + 0.0000001)

    z = sum([math.exp(a / temperature) for a in av_rewards])
    for i in range(len(arms)):
        a = arms[i].av_reward
        new_prob = math.exp(a / temperature) / z
        arms[i].prob = new_prob
        arms[i].save()


def select_arm():
    arms = get_arms()
    probs = []
    for arm in arms:
        probs.append(arm.prob)
    return categorical_draw(probs)


def get_arms():
    arms = list(Arm.objects.all().order_by('number'))
    return arms
