from __future__ import annotations

from django.conf import settings

from .abstract import AbstractEnumValue


class EnumValue(AbstractEnumValue):
    """
    Concrete implementation of EnumValue model.
    
    This is the default EnumValue model. To customize this model, create your own
    model that inherits from AbstractEnumValue and set EAV_ENUM_VALUE_MODEL in your
    Django settings.
    
    See AbstractEnumValue for full documentation on fields and methods.
    """

    class Meta(AbstractEnumValue.Meta):
        swappable = getattr(settings, 'EAV_ENUM_VALUE_MODEL', 'eav.EnumValue')
