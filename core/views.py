from django.shortcuts import render, redirect
from .forms import DriverForm, CustomUserCreationForm, AccidentForm
from .models import Accident, Driver
from django.contrib.auth.views import LoginView


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
    transactions = Transaction.objects.all()
    accidents = Accident.objects.all() 
    return render(request, 'driver_register.html', {
        'user_form': user_form,
        'driver_form': driver_form,
        'transactions': transactions,
        'drivers': driver,
        'accidents': accidents,
    })

from django.contrib.auth.decorators import login_required
from .models import Driver, Transaction
from django.contrib import messages

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


@login_required
def driver_profile(request):
    if request.method == 'POST':
        accident_form = AccidentForm(request.POST)
        if accident_form.is_valid():
            accident = accident_form.save() 
            return redirect('driver-profile')
    current_user = request.user
    accident_form = AccidentForm()
    try:
        driver = Driver.objects.get(user=current_user)
        transactions = Transaction.objects.all()
        accidents = Accident.objects.all()
    except Driver.DoesNotExist:
        driver = None
        transactions = None
        accidents = None
    print(accidents)
    return render(request, 'driver_profile.html', {
        'user': current_user,
        'driver': driver,
        'transactions': transactions,
        'accident_form': accident_form,
        'accidents': accidents,
    })



    


