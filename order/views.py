from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *

# Register a new Buyer 

# class RegisterBuyer(APIView):

#     def post(self, request):
#         serializer = UserSerializer(data = request.data)     
#         if serializer.is_valid():
#             data = serializer.data
#             try:
#                 user = User.objects.create_user(username=data['username'], password=['password'])
#                 user.save()
#             except:
#                 return Response({"error": "Username already exists"})
#             buyer = Buyer.objects.create(name=data['username'], user=user)
#             buyer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"error": "Invalid Params or username may already exist"})
@api_view(['POST'])
def RegisterBuyer(request):
    if request.method == 'POST':
        serializer = BuyerSerializer(data=request.data)
        if serializer is valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View a list of buyers on the platform
@api_view(['GET'])
def ViewAllBuyers(request):
    if request.method == 'GET':
        buyers = Buyer.objects.all()
        serializer = BuyerSerializer(buyers, context={'request': request}, many=True)
        return Response(serializer.data)

# LIst all products or create a new product
@api_view(['GET', 'POST'])
def CreateProduct(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer is valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product, context={'request': request}, many=True)
        return Response(serializer.data)
    

""" 
PRODUCTS AVAILABILITY API
"""
# api url order/products/available
@api_view(['GET'])
def ProductsAvailable(request):
    if request.method == 'GET':
        products = Product.objects.filter(status='AV')
        serializer = ProductStatusSerializer(products, many=True)
        return Response(serializer.data)

# api url order/products/outofstock
@api_view(['GET'])
def ProductsUnavailable(request):
    if request.method == 'GET':
        products = Product.objects.filter(status='OUT')
        serializer = ProductStatusSerializer(products, many=True)
        return Response(serializer.data)

# api url order/products/comingsoon
@api_view(['GET'])
def ProductsComingsoon(request):
    if request.method == 'GET':
        products = Product.objects.filter(status='CS')
        serializer = ProductStatusSerializer(products, many=True)
        return Response(serializer.data)


"""
PRODUCT DETAILS API
"""
#api url order/product/details
@api_view(['GET'])
def ProductDetails(request, product_name):
    if request.method == 'GET':
        try:
            product = Product.objects.get(name=product_name)
        except:
            return Response({'Product with name {} is not available'.format(product_name)})
        serializer = ProductSerializer(product)
        return Response(serializer.data)


"""
   A BUYER ORDER HISTORY API
"""
#api url order/buyer/buyer_id/history
@api_view(['GET'])
def OrderBuyerHistory(request, buyer_id):
    if request.method == 'GET':
        try:
            buyer = Buyer.objects.get(id=buyer_id)
        except:
            return Response({'Buyer with ID {} is not available'.format(buyer_id)})
        orders = OrderProduct.objects.filter(buyer=buyer)
        serializer = OrderProductSerializer(orders, many=True)
        return Response(serializer.data)


"""
    ORDER  PRODUCTS API
"""
#URL: order/ordering/buyer_id/product_id
#POST: Params [source, destination, fare]
@api_view(['POST'])
def OrderProducts(request, buyer_id, product_id):
    try:
        buyer = Buyer.objects.get(id=buyer_id)
    except:
        return Response({"error": "Buyer with this ID {} does not exist".format(buyer_id)})
    try:
        product = Product.objects.get(id=product_id)
    except:
        return Response({"error": "Driver with this ID {} does not exist".format(product_id)})
    
    # Lets filter Available Products
    if product.status == "AV":   
        product.save()
        order = OrderProduct.objects.create(buyer=buyer, product=product)
        serializer = OrderProductSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid params"})
    elif product.status == "OUT":
        return Response({"error": "Product with {} is out of stock".format(product_id)})  
    elif product.status == "CS":
        return Response({"error": "Product with {} is not available but is coming soon".format(product_id)})
  


"""
Payment STATUS API
"""
#api url order/paymenttatus/paid
@api_view(['GET'])
def PaymentPaid(request):
    if request.method == 'GET':
        payments = Payment.objects.filter(status='PAID')
        serializer = PaymentStatusSerializer(payments, many=True)
        return Response(serializer.data)


#api url order/paymentstatus/notpaid
@api_view(['GET'])
def PaymentUnpaid(request):
    if request.method == 'GET':
        orderstatus = Payment.objects.filter(status='NOTPAID')
        serializer = PaymentStatusSerializer(orderstatus, many=True)
        return Response(serializer.data)

#api url order/paymentstatus/partiallypaid
@api_view(['GET'])
def PaymentPartPaid(request):
    if request.method == 'GET':
        orderstatus = Payment.objects.filter(status='PARTPAID')
        serializer = PaymentStatusSerializer(orderstatus, many=True)
        return Response(serializer.data)


"""
                  STATUS
"""

"""
Change Product status
"""
 # URL: /orders/update/<product_id>
# POST Params: [status]
# status choices: ['AV', 'BK', 'OFF]
@api_view(['POST'])
def ChangeProductStatus(request, product_id):
    if request.method == 'POST':
        try:
            n = Product.objects.get(id=product_id)
        except:
            return Response({"error": "Product with ID {} does not exist".format(product_id)})
        serializer = ProductStatusSerializer(n, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid params"})

"""
Change Payment status
"""
 # URL: /orders/update/<order_id>
# POST Params: [status]
# status choices: ['AV', 'BK', 'OFF]
@api_view(['POST'])
def ChangePaymentStatus(request, order_id):
    if request.method == 'POST':
        try:
            n = ORDER.objects.get(id=order_id)
        except:
            return Response({"error": "Order with ID {} does not exist".format(order_id)})
        serializer = OrderStatusSerializer(n, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Invalid params"})