from django.contrib import admin
from .models import Contact,User,Doctor_profile,Appointment, Helthprofile,CancelAppointment, Transaction

# Register your models here.
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(Doctor_profile)
admin.site.register(Appointment)
admin.site.register(Helthprofile)
admin.site.register(CancelAppointment)
admin.site.register(Transaction)