from decimal import Decimal

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.invoice_utils import PayPalClient, generate_invoice_for_trip_invite
from payments.models import Payment, PayPalInvoice


def record_payment(request, *args, **kwargs):
    invoice_ids = request.POST.get("invoice_ids", None)
    amount = request.POST.get("amount", None)
    method = request.POST.get("method", None)
    note = request.POST.get("note", "")

    if amount is None or method is None:
        messages.add_message(
            request,
            messages.ERROR,
            "Missing payment amount and/or method data",
        )
        return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))

    if invoice_ids is None:
        messages.add_message(
            request,
            messages.ERROR,
            "Missing invoice data",
        )
        return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))

    invoice_ids = invoice_ids.split(",")

    if len(invoice_ids) > 1:
        messages.add_message(request, messages.ERROR, "Multiple payments selected!")
        return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))

    invoice = PayPalInvoice.objects.get(id=invoice_ids[0])

    client = PayPalClient()

    response = client.add_payment_to_invoice(
        invoice_id=invoice.invoice_number, amount=amount, method=method, note=note
    )

    if response.ok:
        # Update payment object
        invoice.amount_paid += Decimal(amount)
        invoice.save()

        # Return success response
        messages.add_message(
            request,
            messages.SUCCESS,
            "Succesfully recorded a payment of {} to invoice with id {}".format(
                amount, invoice.invoice_number
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

        resource = data.get("resource")
        invoice_data = resource.get("invoice")
        invoice_number = invoice_data.get("id")
        payment_data = invoice_data.get("payments")
        paid_amount = payment_data.get("paid_amount")

        invoice_object = None

        try:
            invoice_object = PayPalInvoice.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

        # Update the invoice paid amount
        invoice_object.amount_paid = Decimal(paid_amount["value"])
        invoice_object.save()

        # Let's grab the total amount paid so far
        payment_object = invoice_object.payment
        total_amount_paid = payment_object.paypalinvoice_set.aggregate(
            Sum("amount_paid")
        )["amount_paid__sum"]

        # Get the trip invite
        trip_invitation = invoice_object.payment.tripinvitation_set.all()[0]

        if total_amount_paid >= payment_object.amount_due:
            trip_invitation.status = "Paid"
        elif total_amount_paid >= payment_object.amount_deposit:
            trip_invitation.status = "Deposit Paid"

        trip_invitation.save()

        # Moved this outside of the if/elif so we don't fail to update
        # the payment if invoice creation fails for some reason
        existing_invoice_count = trip_invitation.payment.paypalinvoice_set.count()
        if (
            trip_invitation.status in ["Deposit Paid", "Paid"]
            and existing_invoice_count == 1
        ):
            # Create and send leftover invoice
            generate_invoice_for_trip_invite(trip_invitation, False)

        return Response(status=status.HTTP_200_OK)
