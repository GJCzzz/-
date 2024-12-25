from django.db import models
from django.contrib.auth.models import User

class Publisher(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    table_of_contents = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    suppliers = models.ManyToManyField(Supplier, related_name='books', blank=True)
    is_series = models.BooleanField(default=False)
    storage_location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

class OutOfStock(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.supplier.name}"

class PurchaseOrder(models.Model):
    out_of_stock = models.ForeignKey(OutOfStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_ordered = models.DateField(auto_now_add=True)
    received = models.BooleanField(default=False)

    def __str__(self):
        return f"Order for {self.out_of_stock.book.title}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit_rating = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=500)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in Order {self.order.id}"

class SupplierBook(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} from {self.supplier.name}"
# Create your models here.
