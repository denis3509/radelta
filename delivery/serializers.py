from decimal import Decimal

from rest_framework import serializers

from delivery import models as mdl


class PackageType(serializers.ModelSerializer):
    class Meta:
        model = mdl.PackageType
        fields = "__all__"


class Package(serializers.ModelSerializer):
    class Meta:
        model = mdl.Package

    weight = serializers.DecimalField(min_value=Decimal("0"), decimal_places=3, max_digits=6)
    cost = serializers.DecimalField(min_value=Decimal("0"), decimal_places=2, max_digits=6)


class CreatePackage(Package):
    class Meta(Package.Meta):
        exclude = ['session', 'delivery_cost', 'registration_status']


class GetPackage(Package):
    class Meta(Package.Meta):
        exclude = ['session', 'delivery_cost']

    display_delivery_cost = serializers.CharField()
