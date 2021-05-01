from decimal import Decimal

import datetime
import json

from django.conf import settings

import requests


def generate_detail(invoice_number, today, deposit_only, due_date):

    note = (
        "All online transactions are subject to a 3% Processing fee.\n"
        "In order to avoid those fees, you can pay the rest of the the "
        "remaining balance via check, money order or Zelle.\n"
        "For Check/money orders, please make them payable to AP Soccer LLC "
        "and mail them to: AP Soccer 6339 Hobson St. N. E. St. Petersburg, FL 33702.\n"
        "For Zelle, please use support@americanpremiersoccer.com for all payments to "
        "our account."
    )

    if deposit_only:
        note = (
            "All online transactions are subject to a 3% Processing fee "
            "($500.00 + 3% Processing Fee $15.00 = $515.00).\n"
            "In order to avoid those fees, you can pay the rest of the amount, "
            "after the deposit is paid using check, money order, or Zelle.\n"
            "Additional information will be provided, once your deposit/s is received.\n"
            "Thank you!"
        )

    terms_and_conditions = (
        "All outstanding balances have to be closed by {}.\n"
        "Please reach out to us at support@americanpremiersoccer.com if you have any "
        "questions.\n"
        "Thank you!"
    ).format(due_date.strftime("%B %d, %Y"))

    detail = {
        "invoice_number": invoice_number,
        "reference": "deal-ref",
        "invoice_date": str(today.date()),
        "currency_code": "USD",
        "note": note,
        "terms_and_conditions": terms_and_conditions,
        "payment_term": {
            "term_type": "DUE_ON_DATE_SPECIFIED",
            "due_date": str(due_date),
        },
    }

    return detail


def generate_invoicer():
    invoicer_email_address = (
        "support@americanpremiersoccer.com"
        if settings.ENVIRONMENT == "production"
        else "sb-qswj5269996@business.example.com"
    )

    invoicer = {
        "business_name": "AP Soccer Enterprises, LLC",
        "address": {
            "address_line_1": "6339 Hobson St. N. E.",
            "address_line_2": "",
            "admin_area_2": "Saint Petersburg",
            "admin_area_1": "FL",
            "postal_code": "33702",
            "country_code": "US",
        },
        "email_address": invoicer_email_address,
        "phones": [
            {
                "country_code": "+1",
                "national_number": "727-452-4246",
                "phone_type": "MOBILE",
            }
        ],
        "website": "https://americanpremiersoccer.com",
        "tax_id": "84-3667031",
        "logo_url": "https://americanpremiersoccer.com/wp-content/uploads/2020/01/APS-Transparent-Final-Small-Resised-2.png",
    }

    return invoicer


def generate_recipients(player):
    recipients = [
        {
            "billing_info": {
                "name": {
                    "given_name": player["parent_first_name"],
                    "surname": player["parent_last_name"],
                },
                "address": {
                    "address_line_1": player["address"],
                    "admin_area_2": player["city"],
                    "admin_area_1": player["state"],
                    "postal_code": player["zip_code"],
                    "country_code": "US",
                },
                "email_address": player["email"],
            }
        }
    ]
    return recipients


def generate_configuration(deposit_only):
    configuration = {
        "partial_payment": {"allow_partial_payment": "True"},
        "allow_tip": False,
        "tax_calculated_after_discount": True,
        "tax_inclusive": False,
    }

    # Remove support for partial payments if we are doing deposit flow
    if deposit_only:
        configuration["partial_payment"]["allow_partial_payment"] = "False"
        del configuration["partial_payment"]["minimum_amount_due"]

    return configuration


def generate_items(trip_invite, player, deposit_only):
    trip = trip_invite.trip
    trip_name = trip.name
    player_price = trip.deposit_amount if deposit_only else trip.player_price
    traveler_price = trip.deposit_amount if deposit_only else trip.traveler_price
    type_of_payment = "Deposit" if deposit_only else "Payment"

    additional_people = trip_invite.form_information["companions"]

    player_data = []

    # Conditionally compute additional players
    if "players" in additional_people:
        player_data = [
            {
                "name": "{type_of_payment} for {first_name} {last_name} to attend {trip_name}".format(
                    type_of_payment=type_of_payment,
                    first_name=additional_player["first_name"],
                    last_name=additional_player["last_name"],
                    trip_name=trip_name,
                ),
                "quantity": 1,
                "unit_amount": {"currency_code": "USD", "value": player_price},
                "unit_of_measure": "QUANTITY",
            }
            for additional_player in additional_people["players"]
        ]

    # Add player to first position in player array
    player_data.insert(
        0,
        {
            "name": "{type_of_payment} for {first_name} {last_name} to attend {trip_name}".format(
                type_of_payment=type_of_payment,
                first_name=player["first_name"],
                last_name=player["last_name"],
                trip_name=trip_name,
            ),
            "quantity": 1,
            "unit_amount": {"currency_code": "USD", "value": player_price},
            "unit_of_measure": "QUANTITY",
        },
    )

    traveler_data = []
    if "companions" in additional_people:
        traveler_data = [
            {
                "name": (
                    "{type_of_payment} for {first_name} {last_name} to accompany a "
                    "player on {trip_name}.{package}"
                ).format(
                    type_of_payment=type_of_payment,
                    first_name=traveler["first_name"],
                    last_name=traveler["last_name"],
                    trip_name=trip_name,
                    package=" + ${}".format(traveler["additional_price"])
                    if traveler["additional_price"]
                    else "",
                ),
                "quantity": 1,
                "unit_amount": {"currency_code": "USD", "value": traveler_price},
                "unit_of_measure": "QUANTITY",
            }
            for traveler in additional_people["companions"]
        ]

    player_data.extends(traveler_data)
    return player_data


def generate_invoice_for_trip_invite(trip_invite, deposit_only):
    """
    Given a trip_invitation object and a boolean - generates an invoice
    If deposit_only is True - invoice is generated only for a deposit
    Otherwise - generates for the leftover amount
    """
    client = PayPalClient()

    # Data needed for Detail Invoice Section
    invoice_number = client.generate_invoice_number()
    today = datetime.datetime.today()
    due_date = trip_invite.trip.from_date - datetime.timedelta(days=31)

    # Data needed for Recipients Invoice Section
    player = trip_invite.form_information["player"]

    detail = generate_detail(invoice_number, today, deposit_only, due_date)
    invoicer = generate_invoicer()
    recipients = generate_recipients(player)
    configuration = generate_configuration(deposit_only)
    items = generate_items(trip_invite, player, deposit_only)

    draft = client.create_invoice_draft(
        detail=detail,
        invoicer=invoicer,
        recipients=recipients,
        items=items,
        configuration=configuration,
    )

    invoice_id = draft["href"].split("/")[-1]

    client.send_invoice(invoice_id)

    trip_invite.payment.invoice_number = invoice_id

    # Build invoice url and save it so we can expose it in next trip step
    paypal_url = (
        "https://www.sandbox.paypal.com/invoice/p/#"
        if settings.ENVIRONMENT == "production"
        else "https://www.sandbox.paypal.com/invoice/p/#"
    )
    trip_invite.payment.invoice_url = "{}{}".format(paypal_url, invoice_id)
    trip_invite.payment.save()

    return invoice_id


class PayPalClient:
    def __init__(self):
        self.root_url = (
            "https://api.paypal.com"
            if settings.ENVIRONMENT == "production"
            else "https://api.sandbox.paypal.com"
        )
        client_id = settings.PAYPAL_CLIENT_ID
        client_secret = settings.PAYPAL_SECRET

        token_session = requests.Session()
        token_session.auth = (client_id, client_secret)
        token_session.headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
        }

        data = {"grant_type": "client_credentials"}

        response = token_session.post(
            "{}/v1/oauth2/token".format(self.root_url), data=data
        )

        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(response.json()["access_token"]),
        }

    def generate_invoice_number(self):
        url = "{}/v2/invoicing/generate-next-invoice-number".format(self.root_url)
        response = self.session.post(url)
        return response.json()["invoice_number"]

    def send_invoice(self, invoice_id):
        url = "{}/v2/invoicing/invoices/{}/send".format(self.root_url, invoice_id)
        data = {
            "send_to_recipient": True,
            "send_to_invoicer": True,
            # "additional_recipients": [],
        }
        response = self.session.post(url, data=json.dumps(data))

        return response

    def add_payment_to_invoice(self, invoice_id, method, amount, note=""):
        url = "{}/v2/invoicing/invoices/{}/payments".format(self.root_url, invoice_id)
        data = {
            "payment_date": datetime.date.today().strftime("%Y-%m-%d"),
            "method": method,
            "note": note,
            "amount": {"currency_code": "USD", "value": amount},
        }

        response = self.session.post(url, data=json.dumps(data))

        return response

    def create_invoice_draft(
        self, detail, invoicer, recipients, items, configuration, data,
    ):
        url = "{}/v2/invoicing/invoices".format(self.root_url)

        data = {
            "detail": detail,
            "invoicer": invoicer,
            "primary_recipients": recipients,
            "items": items,
            "configuration": configuration,
        }

        response = self.session.post(url, data=json.dumps(data))

        return response.json()
