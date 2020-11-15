from django.urls import path

from payments.views import record_payment

urlpatterns = [
    path("record_payment/", record_payment, name="record-payment"),
]

app_name = "payments"
