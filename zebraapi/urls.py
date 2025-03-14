from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecialZebraViewSet

router = DefaultRouter()
router.register(r'zebra', SpecialZebraViewSet, basename='zebra')

urlpatterns = [
    path('', include(router.urls)),
]