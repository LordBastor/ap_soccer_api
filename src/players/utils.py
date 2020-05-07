from django.conf import settings
from django.core.mail import send_mail
from django.core.mail.message import EmailMultiAlternatives


def send_player_invite(name, email, uid, trip_name, trip_template, attachments):
    subject = "You have been selected for {}!".format(trip_name)
    message = ""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    html_message = trip_template

    html_message = html_message.replace("{{player_name}}", name)
    html_message = html_message.replace(
        "{{invitation_link}}", "https://example.com/{}".format(uid)
    )

    invitation_email = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=from_email,
        to=recipient_list,
        reply_to=[from_email],
    )

    invitation_email.attach_alternative(html_message, "text/html")

    for attachment in attachments:
        invitation_email.attach_file(attachment.document.path)

    return invitation_email.send(fail_silently=True)

    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=True,
    )
