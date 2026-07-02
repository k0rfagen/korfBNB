from rest_framework.views import APIView, Response
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import *
from .serializers import *
from rest_framework import generics
from .permissions import *
from django.core.cache import cache


class ListingAPIView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = (IsHostOrReadOnly, )
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
class ListingAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = (IsOwnerOrReadOnly, )

class BookingAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsGuest()]
        return [IsAuthenticated()]
    def get(self, request, pk):
        cache_key = f'booking_{pk}'
        data = cache.get(cache_key)
        if not data:
            booking = get_object_or_404(Booking, pk=pk)
            serializer = BookingSerializer(booking)
            data = serializer.data
            cache.set(cache_key, data, 3600)
        return Response(data)
    def post(self, request, pk):
        data = request.data.copy()
        data['listing'] = pk 
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserApiView(generics.ListAPIView):
    pass