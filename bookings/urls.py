from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    register,
    get_bookings,
    available_rooms,
    occupancy_report,
    check_in,
    check_out,
    booking_history,
   generate_invoice
)
login_view = csrf_exempt(TokenObtainPairView.as_view())
urlpatterns=[
    path('register/',register),
    path('login/',login_view),
    path("bookings/",get_bookings),
    path("booking-history/",booking_history),
    path("rooms/available/",available_rooms),
    path("occupancy-report/",occupancy_report),
    path("check-in/",check_in),
    path("check_out/",check_out),
    path("invoice/<int:booking_id>/",generate_invoice)

]