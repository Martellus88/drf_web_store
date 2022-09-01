from django.conf import settings
from django.utils.module_loading import import_string

from services.query import get_user_wallet_wif_key


def get_type_wallet_from_setting():
    path_to_type_wallet = f"bit.{getattr(settings, 'TYPE_WALLET')}"
    type_wallet = import_string(path_to_type_wallet)
    return type_wallet

def get_user_btc_wallet(user):
    user_wif_key = get_user_wallet_wif_key(user=user)
    user_btc_wallet = get_type_wallet_from_setting()(user_wif_key)
    return user_btc_wallet