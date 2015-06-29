from django.conf.urls import patterns, url, include
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from drf_nested_routing.routers import NestedRouterMixin
from .views import TestResourceViewSet, NestedResourceViewSet

admin.autodiscover()


class NestedSimpleRouter(NestedRouterMixin, SimpleRouter):
    pass


router = NestedSimpleRouter()
resourceRoute = router.register(r'test-resources', TestResourceViewSet)
resourceRoute.register(r'nested', NestedResourceViewSet, ['resource'])

urlpatterns = patterns(
    '',
    url(r'', include(router.urls)),
)
