from rest_framework import mixins

from e_commerce.serializers import ProductListingSerializer
from e_commerce.utils import StandardResultsSetPagination
from store.models import Product


class ProductListingViewSet(mixins.ListModelMixin):
    queryset = Product.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = ProductListingSerializer
