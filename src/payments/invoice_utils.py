import datetime
import json

from django.conf import settings

import requests


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

    def create_invoice_draft(
        self,
        invoice_number,
        recipient_given_name,
        recipient_surname,
        recipient_phone,
        recipient_email,
        recipient_address,
        trip_name,
        trip_date,
        trip_description,
        trip_price,
        trip_deposit,
        trip_quantity,
        additional_travelers_quantity,
        additional_traveler_price,
    ):
        url = "{}/v2/invoicing/invoices".format(self.root_url)

        trip_deposit = trip_deposit * (trip_quantity + additional_travelers_quantity)

        today = datetime.datetime.today()

        due_date = trip_date - datetime.timedelta(days=31)

        data = {
            "detail": {
                "invoice_number": invoice_number,
                "reference": "deal-ref",
                "invoice_date": str(today.date()),
                "currency_code": "USD",
                "note": (
                    "In order to avoid the 3% Processing fees for all online transactions, "
                    "you can mail us a check for the remaining balance. Please make out the "
                    "check payable to GFL Soccer Enterprises, and mail to GFL Soccer 6339 "
                    "Hobson St. N. E. St. Petersburg, FL 33702. \n"
                    "You can also use a direct bank deposit or Zelle. "
                    "Please reach out to us at contact@gflsoccer.com if you want to do a direct deposit."
                ),
                "terms_and_conditions": (
                    "We have received your deposit. Thank you! \n"
                    "We need an additional minimum of $500.00 (or $515.00 with 3% processing fee added) "
                    "ASAP in order to add your child to the uniform roster and you to be able to order the uniform for the trip. \n"
                    "The final amount due for the trip is {}. \n"
                    "You can pay partial, or the full amount of this invoice at any time. \n"
                ).format(due_date.strftime("%B %d, %Y")),
                "payment_term": {
                    "term_type": "DUE_ON_DATE_SPECIFIED",
                    "due_date": str(due_date.date()),
                },
            },
            "invoicer": {  # Fill out invoicer info
                "business_name": "AP Soccer Enterprises, LLC",
                "address": {
                    "address_line_1": "6339 Hobson St. N. E.",
                    "address_line_2": "",
                    "admin_area_2": "Saint Petersburg",
                    "admin_area_1": "FL",
                    "postal_code": "33702",
                    "country_code": "US",
                },
                "email_address": "sb-qswj5269996@business.example.com",
                "phones": [
                    {
                        "country_code": "001",
                        "national_number": "4085551234",
                        "phone_type": "MOBILE",
                    }
                ],
                "website": "https://gflsoccer.com",
                "tax_id": "45-4532237",
                "logo_url": "https://pics.paypal.com/00/s/NzE0WDE2MDA=/z/iTUAAOSwFTRTog2G/$_109.GIF",
            },
            "primary_recipients": [
                {
                    "billing_info": {
                        "name": {
                            "given_name": recipient_given_name,
                            "surname": recipient_surname,
                        },
                        "address": {
                            "address_line_1": "1234 Main Street",
                            "admin_area_2": "Anytown",
                            "admin_area_1": "CA",
                            "postal_code": "98765",
                            "country_code": "US",
                        },
                        "email_address": recipient_email,
                        "phones": [
                            {
                                "country_code": "001",
                                "national_number": "4884551234",
                                "phone_type": "HOME",
                            }
                        ],
                    }
                }
            ],
            "items": [
                {
                    "name": trip_name,
                    "description": trip_description,
                    "quantity": trip_quantity,
                    "unit_amount": {"currency_code": "USD", "value": trip_price},
                    "unit_of_measure": "QUANTITY",
                },
                {
                    "name": "Additional Traveler for {}".format(trip_name),
                    "quantity": additional_travelers_quantity,
                    "unit_amount": {
                        "currency_code": "USD",
                        "value": additional_traveler_price,
                    },
                    "unit_of_measure": "QUANTITY",
                },
            ],
            "configuration": {
                "partial_payment": {
                    "allow_partial_payment": True,
                    "minimum_amount_due": {
                        "currency_code": "USD",
                        "value": str(trip_deposit),
                    },
                },
                "allow_tip": False,
                "tax_calculated_after_discount": True,
                "tax_inclusive": False,
            },
        }

        response = self.session.post(url, data=json.dumps(data))

        return response.json()["href"]


# Additional items - managed by admin
# Paypal amount paid / total amount
# https://www.npmjs.com/package/signature_pad
# Send reminder button
# Pass trip date to DUE_DATE
