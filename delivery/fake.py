from core.fake import BaseFaker
from delivery import models as mdl


class DeliveryFaker(BaseFaker):
    """Mock data generator for Delivery"""

    def package(self, session_key, save=True, delivery_cost=None):
        pkg = mdl.Package(
            session_id=session_key,
            name=self.word(),
            weight=self.decimal(10, 20),
            cost=self.decimal(10, 20),
            type_id=self.random.choice([1, 2, 3]),
            delivery_cost=delivery_cost,
        )
        if save:
            pkg.save()
        return pkg
