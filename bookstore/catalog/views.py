from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Author, Publisher, Supplier
from .forms import BookForm


def book_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'catalog/book_detail.html', {'book': book})


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'catalog/book_form.html', {'form': form})


@login_required
def book_update(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'catalog/book_form.html', {'form': form})


@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'catalog/book_confirm_delete.html', {'book': book})


from django.shortcuts import render
from .models import OutOfStock, PurchaseOrder
from .forms import OutOfStockForm, PurchaseOrderForm

@login_required
def out_of_stock_list(request):
    out_of_stocks = OutOfStock.objects.all()
    return render(request, 'catalog/out_of_stock_list.html', {'out_of_stocks': out_of_stocks})

@login_required
def out_of_stock_create(request):
    if request.method == 'POST':
        form = OutOfStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('out_of_stock_list')
    else:
        form = OutOfStockForm()
    return render(request, 'catalog/out_of_stock_form.html', {'form': form})

@login_required
def purchase_order_list(request):
    purchase_orders = PurchaseOrder.objects.all()
    return render(request, 'catalog/purchase_order_list.html', {'purchase_orders': purchase_orders})

@login_required
def purchase_order_create(request, out_of_stock_id):
    out_of_stock = get_object_or_404(OutOfStock, pk=out_of_stock_id)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            purchase_order = form.save(commit=False)
            purchase_order.out_of_stock = out_of_stock
            purchase_order.save()
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()
    return render(request, 'catalog/purchase_order_form.html', {'form': form, 'out_of_stock': out_of_stock})

@login_required
def purchase_order_receive(request, purchase_order_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=purchase_order_id)
    if request.method == 'POST':
        purchase_order.received = True
        purchase_order.save()
        # 增加库存
        book = purchase_order.out_of_stock.book
        book.stock += purchase_order.quantity
        book.save()
        # 删除缺书记录
        purchase_order.out_of_stock.delete()
        return redirect('purchase_order_list')
    return render(request, 'catalog/purchase_order_receive.html', {'purchase_order': purchase_order})
# Create your views here.
from .models import Customer
from .forms import CustomerForm

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'catalog/customer_list.html', {'customers': customers})

@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'catalog/customer_detail.html', {'customer': customer})

@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'catalog/customer_form.html', {'form': form})

@login_required
def customer_update(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'catalog/customer_form.html', {'form': form})

@login_required
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'catalog/customer_confirm_delete.html', {'customer': customer})

from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'catalog/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'catalog/order_detail.html', {'order': order})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer
            order.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'catalog/order_form.html', {'form': form})

@login_required
def order_item_create(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderItemForm()
    return render(request, 'catalog/order_item_form.html', {'form': form, 'order': order})

@login_required
def order_ship(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.shipped = True
        order.save()
        # 扣减客户账户余额
        customer = order.customer
        customer.account_balance -= order.total_amount
        customer.save()
        return redirect('order_list')
    return render(request, 'catalog/order_ship.html', {'order': order})

from .models import Supplier
from .forms import SupplierForm

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'catalog/supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    return render(request, 'catalog/supplier_detail.html', {'supplier': supplier})

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'catalog/supplier_form.html', {'form': form})

@login_required
def supplier_update(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_detail', supplier_id=supplier.id)
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'catalog/supplier_form.html', {'form': form})

@login_required
def supplier_delete(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'catalog/supplier_confirm_delete.html', {'supplier': supplier})

def search(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(authors__name__icontains=query)
        customers = Customer.objects.filter(name__icontains=query)
    else:
        books = Book.objects.none()
        customers = Customer.objects.none()
    return render(request, 'catalog/search_results.html', {'books': books, 'customers': customers})