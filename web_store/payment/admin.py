from django.contrib import admin

from payment.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass
