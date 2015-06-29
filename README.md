drf-nested-routing
=================
Extension for Django REST Framework 3 which allows for usage nested resources.

## Setup ##

	pip install drf-nested-routing

## Requirement ##

* Python 2.7+
* Django 1.6+
* Django REST Framework 3

## Example ##

models.py:

	class TestResource(models.Model):
    	name = models.CharField(max_length=255)
    	active = models.BooleanField(default=True)

	class NestedResource(models.Model):
    	resource = models.ForeignKey(TestResource)
    	name = models.CharField(max_length=255)
		
serializers.py:
	
	class TestResourceSerializer(HyperlinkedModelSerializer):
    	class Meta:
        	model = TestResource

	class NestedResourceSerializer(NestedRoutingSerializerMixin, HyperlinkedModelSerializer):
    	class Meta:
        	model = NestedResource
        	
views.py:
	
	class TestResourceViewSet(ModelViewSet):
    	serializer_class = TestResourceSerializer
    	queryset = TestResource.objects.all()

	class NestedResourceViewSet(NestedViewSetMixin, ModelViewSet):
    	serializer_class = NestedResourceSerializer
    	queryset = NestedResource.objects.all()
	
urls.py

	class NestedSimpleRouter(NestedRouterMixin, SimpleRouter):
    	pass

	router = NestedSimpleRouter()
	resourceRoute = router.register(r'test-resources', TestResourceViewSet)
	resourceRoute.register(r'nested', NestedResourceViewSet, ['resource'])

	urlpatterns = patterns(	
    	'',
    	url(r'', include(router.urls)),
	)