from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bit.exceptions import InsufficientFunds
from bit.network import get_fee

from services.query import get_order_total_cost, change_order_paid
from services.utils import get_user_btc_wallet


class OnlinePayment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        order_total_cost = get_order_total_cost(order_id=request.data.get('order_id'))
        user_btc_wallet = get_user_btc_wallet(request.user)
        user_btc_wallet_balance = user_btc_wallet.get_balance('usd')

        try:
            user_btc_wallet.send([
                (settings.ADMIN_WALLET_ADDRESS, order_total_cost - get_fee(fast=False), 'usd')
            ], message=f"Order №:{request.data.get('order_id')}", fee=get_fee(fast=False))
        except InsufficientFunds:
            return Response(
                {'message': 'insufficient funds to pay for the order', 'balance': f'{user_btc_wallet_balance} USD',
                 'order_total_cost': f"{order_total_cost} USD"}
            )

        change_order_paid(order_id=request.data.get('order_id'))

        return Response({'message': f"order №{request.data.get('order_id')} successfully paid"})
