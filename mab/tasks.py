from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from .utils import update_algorithm_data

logger = get_task_logger(__name__)


@periodic_task(
    run_every=crontab(minute='*/30'),
    name="update_algorithm_data",
    ignore_result=True
)
def update_algorithm_data_task():
    update_algorithm_data()
    logger.info("Updated")


@task(name="finish_visit_exploration_task")
def finish_visit_exploration_task(visit):
    logger.info("Visit expired")
    logger.info(visit)

    visit.expired = True
    visit.save()
    logger.info(visit.expired)
    return
    