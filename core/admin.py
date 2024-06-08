from django.contrib import admin

# Register your models here.
from .models import Driver, Transaction, Accident

# Dynamically register all models in the app
admin.site.register(Driver)
admin.site.register(Transaction)
admin.site.register(Accident)
