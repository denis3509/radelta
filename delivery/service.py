from decimal import Decimal

from delivery import models as mdl, serializers
from delivery.exchangerate import ExchangeRate


def calculate_cost(cost: Decimal, weight_kg: Decimal,
                   usd_rate: Decimal
                   ) -> Decimal:
    """
        calculates delivery cost
    """
    weight_kg = Decimal(weight_kg)

    return weight_kg * Decimal('0.5') + cost * Decimal('0.01') * usd_rate


def update_pkg_delivery_cost(pkg: mdl.Package, save=True):
    """updates package delivery cost
       using actual exchange rates"""
    ex_rates = ExchangeRate('RUB')
    usd_rate = ex_rates.get_by_code('USD')
    pkg.delivery_cost = calculate_cost(pkg.cost, pkg.weight, usd_rate)
    if save is True:
        pkg.save(update_fields=['delivery_cost'])


def update_delivery_costs():
    """"calculates delivery costs for packages that wasn't processed"""
    to_update = []
    for pkg in mdl.Package.objects.filter(delivery_cost__isnull=True):
        update_pkg_delivery_cost(pkg, save=False)
        to_update.append(pkg)
    mdl.Package.objects.bulk_update(to_update, fields=['delivery_cost'])


def register_package(data: dict, session_key: str) -> mdl.Package:
    """ creates Package with given data
    and updates delivery_cost using actual exchange rates"""

    ser = serializers.CreatePackage(data=data)
    ser.is_valid(raise_exception=True)
    pkg = ser.save(session_id=session_key,
                   registration_status=mdl.Package.SUCCESS)

    pkg.save()
    return pkg


