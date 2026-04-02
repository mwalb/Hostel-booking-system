from rest_framework import serializers
from .models import CustomUser, Room, Booking, Invoice


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'number', 'room_type', 'status','price']


class BookingSerializer(serializers.ModelSerializer):

    guest = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'guest', 'room', 'check_in', 'check_out', 'created_at']


class BookingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['guest', 'room']


class InvoiceSerializer(serializers.ModelSerializer):

    booking = BookingSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"

class BookingHistorySerializer(serializers.ModelSerializer):

    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out']