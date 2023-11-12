from rest_framework.generics import ListCreateAPIView

from .models import Blob
from .serializer import ExampleBinarySerializer
from .serializer import ExampleURLSafeBinarySerializer


class ExampleView(ListCreateAPIView):
    queryset = Blob.objects.all()
    serializer_class = ExampleBinarySerializer


class ExampleWebSafeView(ListCreateAPIView):
    queryset = Blob.objects.all()
    serializer_class = ExampleURLSafeBinarySerializer
