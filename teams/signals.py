from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from .models import Team

def students_changed(sender, **kwargs):

    print(kwargs)

    if kwargs['instance'].students.count() > 4:
        raise ValidationError("You cant assign more than 4 members in a Team")
