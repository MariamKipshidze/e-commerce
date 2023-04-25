from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store import views

router = DefaultRouter()
router.register('products', views.ProductListingViewSet, basename="product")

urlpatterns = [
    path('', include(router.urls)),
]
