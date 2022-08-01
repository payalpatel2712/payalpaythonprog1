from django.shortcuts import render,redirect

from .models import Contact,User,Doctor_profile,Appointment,CancelAppointment,Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
import random
from django.http import JsonResponse
# Create your views here.
def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about-us.html')

def gallery(request):
	return render(request,'gallery.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email allready axeist plz try another email"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password']
			
					)
				msg=" User signup successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="password & cpassword doesnot matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')


def login(request):
	if  request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],password=request.POST['password'])

			if user.usertype=="patient":
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'index.html')
			else:
				
				request.session['email']=user.email
				request.session['fname']=user.fname
				try:
					doctor_profile=Doctor_profile.objects.get(doctor=user)
					request.session['doctor_picture']=doctor_profile.doctor_picture.url
				except:
					pass
				return redirect('doctor_index')

		except Exception as e:
			print(e)
			msg="email or password doesnot match"
			return render(request,'login.html',{'msg':msg})
	else:

	
		return render(request,'login.html')	
		
def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if request.POST['old_password']==user.password:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="new_password & cnew_password doesnotmatch"
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg="old_password doesnotmatch"
			return render(request,'change_password.html',{'msg':msg})
	else:
		return render(request,'change_password.html')



def forgotpassword(request):

		if request.method=="POST":  
			try:
				user=User.objects.get(email=request.POST['email'])
		
				subject = 'otp for forgotpassword'
				otp=random.randint(1000,9999)
				message ='hello'+user.fname+', your otp for forgotpassword is '+str(otp)
				email_from = settings.EMAIL_HOST_USER
				recipient_list = [user.email, ]
				send_mail( subject, message, email_from, recipient_list )
				return render(request,'otp.html',{'otp':otp,'email':user.email})
			except Exception as e:
				print(e)
				msg="Email not Registered"

				return render(request,'forgotpassword.html',{'msg':msg})
		else:
			return render(request,'forgotpassword.html')


def otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']

	if otp==uotp:
		return render(request,'newpassword.html',{'email':email})
	else:
		msg="invalid otp"
		return render(request,'otp.html',{'otp':otp,'email':email,'msg':msg})


def newpassword(request):
	email=request.POST['email']
	newpassword=request.POST['newpassword']
	cnewpassword=request.POST['cnewpassword']
	if newpassword==cnewpassword:
		user=User.objects.get(email=email)
		user.password=newpassword
		user.save()
		msg="password change successfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="New password & conformpassword doesnotmatch"	
		return render(request,'newpassword.html',{'email':email,'msg':msg})



def contact(request):
	if request.method=="POST":
		Contact.objects.create(
				fname=request.POST['fname'],
				email=request.POST['email'],
				subject=request.POST['subject'],
				remark=request.POST['remark']
			)
		msg="Contact saved successfully"
		contacts=Contact.objects.all().order_by("-id")[:4]
		return render(request,'contact.html',{'msg':msg,'contacts':contacts})
	else:
		contacts=Contact.objects.all().order_by("-id")[:4]
		return render(request,'contact.html',{'contacts':contacts})	


def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def doctor_index(request):
	return render(request,'doctor_index.html')


def doctor_header(request):
	return render(request,'doctor_header.html')


def doctor_profile(request):
	doctor_profile=Doctor_profile()
	doctor=User.objects.get(email=request.session['email'])
	try:
		doctor_profile=Doctor_profile.objects.get(doctor=doctor)
	except:
		pass
	if request.method=="POST":

		if doctor_profile.doctor_speciality:
			doctor_profile.doctor=doctor
			doctor_profile.doctor_degree=request.POST['doctor_degree']
			doctor_profile.doctor_speciality=request.POST['doctor_speciality']
			doctor_profile.doctor_start_time=request.POST['doctor_start_time']
			doctor_profile.doctor_end_time=request.POST['doctor_end_time']
			doctor_profile.doctor_fees=request.POST['doctor_fees']
			try:
				doctor_profile.doctor_picture=request.FILES['doctor_picture']
			except:
				pass
			doctor_profile.save()
			msg="Doctor profile updated successfully"
			return render(request, 'doctor_profile.html',{'msg':msg,'doctor_profile':doctor_profile})
		else:
			
			doctor_profile=Doctor_profile.objects.create(
				doctor=doctor,
				doctor_degree=request.POST['doctor_degree'],
				doctor_speciality=request.POST['doctor_speciality'],
				doctor_start_time=request.POST['doctor_start_time'],
				doctor_end_time=request.POST['doctor_end_time'],
				doctor_fees=request.POST['doctor_fees'],
				doctor_picture=request.FILES['doctor_picture'] 
				)
			doctor_profile.save()
			msg="Doctor profile created successfully"
			return render(request,'doctor_profile.html',{'msg':msg,'doctor_profile':doctor_profile})			
	else:
		msg="Doctor profile not updated"
		return render(request, 'doctor_profile.html',{'doctor_profile':doctor_profile,'msg':msg})
	
def doctors(request):
	doctors=Doctor_profile.objects.all()
	for i in doctors:
		print(i.id)
	return render(request,'doctors.html',{'doctors':doctors})

def doctor_detail(request,pk):
	doctor=Doctor_profile.objects.get(pk=pk)
	return render(request,'doctor_detail.html',{'doctor':doctor})

def doctorappointment(request):
	doctor=User.objects.get(email=request.session['email'])
	doctor_profile=Doctor_profile.objects.get(doctor=doctor)
	doctorappointment=Appointment.objects.filter(doctor=doctor_profile)
	return render(request,'doctorappointment.html',{'doctorappointment':doctorappointment})



def doctor_aprove_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	appointment.status="approved"
	appointment.save()
	return redirect('doctorappointment')

def doctor_complete_appointment(request,pk):
  
	appointment=Appointment.objects.get(pk=pk)
	if request.method=="POST":
		appointment.prescription=request.POST['prescription']
		appointment.status="completed"
		appointment.save()
		return redirect('doctorappointment')
	else:
		return render(request,'doctor_complete_appointment.html',{'appointment':appointment}) 
		appointment.status="completed"
		appointment.save() 

#def prescription(request):
#	appointment=Appointment.objects.get(appointment=appointment)		
#	if request.method=="POST":
#		appointment.prescription=request.POST['prescription']
#		prescription.save()
#		return render(request,'prescription.html',{'appointment':appointment})
#	else:
		return render(request,'doctor_complete_appointment.html.html',{'appointment':appointment})


def doctor_cencel_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	appointment.status="cencelled by doctor"
	appointment.save()
	return redirect('doctorappointment')

def bookappointment(request,pk):
	doctor= Doctor_profile.objects.get(pk=pk)
	Patient=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		appointment=Appointment.objects.create(
				Patient=Patient,
				doctor=doctor,
				Date=request.POST['date'],
				Time=request.POST['time'],
				Helth_issue=request.POST['health_issue']

			)
		msg="Appointment Booked Successfully"
		appointments1=Appointment.objects.filter(Patient=Patient,status="pending")
		request.session['appointment_count']=len(appointments1)
		appointments=Appointment.objects.filter(Patient=Patient)

		#return render(request,'myappointment.html',{'msg':msg,'appointments':appointments})
		return render(request,'payment.html',{'appointment':appointment})
	else:
		msg="Appointment not booked"
		return render(request,'bookappointment.html',{'doctor':doctor,'Patient':Patient,'msg':msg})

def myappointment(request):
	Patient=User.objects.get(email=request.session['email'])
	appointments=Appointment.objects.filter(Patient=Patient)
	appointments1=Appointment.objects.filter(Patient=Patient,status="pending")
	request.session['appointment_count']=len(appointments1)
	return render(request,'myappointment.html',{'appointments':appointments})

def patient_cancel_appointment(request,pk):
	appointment=Appointment.objects.get(pk=pk)
	if request.method=="POST":
		CancelAppointment.objects.create(
			appointment=appointment,
			reason=request.POST['reason']
		)
		appointment.status="cancelled by patient"
		appointment.save()
		return redirect('myappointment')
	else:
		return render(request,'patient_cancel_appointment.html',{'appointment':appointment}) 
		

def helth_profile(request):
	helth_profile=Helthprofile()
	Patient=User.objects.get(email=request.session['email'])
	try:
		helth_profile=Helthprofile.objects.get(Patient=Patient)
	except:
		pass

	if request.method=="POST":
	
		diabetes=request.POST['diabetes']
		if diabetes=="YES":
			flag1=True
		else:
			flag1=False

		Blood_pressure=request.POST['Blood_pressure']
		if Blood_pressure=="YES":
			flag2=True
		else:
			flag2=False

		helth_profile=Helthprofile.objects.create(
			patient=patient,
			blood_group=request.POST['blood_group'],
			weight=request.POST['weight'],
			Diabetes=flag1,
			Blood_pressure=flag2
			)
		msg=" Helth profile updated successfully"
		return render(request,'helth_profile.html',{'msg':msg,'helth_profile':helth_profile})
	else:

		return render(request,'helth_profile.html',{'helth_profile':helth_profile})

##########paytem integration  function ###########################


def initiate_payment(request):
	user=User.objects.get(email=request.session['email'])
	pk=int(request.POST['pk'])
	try:
		amount = int(request.POST['amount'])
	except:
		return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

	transaction = Transaction.objects.create(made_by=user,amount=amount)
	transaction.save()
	merchant_key = settings.PAYTM_SECRET_KEY
	params = (
    	('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(user.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

	paytm_params = dict(params)
	checksum = generate_checksum(paytm_params, merchant_key)

	transaction.checksum = checksum
	transaction.save()

	paytm_params['CHECKSUMHASH'] = checksum
	appointment=Appointment.objects.get(pk=pk)
	appointment.payment_status="paid"
	appointment.save()
	print('SENT: ', checksum)
	return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

## ajax function ###

def validate_email(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

 
 
def validate_mobile(request):
	mobile=request.GET.get('mobile')
	data={
		'is_taken':User.objects.filter(mobile__iexact=mobile).exists()
	}
	return JsonResponse(data)

 
def validate_date(request):
	date=request.GET.get('date')
	data={
		'is_taken':Appointment.objects.filter(Date__iexact=date).exists()
	}
	return JsonResponse(data)

 
def validate_time(request):
	time=request.GET.get('time')
	data={
		'is_taken':Appointment.objects.filter(Time__iexact=time).exists()
	}
	return JsonResponse(data)

 
