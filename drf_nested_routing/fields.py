from django.db.models import Model
from rest_framework.relations import HyperlinkedRelatedField, HyperlinkedIdentityField, reverse, PKOnlyObject
from drf_nested_routing import get_parent_query_lookups_by_view
import drf_nested_routing


class NestedHyperlinkedRelatedField(HyperlinkedRelatedField):
    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        if isinstance(obj, PKOnlyObject):
            obj = self.queryset.get(pk=obj.pk)

        parent_lookups = get_parent_query_lookups_by_view(view_name.split("-")[0])
        lookup_field = getattr(obj, self.lookup_field)
        kwargs = {self.lookup_field: lookup_field}
        if parent_lookups:
            for lookup in parent_lookups:
                parent_lookup = obj
                lookup_path = lookup.split('__')
                if len(lookup_path) > 1:
                    for part in lookup_path[:-1]:
                        parent_lookup = getattr(parent_lookup, part)
                parent_lookup_id = getattr(parent_lookup, lookup_path[-1] + '_id', None)
                kwargs[drf_nested_routing.PARENT_LOOKUP_NAME_PREFIX + lookup] = parent_lookup_id
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class NestedHyperlinkedIdentityField(HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        parent_lookups = get_parent_query_lookups_by_view(view_name.split("-")[0])
        lookup_field = getattr(obj, self.lookup_field, None)
        kwargs = {self.lookup_field: lookup_field}
        if parent_lookups:
            for lookup in parent_lookups:
                lookup_path = lookup.split('__')
                parent_lookup = obj
                for part in lookup_path:
                    parent_lookup = getattr(parent_lookup, part)
                parent_lookup_id = parent_lookup.id if isinstance(parent_lookup, Model) else parent_lookup
                kwargs[drf_nested_routing.PARENT_LOOKUP_NAME_PREFIX + lookup] = parent_lookup_id

        if lookup_field is None:  # Handle unsaved object case
            return None

        return reverse(view_name, kwargs=kwargs, request=request, format=format)
