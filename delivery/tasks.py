from celery.schedules import crontab

from core.logging import get_logger
from delivery import service as srv, models
from radelta.celery import celery_app, Queue

logger = get_logger()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """ initialize periodic tasks"""
    sender.add_periodic_task(
        crontab(minute="*/5"),
        update_delivery_costs.s(),
        queue=Queue.MAIN,
        periodic_task_name="update_delivery_costs"
    )


@celery_app.task()
def update_delivery_costs():
    """task: calculates delivery costs for packages that wasn't processed"""
    srv.update_delivery_costs()


@celery_app.task()
def update_pkg_delivery_cost(pkg_id: int):
    """task: update delivery cost for a package"""
    pkg = models.Package.objects.get(id=pkg_id)

    srv.update_pkg_delivery_cost(pkg)


@celery_app.task()
def register_package(data: dict, session_id: str):
    """task: register package and update cost"""
    pkg = srv.register_package(data, session_id)
    update_pkg_delivery_cost.delay(pkg.id)
