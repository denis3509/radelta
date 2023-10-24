from django.core.management.base import BaseCommand

from delivery import tasks


class Command(BaseCommand):
    help = "Runs update costs task"

    def handle(self, *args, **options):
        tasks.update_delivery_costs.delay()
        self.stdout.write(
            self.style.SUCCESS('Task "update_delivery_costs" added to queue')
        )