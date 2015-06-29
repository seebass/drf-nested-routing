from rest_framework.serializers import HyperlinkedModelSerializer

from drf_nested_routing.serializers import NestedRoutingSerializerMixin
from .models import NestedResource, TestResource


class TestResourceSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = TestResource


class NestedResourceSerializer(NestedRoutingSerializerMixin, HyperlinkedModelSerializer):
    class Meta:
        model = NestedResource
        fields = ('id', 'url', 'name', 'resource')
