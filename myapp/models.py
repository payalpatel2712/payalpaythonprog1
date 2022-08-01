from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
	fname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	subject=models.CharField(max_length=100)
	remark=models.CharField(max_length=100)

	def __str__(self):
		return self.fname

class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	address=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	usertype=models.CharField(max_length=100,default="patient")

	def __str__(self):
		return self.fname+" - "+ self.lname

class Doctor_profile(models.Model):
	doctor=models.ForeignKey(User,on_delete=models.CASCADE)
	doctor_degree=models.CharField(max_length=100)
	doctor_speciality=models.CharField(max_length=100) 
	doctor_start_time=models.CharField(max_length=100)
	doctor_end_time=models.CharField(max_length=100)
	doctor_fees=models.PositiveIntegerField()
	doctor_picture=models.ImageField(upload_to="doctor_picture/")

	def __str__(self):
		return self.doctor.fname+" - "+ self.doctor_degree

class Appointment(models.Model):
	
	Patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name="patient")
	doctor=models.ForeignKey(Doctor_profile,on_delete=models.CASCADE)
	Date=models.DateTimeField(default=timezone.now)
	Time=models.CharField(max_length=100)
	Helth_issue=models.TextField()
	status=models.CharField(max_length=100,default="pending")
	prescription=models.TextField(default="not given yet")
	payment_status=models.CharField(max_length=100,default="pending")
	def __str__(self):
		return self.Patient.fname
		
class CancelAppointment(models.Model):
	appointment=models.ForeignKey(Appointment,on_delete=models.CASCADE)
	reason=models.CharField(max_length=100)

	def __str__(self):
		return self.appointment.Patient.fname+"-"+self.appointment.doctor.doctor.fname

class Helthprofile(models.Model):
	patient=models.ForeignKey(User,on_delete=models.CASCADE)
	blood_group=models.CharField(max_length=100)
	weight=models.CharField(max_length=100)
	Diabetes=models.BooleanField(default=False)
	Blood_pressure=models.BooleanField(default=False)

	def __str__(self):
		return self.patient.fname
		pass

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
