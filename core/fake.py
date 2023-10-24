from decimal import Decimal

from faker import Faker


class BaseFaker(Faker):
    def decimal(self, start=0, stop=1, decimal_places=2):
        num = self.random.uniform(start, stop)
        decimal_num = Decimal(str(round(num, decimal_places)))
        return decimal_num