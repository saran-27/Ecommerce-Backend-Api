from django.db.models import ImageField
from django.shortcuts import render
from lark.parsers.earley_common import Item
from rest_framework import status
from rest_framework.views import APIView


from .models import *
from rest_framework.response import Response
from .Serializer import *

#api for get all products

class ProductsAPI_And_category(APIView):
    def get(self,request):

        categories =request.GET.get('category')
        products = Product.objects.all()

        if categories:
            products = Product.objects.filter(category__name=categories)

        serializer = ProductSerializer(products, many=True).data
        return Response(serializer)


class ProductsDetail_ById(APIView):
    def get(self,request,id=None):
        if id==None:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True).data
            return Response(serializer)
        else:
            products = Product.objects.get(id=id)
            serializer = ProductSerializer(products).data
            return Response(serializer)

class AddToCart(APIView):
    def post(self, request):
        cart_id = request.data.get("cart_id")
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "product_id required"}, status=400)

        # ✅ Get or create cart
        if cart_id:
            cart, _ = Cart.objects.get_or_create(id=cart_id)
        else:
            cart = Cart.objects.create()

        # ✅ Validate product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        # ✅ Create or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({
            "message": "Added to cart",
            "cart_id": cart.id
        })

# views.py
class CartDetail(APIView):
    def get(self, request, cart_id):
        cart = Cart.objects.get(id=cart_id)
        serializer = Cart_serializer(cart)
        return Response(serializer.data)


class Remove_Item(APIView):
    def post(self, request):
        product_id = request.data.get("product_id")
        cart_id = request.data.get("cart_id")

        try:
            cart = Cart.objects.get(id=cart_id)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            return Response({"message": "Quantity reduced"})
        else:
            item.delete()
            return Response({"message": "Item removed"})



class Checkout(APIView):
    def post(self,request):
        cart_id=request.data.get("cart_id")

        try:
            cart=Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        items=CartItem.objects.filter(cart=cart)

        if not items.exists():
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        total=sum(item.product.price * item.quantity for item in items)

        order=Order.objects.create(
            cart=cart,
            total_amount=total,
        )
        order.save()

        items.delete()

        return Response({"message": "order placed successfully",
                         "Order_id":order.id,
                         "Total_amount":order.total_amount
                         })