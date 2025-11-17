"""
This module defines the four concrete models:
    * :class:`Value`
    * :class:`Attribute`
    * :class:`EnumValue`
    * :class:`EnumGroup`.

Along with the :class:`Entity` helper class and :class:`EAVModelMeta`
optional metaclass for each eav model class.

The :class:`Attribute` model is swappable and can be extended via
:class:`AbstractAttribute`. Other models are regular Django models.
"""

from .attribute import AbstractAttribute, Attribute
from .entity import EAVModelMeta, Entity
from .enum_group import EnumGroup
from .enum_value import EnumValue
from .utils import get_attribute_model
from .value import Value

__all__ = [
    "AbstractAttribute",
    "Attribute",
    "EAVModelMeta",
    "Entity",
    "EnumGroup",
    "EnumValue",
    "Value",
    "get_attribute_model",
]
