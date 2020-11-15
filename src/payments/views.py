from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from decimal import Decimal

from payments.models import Payment

from payments.invoice_utils import PayPalClient


def record_payment(request, *args, **kwargs):
    invoice_ids = request.POST.get("invoice_ids", None)
    amount = request.POST.get("amount", None)
    method = request.POST.get("method", None)
    note = request.POST.get("note", "")

    if amount is None or method is None:
        messages.add_message(
            request, messages.ERROR, "Missing payment amount and/or method data",
        )
        return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))

    if invoice_ids is None:
        messages.add_message(
            request, messages.ERROR, "Missing invoice data",
        )
        return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))

    invoice_ids = invoice_ids.split(",")

    if len(invoice_ids) > 1:
        messages.add_message(request, messages.ERROR, "Multiple payments selected!")
        return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))

    payment = Payment.objects.get(id=invoice_ids[0])

    client = PayPalClient()

    response = client.add_payment_to_invoice(
        invoice_id=payment.invoice_number, amount=amount, method=method, note=note
    )

    if response.ok:
        # Update payment object
        payment.amount_paid += Decimal(amount)
        payment.save()

        # Return success response
        messages.add_message(
            request,
            messages.SUCCESS,
            "Succesfully recorded a payment of {} to invoice with id {}".format(
                amount, payment.invoice_number
            ),
        )
        return HttpResponseRedirect(reverse("admin:players_player_changelist"))

    messages.add_message(request, messages.ERROR, response.json())
    return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))
