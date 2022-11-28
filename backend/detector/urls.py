from django.urls import path, include
from rest_framework import routers

from .views import DetectorViewSet

router = routers.DefaultRouter()
router.register(r'detector', DetectorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]