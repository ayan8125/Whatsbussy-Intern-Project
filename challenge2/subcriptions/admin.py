from django.contrib import admin
from .models import UsersDetails, Product, subscription
# Register your models here.

admin.site.register(UsersDetails)
admin.site.register(Product)
admin.site.register(subscription)
