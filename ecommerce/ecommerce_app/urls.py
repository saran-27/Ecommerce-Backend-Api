from django.urls import path,include
from .views import *


urlpatterns = [
    path('products/',ProductsAPI_And_category.as_view()),
    path('products/<int:id>/', ProductsDetail_ById.as_view()),
    path('cart/add/',AddToCart.as_view()),
    path('cart/<int:cart_id>/',CartDetail.as_view()),
    path('cart/remove/', Remove_Item.as_view()),
    path('cart/checkout/',Checkout.as_view()),
]
