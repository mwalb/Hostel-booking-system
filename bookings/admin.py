from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Room,Booking,Invoice


@admin.register(CustomUser)
class CustomeruserAdmin(UserAdmin):
  list_display=('username','email','role','is_staff','is_active')
  list_filter=('role','is_staff','is_active')
  search_fields=('username','email')
  fieldsets=UserAdmin.fieldsets+((None,{'fields':('role',)}),)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
  list_display=('number','room_type','status')
  list_filter=('room_type','status')
  search_fields=('number',)  

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
  list_display=('id','guest','room','check_in','check_out','created_at')
  list_filter=('check_in','check_out','room')
  search_fields=('guest__username','room__number')  


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
  list_display=('id','booking','amount','paid','generated_at')
  list_filter=('paid',)
  search_fields=('booking__guest__username',)