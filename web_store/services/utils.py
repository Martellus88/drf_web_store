from django.conf import settings
from django.utils.module_loading import import_string


def get_type_wallet_from_setting():
    path_to_type_wallet = f"bit.{getattr(settings, 'TYPE_WALLET')}"
    type_wallet = import_string(path_to_type_wallet)
    return type_wallet
