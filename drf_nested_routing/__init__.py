PARENT_LOOKUP_NAME_PREFIX="parent_lookup_"

__parent_query_lookups_by_view = dict()


def add_parent_query_lookups(viewName, parent_query_lookups):
    __parent_query_lookups_by_view[viewName] = parent_query_lookups


def get_parent_query_lookups_by_view(view_name):
    return __parent_query_lookups_by_view.get(view_name, [])


def get_parent_query_lookups_by_class(clazz):
    return get_parent_query_lookups_by_view(clazz.__name__.lower())
