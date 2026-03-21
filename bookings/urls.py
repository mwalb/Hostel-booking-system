from django.urls import path
from . import views


urlpatterns=[
  path('',views.booking_list,name='booking_list'),
  path('update/<int:id>',views.update_booking,name='update_booking'),
  path('delete/<int:id>',views.delete_booking,name='delete_booking')
]