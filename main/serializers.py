from rest_framework import serializers
from .models import *
from django.db import transaction

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BNBUser
#         field = '__all__'
#         read_only_field = ['']

class ListingSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price_per_night', 'location', 'rooms_count', 'owner', 'date_published', 'id']
        read_only_fields = ['date_published', 'owner', 'id']
        
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Booking
        fields = ['id', 'user', 'listing', 'start_date', 'end_date', 'status']
    def validate(self, attrs):
        Listing = attrs['listing']
        start_date = attrs['start_date']
        end_date = attrs['end_date']
        if start_date >= end_date:
            raise serializers.ValidationError('дата заезда должна быть раньше чем дата выезда')
        overlapping_bookings = Booking.objects.filter(
            listing=Listing,
            status__in=['pending', 'confirmed'],
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)
        if overlapping_bookings.exists():
            raise serializers.ValidationError('это жилье уже забронировано на выбранные даты')        
        return attrs
    def create(self, validated_data):
        with transaction.atomic():
            listing = validated_data['listing']
            listing.save()
            return super().create(validated_data)
            