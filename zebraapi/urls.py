from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecialZebraViewSet

router = DefaultRouter()
router.register(r'specialzebra', SpecialZebraViewSet, basename='specialzebra')

urlpatterns = [
    path('', include(router.urls)),
]