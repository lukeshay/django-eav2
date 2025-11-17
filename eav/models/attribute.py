# ruff: noqa: UP007

from __future__ import annotations

from django.conf import settings

from .abstract import AbstractAttribute


class Attribute(AbstractAttribute):
    """
    Concrete implementation of Attribute model.
    
    This is the default Attribute model. To customize this model, create your own
    model that inherits from AbstractAttribute and set EAV_ATTRIBUTE_MODEL in your
    Django settings.
    
    See AbstractAttribute for full documentation on fields and methods.
    """

    class Meta(AbstractAttribute.Meta):
        swappable = getattr(settings, 'EAV_ATTRIBUTE_MODEL', 'eav.Attribute')
