from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.

choices = (
    (1, 'active'),
    (2, 'trialing'),
    (3, 'past_due'),
    (4, 'unpaid'),
    (5, 'canceled'),
    (6, 'incomplete'),
    (7, 'incomplete_expired')
)

currency_choices = (
    (1, 'USD'),
    (2, 'INR')
)

duration_choices = (
    (1, 'month'),
    (2, '6 month'),
    (3, '9 month'),
    (4, 'year'),
)


class UsersDetails(models.Model):
    cust_id = models.CharField(primary_key=True, max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Product(models.Model):
    pid = models.CharField(primary_key=True, max_length=250)
    pname = models.CharField(max_length=1000)
    description = models.TextField()
    price = models.IntegerField(default=400)
    priceid = models.CharField(max_length=250, default='')
    curreny = models.IntegerField(default=1, choices=currency_choices)
    duration = models.IntegerField(default=0, choices=duration_choices)

    def __str__(self):
        return f'{self.pname} price = {self.price}'


class subscription(models.Model):
    sub_id = models.CharField(primary_key=True, max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_status = models.IntegerField(default=2, choices=choices)
    created_at = models.DateTimeField(default=timezone.now)
    current_start_at = models.DateTimeField(default=timezone.now)
    current_end_At = models.DateTimeField(
        default=timezone.now() + timedelta(30))

    def __str__(self):
        return f'{self.user} subcription will end on {self.current_end_At} current status = {self.sub_status}'

    def givesubscriptiondate(self):
        return f'{ str(self.created_at.strftime("%A"))} , {str(self.created_at.strftime("%d"))} {str(self.created_at.strftime("%B"))} {str(self.created_at.strftime("%Y"))}'

    def givesubscriptionenddate(self):
        return f'{ str(self.current_end_At.strftime("%A"))} , {str(self.current_end_At.strftime("%d"))} {str(self.current_end_At.strftime("%B"))} {str(self.current_end_At.strftime("%Y"))}'

    def givestatus(self):
        for i in choices:
            if i[0] == self.sub_status:
                return i[1]

        return ''
