from decimal import Decimal

import django.contrib.sessions.models
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _


class PackageType(models.Model):
    name = models.TextField()


def more_than_zero(value: Decimal):
    if value <= Decimal('0'):
        ValidationError(
            _("Invalid value: %(value)s"),
            params={"value": value},
        )


class Package(models.Model):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    REG_STATUS = [
        (SUCCESS, "Success"),
        (FAILURE, "Failure"),
    ]

    session = models.ForeignKey(django.contrib.sessions.models.Session, on_delete=models.PROTECT)
    name = models.TextField(max_length=200)
    weight = models.DecimalField(max_digits=6, decimal_places=3, validators=[more_than_zero])
    type = models.ForeignKey(PackageType, on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=6, decimal_places=2, validators=[more_than_zero])
    delivery_cost = models.DecimalField(null=True, max_digits=6, decimal_places=2, validators=[more_than_zero])
    registration_status = models.TextField(
        choices=REG_STATUS,
        default=PENDING)

    @property
    def display_delivery_cost(self):
        if self.delivery_cost is None:
            return "Not calculated"
        else:
            return self.delivery_cost
