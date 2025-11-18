"""
This module defines the four concrete models:
    * :class:`Value`
    * :class:`Attribute`
    * :class:`EnumValue`
    * :class:`EnumGroup`.

Along with the :class:`Entity` helper class and :class:`EAVModelMeta`
optional metaclass for each eav model class.

The :class:`Attribute` and :class:`Value` models are swappable and can be extended via
:class:`AbstractAttribute` and :class:`AbstractValue` respectively. Other models are regular Django models.
"""

from .attribute import AbstractAttribute, Attribute
from .entity import EAVModelMeta, Entity
from .enum_group import EnumGroup
from .enum_value import EnumValue
from .utils import get_attribute_model, get_value_model
from .value import AbstractValue, Value

__all__ = [
    "AbstractAttribute",
    "AbstractValue",
    "Attribute",
    "EAVModelMeta",
    "Entity",
    "EnumGroup",
    "EnumValue",
    "Value",
    "get_attribute_model",
    "get_value_model",
]
