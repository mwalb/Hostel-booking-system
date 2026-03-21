from django.db import models

class Booking(models.Model):
  customer_name=models.CharField(max_length=100)
  room=models.CharField(max_length=50)
  check_in=models.DateField()
  check_out=models.DateField()
  created_at=models.DateTimeField(auto_now_add=True)
     
  def __str__(self):
    return self.customer_name

