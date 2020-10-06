from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.response import Response

from .models import Team

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


def students_changed(sender, **kwargs):

    print(kwargs)

    if kwargs['instance'].students.count() > 4:
        raise serializers.ValidationError({"err": "You cant assign more than 4 members in a Team"})


m2m_changed.connect(students_changed, sender=Team.students.through,
                    dispatch_uid='students_changed')


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    }

    # render email text
    # email_html_message = render_to_string(
    #     'email/user_reset_password.html', context)
    # email_plaintext_message = render_to_string(
    #     'email/user_reset_password.txt', context)

    email_plaintext_message = f'The OTP to reset your password is {reset_password_token.key}'

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for DSC BVP",
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.send()
