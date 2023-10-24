from rest_framework.decorators import api_view, renderer_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size_query_param = 'size'


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def index(request):

    return Response({}, template_name="index.html")
