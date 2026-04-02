from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Booking, Room,Invoice

from .serializers import(
    BookingSerializer,
    BookingHistorySerializer,
    BookingCreateSerializer,
    RoomSerializer,
    InvoiceSerializer,
)

User = get_user_model()


# REGISTER USER
@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = User.objects.create_user(
        username=username,
        password=password
    )

    return Response({"message": "User registered successfully"})


# GET ALL BOOKINGS
@api_view(['GET'])
def get_bookings(request):

    bookings = Booking.objects.all()

    serializer=BookingSerializer(bookings,many=True)
    return Response(serializer.data)


# AVAILABLE ROOMS
@api_view(['GET'])
def available_rooms(request):

    rooms = Room.objects.filter(status='available')
    serializer=RoomSerializer(rooms,many=True)
    return Response(serializer.data)
    
# CHECK IN
@api_view(['POST'])
def check_in(request):

    booking_id = request.data.get("booking_id")

    try:
        booking = Booking.objects.get(id=booking_id)

    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"})

    room = booking.room

    if room.status != "available":
        return Response({"error": "Room not available"})

    room.status = "occupied"
    room.save()

    booking.check_in = timezone.now()
    booking.save()

    return Response({
        "message": "Guest checked in successfully",
        "room": room.number
    })


# CHECK OUT
@api_view(['POST'])
def check_out(request):

    booking_id = request.data.get("booking_id")

    try:
        booking = Booking.objects.get(id=booking_id)

    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"})

    booking.check_out = timezone.now()
    booking.save()

    room = booking.room
    room.status = "available"
    room.save()

    return Response({
        "message": "Guest checked out successfully"
    })


# GENERATE INVOICE
@api_view(['GET'])
def generate_invoice(request, booking_id):

    try:
        booking = Booking.objects.get(id=booking_id)

    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"})

    if not booking.check_out:
        return Response({"error": "Guest has not checked out yet"})

    nights = (booking.check_out - booking.check_in).days
    total = nights * booking.room.price

    invoice = Invoice.objects.create(
        booking=booking,
        amount=total
    )

    serializer = InvoiceSerializer(invoice)

    return Response(serializer.data)

# OCCUPANCY REPORT (ADMIN DASHBOARD)
@api_view(['GET'])
def occupancy_report(request):

    total_rooms = Room.objects.count()
    occupied = Room.objects.filter(status="occupied").count()

    occupancy_rate = 0

    if total_rooms > 0:
        occupancy_rate = (occupied / total_rooms) * 100

    return Response({
        "total_rooms": total_rooms,
        "occupied_rooms": occupied,
        "available_rooms": total_rooms - occupied,
        "occupancy_rate": occupancy_rate
    })


# BOOKING HISTORY (FOR LOGGED USER)
@api_view(['GET'])
def booking_history(request):

    bookings = Booking.objects.filter(
        guest=request.user
    ).order_by("-created_at")

    serializer=BookingHistorySerializer(bookings,many=True)
    return Response(serializer.data)