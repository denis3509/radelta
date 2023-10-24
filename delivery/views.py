from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework import mixins
from rest_framework import serializers as drf_serializers
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response


from delivery import models as mdl, tasks
from delivery import serializers
from radelta.views import BasePagination


class PackageTypeList(mixins.ListModelMixin,
                      generics.GenericAPIView):
    queryset = mdl.PackageType.objects.all()
    serializer_class = serializers.PackageType
    pagination_class = BasePagination

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT}
    )
    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class Package(RetrieveAPIView,
              CreateAPIView):
    def get_queryset(self):
        queryset = mdl.Package.objects.filter(session_id=self.request.session.session_key).order_by("id")
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.GetPackage
        elif self.request.method == "POST":
            return serializers.CreatePackage
        else:
            return serializers.Package

    @extend_schema(
        description="Returns package",
        responses={200: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.OBJECT,
                   404: OpenApiTypes.OBJECT}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(session_id=self.request.session.session_key,
                        registration_status=mdl.Package.SUCCESS)

    @extend_schema(
        description="Creates package",
        responses={201: OpenApiTypes.OBJECT,
                   400: OpenApiTypes.OBJECT}
    )
    def post(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.save()
        response = self.create(request, *args, **kwargs)
        response.data = {'id': response.data["id"]}
        return response


class PackageAsync(Package):
    allowed_methods = ["POST"]

    def perform_create(self, serializer):
        tasks.register_package.delay(self.request.data,
                                     self.request.session.session_key)

    @extend_schema(
        description="Creates package asynchronously. Result can be checked in package list",
        responses={204: OpenApiTypes.NONE,
                   400: OpenApiTypes.OBJECT
                   }
    )
    def post(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session.save()
        resp = self.create(request, *args, **kwargs)
        return Response(None, status=status.HTTP_204_NO_CONTENT, headers=resp.headers)


class PackageList(mixins.ListModelMixin,
                  generics.GenericAPIView):
    queryset = mdl.Package.objects.order_by("id")
    serializer_class = serializers.GetPackage
    pagination_class = BasePagination

    class FilterSerializer(drf_serializers.Serializer):
        has_delivery_cost = drf_serializers.BooleanField(required=False, allow_null=True, default=None)
        types = drf_serializers.ListSerializer(required=False, default=[], allow_null=True,
                                               child=drf_serializers.IntegerField())

    def get_queryset(self):
        queryset = mdl.Package.objects.filter(session_id=self.request.session.session_key)
        return queryset

    def filter_queryset(self, queryset):
        serializer = self.FilterSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        filters = serializer.validated_data
        if filters['has_delivery_cost'] is not None:
            queryset = queryset.filter(delivery_cost__isnull=not filters['has_delivery_cost'])
        if filters['types']:
            queryset = queryset.filter(type__in=filters['types'])

        return queryset

    @extend_schema(
        description="Returns user's packages or empty list if there is none",
        parameters=[
            FilterSerializer
        ],
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def check_test_cookie(request):
    if request.method == "POST":
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        else:
            return Response("Please enable cookies and try again.")
    request.session.set_test_cookie()
