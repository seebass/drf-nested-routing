from rest_framework.mixins import UpdateModelMixin, CreateModelMixin

import drf_nested_routing


class NestedViewSetMixin(object):
    def get_queryset(self):
        queryset = super(NestedViewSetMixin, self).get_queryset()
        self.__add_related_fetches_to_querySet(queryset)
        return self.__filter_query_set_by_parent_lookups(queryset)

    def __add_related_fetches_to_querySet(self, queryset):
        parent_lookups = drf_nested_routing.get_parent_query_lookups_by_class(queryset.model)
        related = getattr(self, 'select_related', [])
        lookups = parent_lookups + related
        if lookups:
            queryset = queryset.select_related(*lookups)
        prefetches = getattr(self, 'prefetch_related', [])
        for prefetch in prefetches:
            queryset = queryset.prefetch_related(prefetch)

    def __filter_query_set_by_parent_lookups(self, queryset):
        parents_query_dict = self.__get_parents_query_filter()
        if parents_query_dict:
            queryset = queryset.filter(**parents_query_dict)
        return queryset

    def __get_parents_query_filter(self):
        result = {}
        for kwarg_name in self.kwargs:
            if kwarg_name.startswith(drf_nested_routing.PARENT_LOOKUP_NAME_PREFIX):
                query_lookup = kwarg_name.replace(drf_nested_routing.PARENT_LOOKUP_NAME_PREFIX, '', 1)
                query_value = self.kwargs.get(kwarg_name)
                result[query_lookup] = query_value
        # return parent query filter if not wildcard *
        return {k: v for k, v in result.items() if v != '*'}


class AddParentToRequestDataMixin:
    def _add_parent_to_request_data(self, request, parent_key, parent_id):
        raise NotImplementedError()

    def _add_parent_to_request_data_through_lookup(self, request, **kwargs):
        lookup_prefix = drf_nested_routing.PARENT_LOOKUP_NAME_PREFIX
        for kwarg in kwargs:
            if not kwarg.startswith(lookup_prefix):
                continue

            parent_lookup_key = kwarg
            parent_lookup_key_without_prefix = parent_lookup_key[len(lookup_prefix):]
            if '__' in parent_lookup_key_without_prefix:
                continue  # only the direct parent is added to data

            self._add_parent_to_request_data(request, parent_lookup_key_without_prefix, kwargs[parent_lookup_key])


class CreateNestedModelMixin(AddParentToRequestDataMixin, CreateModelMixin):
    def create(self, request, *args, **kwargs):
        self._add_parent_to_request_data_through_lookup(request, **kwargs)
        return super(CreateNestedModelMixin, self).create(request, *args, **kwargs)


class UpdateNestedModelMixin(AddParentToRequestDataMixin, UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            self._add_parent_to_request_data_through_lookup(request, **kwargs)
        return super(UpdateNestedModelMixin, self).update(request, *args, **kwargs)
