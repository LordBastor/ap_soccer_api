from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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


class RecordAPIPayment(APIView):
    def post(self, request):
        """
        Record a PayPal payment webhook
        """
        data = request.data

        invoice_data = data.get("resource")
        invoice_number = invoice_data.get("id")

        payment_object = None

        try:
            payment_object = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

        paid_amount = invoice_data.get("paid_amount")

        total_amount_paid = Decimal(0)

        for item in paid_amount:
            total_amount_paid += Decimal(paid_amount[item]["value"])

        payment_object.amount_paid = total_amount_paid
        payment_object.save()

        trip_invitation = payment_object.tripinvitation_set.all()[0]

        if Decimal(payment_object.amount_paid) == Decimal(payment_object.amount_due):
            trip_invitation.status = "Paid"
        else:
            trip_invitation.status = "Deposit Paid"

        trip_invitation.save()

        return Response(status=status.HTTP_200_OK)
