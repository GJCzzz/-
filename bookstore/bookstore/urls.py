"""
URL configuration for bookstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from catalog import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/update/', views.book_update, name='book_update'),
    path('books/<int:book_id>/delete/', views.book_delete, name='book_delete'),

    path('out_of_stock/', views.out_of_stock_list, name='out_of_stock_list'),
    path('out_of_stock/create/', views.out_of_stock_create, name='out_of_stock_create'),
    path('purchase_orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase_orders/create/<int:out_of_stock_id>/', views.purchase_order_create, name='purchase_order_create'),
    path('purchase_orders/<int:purchase_order_id>/receive/', views.purchase_order_receive, name='purchase_order_receive'),

    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:customer_id>/delete/', views.customer_delete, name='customer_delete'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/items/create/', views.order_item_create, name='order_item_create'),
    path('orders/<int:order_id>/ship/', views.order_ship, name='order_ship'),

    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:supplier_id>/update/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:supplier_id>/delete/', views.supplier_delete, name='supplier_delete'),

    path('search/', views.search, name='search'),
]