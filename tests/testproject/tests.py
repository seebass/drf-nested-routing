from django.test import TestCase
from rest_framework.reverse import reverse

import drf_nested_routing
from .models import NestedResource, TestResource


class NestedRoutingTest(TestCase):
    TESTSERVER_URL = "http://testserver"

    def setUp(self):
        self.resource = TestResource.objects.create(name="Resource")
        self.nested_resource = NestedResource.objects.create(name="Nested-Resource", resource=self.resource)

    def testGetNestedResource(self):
        resp = self.client.get("/test-resources/{}/nested/".format(self.resource.id))
        self.assertEqual(200, resp.status_code, resp.content)
        self.assertEqual(1, len(resp.data))
        nested_resource_data = resp.data[0]
        self.assertEqual(4, len(nested_resource_data))
        self.assertEqual(self.nested_resource.id, nested_resource_data['id'])
        self.assertEqual(self.nested_resource.name, nested_resource_data['name'])
        kwargs = {"pk": self.nested_resource.id, drf_nested_routing.PARENT_LOOKUP_NAME_PREFIX + "resource": self.resource.id}
        self.assertEqual(self.TESTSERVER_URL + reverse("nestedresource-detail", kwargs=kwargs), nested_resource_data['url'])
        self.assertEqual(self.TESTSERVER_URL + reverse("testresource-detail", kwargs={"pk": self.resource.id}),
                         nested_resource_data['resource'])
