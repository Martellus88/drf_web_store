from django.urls import path

from payment.views import OnlinePayment

urlpatterns = [
    path('payment', OnlinePayment.as_view())
]
