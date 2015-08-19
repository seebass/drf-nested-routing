from django.core.urlresolvers import NoReverseMatch
from rest_framework import views
from rest_framework.reverse import reverse
from rest_framework.response import Response

from drf_nested_routing import add_parent_query_lookups
import drf_nested_routing
from drf_nested_routing.views import NestedViewSetMixin


class NestedRegistryItem(object):
    def __init__(self, router, parent_prefix, parent_item=None):
        self.router = router
        self.parent_prefix = parent_prefix
        self.parent_item = parent_item

    def register(self, prefix, viewset, parent_query_lookups=None, base_name=None):
        if not issubclass(viewset, NestedViewSetMixin):
            raise ValueError("ViewSets of nested routes must subclass NestedViewSetMixin")
        if not base_name:
            base_name = viewset.queryset.model.__name__.lower()
        if parent_query_lookups:
            add_parent_query_lookups(base_name, parent_query_lookups)
        self.router._register(prefix=self.get_prefix(current_prefix=prefix, parent_query_lookups=parent_query_lookups),
                              viewset=viewset, base_name=base_name)
        return NestedRegistryItem(router=self.router, parent_prefix=prefix, parent_item=self)

    def get_prefix(self, current_prefix, parent_query_lookups):
        return '{0}/{1}'.format(self.get_parent_prefix(parent_query_lookups), current_prefix)

    def get_parent_prefix(self, parent_query_lookups):
        prefix = '/'
        current_item = self
        i = len(parent_query_lookups) - 1
        while current_item:
            prefix = '{}/(?P<{}>[^/.]+)/{}'.format(current_item.parent_prefix,
                                                   drf_nested_routing.PARENT_LOOKUP_NAME_PREFIX + parent_query_lookups[i], prefix)
            i -= 1
            current_item = current_item.parent_item
        return prefix.strip('/')


class NestedRouterMixin(object):
    def _register(self, *args, **kwargs):
        return super(NestedRouterMixin, self).register(*args, **kwargs)

    def register(self, *args, **kwargs):
        self._register(*args, **kwargs)
        return NestedRegistryItem(router=self, parent_prefix=self.registry[-1][0])

    def get_api_root_view(self):
        """
        Return a view to use as the API root.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    try:
                        ret[key] = reverse(url_name, request=request, format=format)
                    except NoReverseMatch:
                        pass
                return Response(ret)

        return APIRoot.as_view()
