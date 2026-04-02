from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
  ROLE_CHOICES=(
    ('guest','Guest'),
    ('receptionist','Receptionist'),
    ('admin','Admin'),
  )
  role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='guest')
  def __str__(self):
    return f"{self.username}({self.role})"
  

class Room(models.Model):

    ROOM_TYPE_CHOICES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    )

    number = models.CharField(max_length=10, unique=True)
    price  = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')

    @staticmethod
    def available_rooms():
        return Room.objects.filter(status='available')

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"
class Booking(models.Model):
    guest=models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'guest'})    
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    check_in=models.DateTimeField(auto_now_add=True)
    check_out=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
       return f"Booking{self.id}-{self.guest.username} in Room{self.room.number}"
    

class Invoice(models.Model):
   booking=models.OneToOneField(Booking,on_delete=models.CASCADE)
   amount=models.DecimalField(max_digits=8,decimal_places=2)
   generated_at=models.DateTimeField(auto_now_add=True)
   paid=models.BooleanField(default=False)

   def __str__(self):
      return f"Invoice {self.id} for Booking {self.booking.id}  -${self.amount}"    