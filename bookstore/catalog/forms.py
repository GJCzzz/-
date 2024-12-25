from django import forms
from .models import Book, OutOfStock, PurchaseOrder, Customer, OrderItem, Order, Supplier


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class OutOfStockForm(forms.ModelForm):
    class Meta:
        model = OutOfStock
        fields = ['book', 'supplier', 'quantity']

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['quantity']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'account_balance', 'credit_rating']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'price']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name']