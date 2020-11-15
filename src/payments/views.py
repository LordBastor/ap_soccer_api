from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from payments.models import Payment

from payments.invoice_utils import PayPalClient


def record_payment(request, *args, **kwargs):
    invoice_ids = request.POST.get("invoice_ids", None)
    amount = request.POST.get("amount", None)
    method = request.POST.get("method", None)
    note = request.POST.get("note", None)

    if amount is None or method is None:
        messages.add_message(
            request, messages.ERROR, "Missing payment amount and/or method data",
        )
        return HttpResponseRedirect(reverse("admin:payments_payment_changelist"))


# def invite_to_trip(request, *args, **kwargs):
#     trip_id = request.POST.get("trip_id", None)
#     player_ids = request.POST.getlist("player_ids", None)

#     if not trip_id or not player_ids:
#         messages.add_message(
#             request, messages.ERROR, "Missing trip and/or player data",
#         )
#         return HttpResponseRedirect(reverse("admin:players_player_changelist"))

#     try:
#         trip = Trip.objects.get(pk=trip_id)
#     except (Trip.DoesNotExist, Trip.MultipleObjects):
#         messages.add_message(
#             request, messages.ERROR, "Specified Trip not found",
#         )
#         return HttpResponseRedirect(reverse("admin:players_player_changelist"))

#     players = Player.objects.filter(id__in=player_ids)

#     successful_sends = 0

#     for player in players:
#         # Create the player invitation
#         invitation = TripInvitation.objects.create(
#             trip=trip, player=player, status=TripInvitation.INVITE_SENT
#         )

#         # Attempt to send invite email
#         success = send_player_invite(
#             player.first_name,
#             player.email,
#             invitation.uid,
#             trip.name,
#             trip.email_template,
#             trip.email_files.all(),
#         )

#         # If something goes wrong - let the user know and remove unused invitation
#         if success:
#             successful_sends += 1
#         else:
#             invitation.delete()
#             messages.add_message(
#                 request,
#                 messages.ERROR,
#                 "Failed to send invitation to {}".format(player),
#             )

#     messages.add_message(
#         request,
#         messages.SUCCESS,
#         "Succesfully invited {} players to {}".format(successful_sends, trip.name),
#     )
#     return HttpResponseRedirect(reverse("admin:players_player_changelist"))
