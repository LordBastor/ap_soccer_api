from django.urls import path

from payments.views import record_payment, RecordAPIPayment

urlpatterns = [
    path("record_payment/", record_payment, name="record-payment"),
    path("record_paypal_payment/", RecordAPIPayment.as_view(), name="record-payment"),
]

app_name = "payments"
