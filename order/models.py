from django.db import models

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime

class Buyer(models.Model):
    name = models.CharField(max_length=200)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=40)
    address = models.CharField(max_length=40)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_regex = RegexValidator(regex=r'^(?:254|\+254|0)?(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$', message="Phone number must be entered in the format: '+254 or '07'.")  
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)

    creation = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    PRODUCT_STATUS = (
        ('AV', 'AVAILABLE'),
        ('OUT', 'OUT OF STOCK'),
        ('CS', 'COMING SOON')
    )

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=PRODUCT_STATUS)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    creation = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class OrderProduct(models.Model):
    buyer = models.ForeignKey(Buyer, related_name='buyer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1 )
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # tax = models.DecimalField(max_digits=10, decimal_places=4, default=0.00)
    # discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creation = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s' % (self.id)

    class Meta:
        unique_together = ('buyer', 'product')

    def description(self):
    # If items is linked, return item's description
        if self.item:
            return str(self.item.name)
        else:
            return 'Order The Item'

    def total(self):
       ordertotal = ((self.cost * Decimal(self.quantity)).quantize(Decimal('0.01')))
       return str(ordertotal)

def increment_order_id():
    """ Creates Order ID of format ABCD . Change as per neeed."""
    prefix = 'ABCD'
    last_order = Payment.objects.all().order_by('id').last()
    if not last_order:
        return str(prefix) + str(datetime.date.today().year) + str(
            datetime.date.today().month).zfill(2) + str(
            datetime.date.today().day).zfill(2) + '0000'
    order_id = last_order.order_id
    order_id_int = int(order_id[12:16])
    new_order_id_int = order_id_int + 1
    new_order_id = str(prefix) + str(str(datetime.date.today().year)) + str(
        datetime.date.today().month).zfill(2) + str(
            datetime.date.today().day).zfill(2) + str(new_order_id_int).zfill(4)
    return new_order_id


class Payment(models.Model):
    """ Order Model """

    # NOTPAID = 0
    # PAID = 1
    # PARTPAID = 2

    PAYMENT_STATUS = (
        ('NOTPAID', 'Not Paid'),
        ('PARTPAID', 'Partial Paid'),
        ('PAID', 'Paid'),
    )

    order_id = models.CharField(max_length=20, default=increment_order_id, null=True, blank=True, editable=False)
    # payment_status = models.IntegerField(default=NOTPAID, choices=PAYMENT_STATUS, null=False)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, null=True)
    lock = models.BooleanField(default=False, null=False)
    delivercost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', '-id')

    def __str__(self):
        return '%s' % (self.order_id)


    def subtotal(self):
        total = Decimal('0.00').quantize(Decimal('0.01'))
        for item in self.orderitems.all().filter(status=True):
            total = total + Decimal(item.total()).quantize(Decimal('0.01'))

        return str(total)
    
    def total(self):
        total = Decimal('0.00').quantize(Decimal('0.01'))
        for item in self.orderitems.all().filter(status=True):
            total = total + Decimal(item.total()).quantize(Decimal('0.01'))

        return str(total + self.delivercost)

