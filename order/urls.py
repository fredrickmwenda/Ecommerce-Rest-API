# from django.conf.urls import url
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import *
from . import views

urlpatterns = [
    path('buyer/register', views.RegisterBuyer),
    path('buyer/viewbuyers', views.ViewAllBuyers),

    path('product/create', views.CreateProduct, name='create product'),

    path('products/available', views.ProductsAvailable, name='Products Available'),
    path('products/outofstock', views.ProductsUnavailable, name='Products Unavailable'),
    path('products/comingsoon', views.ProductsComingsoon, name='Products ComingSoon'),

    path('product/<str:product_name>/', views.ProductDetails, name='Product Details'),

    re_path(r'^buyer/(?P<buyer_id>[0-9]+)/history', views.OrderBuyerHistory, name='Buyer Order History'),


    path('payment/paid', views.PaymentPaid, name='Payments Paid'),
    path('payment/partpaid', views.PaymentPartPaid, name='Payments Partially Paid'),
    path('payment/notpaid', views.PaymentUnpaid, name='Payments Not Paid'),

    re_path(r'^update/(?P<product_id>[0-9]+)', views.ChangeProductStatus, name="Change Product Status"),
    re_path(r'^update/(?P<order_id>[A-Z]+)', views.ChangePaymentStatus, name="Change Payment Status"),

    re_path(r'^ordering/(?P<buyer_id>[0-9]+)/(?P<product_id>[0-9]+)', views.OrderProducts, name='Order Product'),

    
]

urlpatterns = format_suffix_patterns(urlpatterns)