from django.shortcuts import render, redirect
from .forms import DriverForm, CustomUserCreationForm, AccidentForm
from .models import Accident, Driver
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
import requests, json
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Driver, Transaction
from django.contrib import messages



def register_driver(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        driver_form = DriverForm(request.POST)
       
        print(driver_form.errors)
        if user_form.is_valid() and driver_form.is_valid():
            user = user_form.save()
            driver = driver_form.save(commit=False)
            driver.user = user  # Set the one-to-one link between User and Driver
            driver.save()
            messages.success(request, 'Registration successful. Please login.')  # Display success message
            return redirect('driver-profile')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')  # Display error message
    else:
        user_form = CustomUserCreationForm()
        driver_form = DriverForm()
        driver = Driver.objects.all() 
        for d in driver:
            d.first_name = d.user.first_name
            d.last_name = d.user.last_name
            d.email = d.user.email
    transactions = Transaction.objects.all().order_by('-date')
    accidents = Accident.objects.all() 
    return render(request, 'driver_register.html', {
        'user_form': user_form,
        'driver_form': driver_form,
        'transactions': transactions,
        'drivers': driver,
        'accidents': accidents,
    })



class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


@login_required
def driver_profile(request):
    current_user = request.user
    if request.method == 'POST':
        accident_form = AccidentForm(request.POST)
        if accident_form.is_valid():
            accident = accident_form.save(commit=False)
            accident.user =  current_user 
            accident.save() 
            return redirect('driver-profile')
    accident_form = AccidentForm()
    try:
        driver = Driver.objects.get(user=current_user)
        transactions = Transaction.objects.filter(driver=driver)
        accidents = Accident.objects.filter(user=current_user)
    except Driver.DoesNotExist:
        driver = None
        transactions = None
        accidents = None
    return render(request, 'driver_profile.html', {
        'user': current_user,
        'driver': driver,
        'transactions': transactions,
        'accident_form': accident_form,
        'accidents': accidents,
    })


def check_card(request):
    url = 'http://192.168.8.117/'
    response = requests.get(url)
    data = json.loads(response.text)
    print(data) 
    uid = data.get('UID')
    message = data.get('Message')
    try:
        driver = Driver.objects.get(driver_id=uid)
        if driver:
            if message == 'Access Granted':

                amount = 10 if driver.vehicle_type == 'level_1' else 20 
                if driver.vehicle_type == 'level_3': amount = 30 

                bill = driver.balance - amount
                if bill >= 0:

                    driver.balance -= amount
                    driver.save()
                    
                    new_transaction = Transaction(driver=driver, transfered_amount=amount, date=timezone.now())
                    # new_transaction = Transaction(driver=driver, transfered_amount= amount)
                    new_transaction.save()
                    message = "payment done successfuly"
                else:
                    message = "you don't have enough payment"

            driver.first_name = driver.user.first_name
            driver.last_name = driver.user.last_name
            driver.email = driver.user.email
    except :
        driver = None
        message = "Driver not found."
        

    transactions = Transaction.objects.all().order_by('-date') 


    return render(request,'service.html',
                          {'uid': uid,
                           'message':message,
                           'driver': driver,
                           'transactions': transactions
                           }
                          )

def check_uid(request):
    uid = request.GET.get('uid','')
    
    print(request.GET)
    return JsonResponse({'status':uid})


