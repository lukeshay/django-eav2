# ruff: noqa: UP007
from __future__ import annotations

from django.conf import settings

from .abstract import AbstractValue


class Value(AbstractValue):
    """
    Concrete implementation of Value model.
    
    This is the default Value model. To customize this model, create your own
    model that inherits from AbstractValue and set EAV_VALUE_MODEL in your
    Django settings.
    
    See AbstractValue for full documentation on fields and methods.
    """

    class Meta(AbstractValue.Meta):
        swappable = getattr(settings, 'EAV_VALUE_MODEL', 'eav.Value')
