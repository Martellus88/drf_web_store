from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import Cart
from .serializers import CartSerializer


class CartAPIView(APIView):

    def get(self, request):
        cart = Cart(request)
        return Response(cart.cart, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request):
        cart = Cart(request)
        serializer_data = CartSerializer(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            cart.add(**serializer_data.data)
            return Response(cart.cart, status=status.HTTP_201_CREATED, content_type='application/json')
        return Response({'message': serializer_data.errors})
