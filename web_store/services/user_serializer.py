from django.contrib.auth import get_user_model

from rest_framework import serializers
from djoser.serializers import UserSerializer

from services.query import get_user_wallet
from services.utils import get_type_wallet_from_setting

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    wallet_address = serializers.CharField(source='wallet.address')
    balance = serializers.SerializerMethodField('get_balance')

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('wallet_address', 'balance')

    def get_balance(self, user_instance):
        user_wallet = get_user_wallet(user_instance=user_instance)
        key = get_type_wallet_from_setting()(user_wallet.wif_key)
        return f"{key.get_balance('usd')} USD"
