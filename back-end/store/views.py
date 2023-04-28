from rest_framework import mixins
from django_filters import rest_framework
from rest_framework.viewsets import GenericViewSet

from e_commerce.serializers import ProductListingSerializer
from e_commerce.utils import StandardResultsSetPagination
from store.models import Product


class ProductListingViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductListingSerializer
    filter_backends = [rest_framework.DjangoFilterBackend]
