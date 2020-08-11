from rest_framework import viewsets
from .serializers import SellSerializer
from .models import Sell

class SellView(viewsets.ModelViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer