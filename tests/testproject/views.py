from rest_framework.viewsets import ModelViewSet

from drf_nested_routing.views import NestedViewSetMixin
from .models import NestedResource, TestResource
from .serializers import TestResourceSerializer, NestedResourceSerializer


class TestResourceViewSet(ModelViewSet):
    serializer_class = TestResourceSerializer
    queryset = TestResource.objects.all()


class NestedResourceViewSet(NestedViewSetMixin, ModelViewSet):
    serializer_class = NestedResourceSerializer
    queryset = NestedResource.objects.all()
