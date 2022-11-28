from rest_framework import viewsets

from .serializers import DetectorSerializer
from .models import Detector


class DetectorViewSet(viewsets.ModelViewSet):
    queryset = Detector.objects.all()
    serializer_class = DetectorSerializer