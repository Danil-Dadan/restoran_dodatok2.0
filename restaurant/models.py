from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def str(self):
        return self.name

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(default=4)

    def str(self):
        return f"Table {self.number} ({self.seats} seats)"

class Reservation(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    guests = models.PositiveIntegerField(default=1)
    datetime = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def str(self):
        return f"Reservation {self.name} at {self.datetime}"

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def str(self):
        return f"Order {self.id} — {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def line_total(self):
        return self.price * self.quantity
