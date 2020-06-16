from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class  BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'status')

class ProductStatusSerializer(serializers.ModelSerializer):

    def update(self, obj, data):
        obj.status = data.get("status", obj.status)
        obj.save()
        return obj

    class Meta:
        model = Product
        fields = ('name',  'status')


class  OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        exclude = ('buyer', 'product')

        # fields = '__all__'

class  PaymentTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('order_id', 'total')

class PaymentStatusSerializer(serializers.ModelSerializer):
    def update(self, obj, data):
        obj.status = data.get("status", obj.status)
        obj.save()
        return obj
    class Meta:
        model = Payment
        fields = ('order_id', 'status')