"""
This module defines the EAV models and base classes.

Concrete models (swappable):
    * :class:`Value` - Stores EAV values
    * :class:`Attribute` - Defines EAV attributes
    * :class:`EnumValue` - Enum value choices
    * :class:`EnumGroup` - Groups of enum values

Abstract base models (for customization):
    * :class:`AbstractValue`
    * :class:`AbstractAttribute`
    * :class:`AbstractEnumValue`
    * :class:`AbstractEnumGroup`

Helper classes:
    * :class:`Entity` - EAV helper class
    * :class:`EAVModelMeta` - Optional metaclass for EAV models
"""

from .abstract import (
    AbstractAttribute,
    AbstractEnumGroup,
    AbstractEnumValue,
    AbstractValue,
)
from .attribute import Attribute
from .entity import EAVModelMeta, Entity
from .enum_group import EnumGroup
from .enum_value import EnumValue
from .value import Value

__all__ = [
    # Concrete models
    "Attribute",
    "EnumGroup",
    "EnumValue",
    "Value",
    # Abstract models
    "AbstractAttribute",
    "AbstractEnumGroup",
    "AbstractEnumValue",
    "AbstractValue",
    # Helper classes
    "EAVModelMeta",
    "Entity",
]
