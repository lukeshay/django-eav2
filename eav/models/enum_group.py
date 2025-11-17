from __future__ import annotations

from django.conf import settings

from .abstract import AbstractEnumGroup


class EnumGroup(AbstractEnumGroup):
    """
    Concrete implementation of EnumGroup model.
    
    This is the default EnumGroup model. To customize this model, create your own
    model that inherits from AbstractEnumGroup and set EAV_ENUM_GROUP_MODEL in your
    Django settings.
    
    See AbstractEnumGroup for full documentation on fields and methods.
    """

    class Meta(AbstractEnumGroup.Meta):
        swappable = getattr(settings, 'EAV_ENUM_GROUP_MODEL', 'eav.EnumGroup')
