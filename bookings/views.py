from django.shortcuts import render ,redirect,get_object_or_404
from  .models import Booking 
from django.contrib import messages


def booking_list(request):
  bookings=Booking.objects.all()
  error=None
  if request.method=="POST":
     
     
        customer_name = request.POST['customer_name']
        room = request.POST['room']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']

     
        if not customer_name or not room or not check_in:
           error="All required fields must be filled"
        elif check_out and check_out < check_in:
           error="check_out must be after check_in"
        else:
            Booking.objects.create(
                  customer_name=customer_name,
                  room=room,
                  check_in=check_in,
                  check_out=check_out
            )
            messages.success(request, "Booking added successfully")     
        return redirect('booking_list')
  
  return render(request,'booking_list.html',{'bookings':bookings,'error':error})

def update_booking(request,id):
   booking=get_object_or_404(Booking,id=id)
   if request.method=="POST":
      booking.customer_name=request.POST['customer_name']
      booking.room=request.POST['room']
      booking.check_in=request.POST['check_in']
      booking.check_out=request.POST['check_out']
      booking.save()
      return redirect('booking_list')
   return render(request,'Update_booking.html',{'booking':booking})
def delete_booking(request,id):
   booking=get_object_or_404(Booking,id=id)


   if request.method=="POST":
      booking.delete()
      return redirect('booking_list')
   
   return render(request,'delete_booking.html',{'booking':booking})



   
