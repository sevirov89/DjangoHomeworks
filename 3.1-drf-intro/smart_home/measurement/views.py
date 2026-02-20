#
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, RetrieveAPIView

from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer




class SensorListView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer



class MeasurementUpdateView(RetrieveUpdateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class SensorCreateAPIView(CreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class SensorDetailView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer
