from django.contrib import admin

# Register your models here.
from .models import Driver, Transaction, Accident


admin.site.site_header = "EthioTrollService Admin"
admin.site.site_title = "EthioTrollService Admin Portal"

admin.site.register(Driver)
admin.site.register(Transaction)
admin.site.register(Accident)
