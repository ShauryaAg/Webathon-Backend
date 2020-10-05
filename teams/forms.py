from django import forms
from django.utils.translation import ugettext_lazy as _


class ResetPasswordForm(forms.Form):

    new_password = forms.CharField(required=True, label='New Password')

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)