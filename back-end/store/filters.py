from django.contrib.postgres.search import TrigramSimilarity
from django_filters import rest_framework as filters

from store.models import Product


class ProductFilterSet(filters.FilterSet):
    title = filters.CharFilter(label='title', method='filter_title')

    class Meta:
        model = Product
        fields = ('title', )

    @staticmethod
    def filter_title(queryset, _title, value):
        return queryset.annotate(
            similarity=TrigramSimilarity("title", value)
        ).filter(similarity__gt=0.3).order_by("-similarity")
