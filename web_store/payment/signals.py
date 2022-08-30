from django.dispatch import receiver

from djoser.signals import user_registered

from services.query import create_wallet
from services.utils import get_type_wallet_from_setting


@receiver(user_registered)
def create_wallet_for_user(user, **kwargs):
    key = get_type_wallet_from_setting()()
    create_wallet(user=user, wif_key=key.to_wif(), address=key.address)
