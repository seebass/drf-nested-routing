from drf_nested_routing.fields import NestedHyperlinkedIdentityField
from drf_nested_routing.fields import NestedHyperlinkedRelatedField


class NestedRoutingSerializerMixin:
    serializer_related_field = NestedHyperlinkedRelatedField
    serializer_url_field = NestedHyperlinkedIdentityField
